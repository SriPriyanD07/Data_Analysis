"""
Intent Parser - Extract structured intent from user task description
"""

import pandas as pd
from typing import Dict, List, Optional
import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()


class IntentParser:
    def __init__(self):
        genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
        self.model = genai.GenerativeModel('gemini-pro')
    
    def parse(self, dataset_path: str, task_description: str) -> Dict:
        """
        Parse user intent from task description and dataset
        
        Returns:
            Dict with keys: task_type, target_column, columns_info, suggestions
        """
        # Load dataset to analyze schema
        try:
            df = pd.read_csv(dataset_path, nrows=5)
            
            schema_info = {
                "columns": list(df.columns),
                "dtypes": {col: str(dtype) for col, dtype in df.dtypes.items()},
                "shape": df.shape,
                "sample": df.head(3).to_dict()
            }
        except Exception as e:
            raise ValueError(f"Could not read dataset: {e}")
        
        # Use LLM to parse intent
        intent = self._parse_with_llm(task_description, schema_info)
        intent["schema"] = schema_info
        
        return intent
    
    def _parse_with_llm(self, task_description: str, schema_info: Dict) -> Dict:
        """
        Use LLM to extract structured intent
        """
        prompt = f"""You are analyzing a data science task request.

Dataset Schema:
- Columns: {', '.join(schema_info['columns'])}
- Shape: {schema_info['shape'][0]} rows × {schema_info['shape'][1]} columns
- Data types: {schema_info['dtypes']}

User Task: "{task_description}"

Extract the following information in JSON format:
{{
    "task_type": "eda" | "classification" | "regression" | "clustering" | "hypothesis_testing" | "correlation",
    "target_column": "column_name or null if not applicable",
    "focus_columns": ["list of specific columns mentioned, or empty array"],
    "analysis_goals": ["specific analysis goals extracted from task"],
    "suggested_sections": ["list of EDA sections to include"]
}}

For Phase 1 MVP, default to "eda" task type unless clearly specified otherwise.
Suggested sections can include: data_overview, missing_values, distributions, correlations, target_analysis, outliers, statistical_summary.
"""
        
        try:
            # Construct full prompt with system context
            full_prompt = f"""You are a data science assistant that parses task descriptions.

{prompt}

IMPORTANT: Respond ONLY with valid JSON. Do not include any explanatory text before or after the JSON."""
            
            response = self.model.generate_content(
                full_prompt,
                generation_config={
                    'temperature': 0.3,
                }
            )
            
            import json
            # Extract JSON from response
            response_text = response.text.strip()
            # Remove markdown code blocks if present
            if '```json' in response_text:
                response_text = response_text.split('```json')[1].split('```')[0].strip()
            elif '```' in response_text:
                response_text = response_text.split('```')[1].split('```')[0].strip()
            
            intent = json.loads(response_text)
            return intent
            
        except Exception as e:
            print(f"LLM parsing failed: {e}, using fallback")
            # Fallback intent
            return {
                "task_type": "eda",
                "target_column": None,
                "focus_columns": [],
                "analysis_goals": ["Perform exploratory data analysis"],
                "suggested_sections": [
                    "data_overview",
                    "missing_values",
                    "statistical_summary",
                    "distributions",
                    "correlations"
                ]
            }
