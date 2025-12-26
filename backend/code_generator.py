"""
Code Generator - Generate Python code for notebook sections using LLM
"""

import os
import google.generativeai as genai
from dotenv import load_dotenv
from typing import Dict, List

load_dotenv()


class CodeGenerator:
    def __init__(self):
        genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
        self.model = genai.GenerativeModel('gemini-pro')
        self.prompts = self._load_prompts()
    
    def _load_prompts(self) -> Dict[str, str]:
        """Load section-specific prompts"""
        return {
            "data_overview": """Generate Python code to display dataset overview:
- Load the CSV file into pandas DataFrame named 'df'
- Display first 5 rows
- Show dataset shape
- Display column names and data types
- Show memory usage

Use only pandas. The dataset path will be provided.""",
            
            "missing_values": """Generate Python code to analyze missing values:
- Calculate missing value count and percentage for each column
- Create a bar chart showing missing value percentages
- Display summary DataFrame with columns: [Column, Missing_Count, Missing_Percentage]

Use pandas, matplotlib, and seaborn.""",
            
            "statistical_summary": """Generate Python code for statistical summary:
- Use df.describe() for numerical columns
- Show value counts for categorical columns (top 10)
- Display properly formatted tables

Use pandas.""",
            
            "distributions": """Generate Python code to visualize distributions:
- For numerical columns: histograms with KDE curves
- For categorical columns: count plots (limit to top 10 categories)
- Create subplots for better organization
- Use appropriate figure size and styling

Use pandas, matplotlib, and seaborn.""",
            
            "correlations": """Generate Python code for correlation analysis:
- Calculate correlation matrix for numerical columns
- Create a heatmap with annotations
- Identify high correlations (> 0.7 or < -0.7)
- Display correlation findings

Use pandas, matplotlib, and seaborn.""",
            
            "target_analysis": """Generate Python code to analyze the target variable:
- Show target variable distribution
- For classification: count plot and percentage breakdown
- For regression: histogram and basic statistics
- Include value counts

Use pandas, matplotlib, and seaborn.""",
            
            "outliers": """Generate Python code for outlier detection:
- Use box plots for numerical columns
- Calculate IQR and identify outliers
- Display outlier statistics

Use pandas, matplotlib, and seaborn."""
        }
    
    def generate_section_code(
        self,
        section_name: str,
        schema_info: Dict,
        additional_context: str = ""
    ) -> str:
        """
        Generate code for a specific EDA section
        """
        columns = schema_info.get("columns", [])
        dtypes = schema_info.get("dtypes", {})
        
        # Identify numerical and categorical columns
        numerical_cols = [col for col, dtype in dtypes.items() if 'int' in dtype or 'float' in dtype]
        categorical_cols = [col for col, dtype in dtypes.items() if dtype == 'object' or 'category' in dtype]
        
        base_prompt = self.prompts.get(section_name, "Generate exploratory data analysis code.")
        
        prompt = f"""{base_prompt}

Dataset Information:
- Total columns: {len(columns)}
- Numerical columns ({len(numerical_cols)}): {', '.join(numerical_cols[:10])}
- Categorical columns ({len(categorical_cols)}): {', '.join(categorical_cols[:10])}

{additional_context}

Requirements:
- Use 'df' as the DataFrame variable name
- Include proper labels, titles, and formatting
- Add comments explaining each step
- Use modern matplotlib/seaborn styling (set style to 'whitegrid' or 'darkgrid')
- Handle edge cases (empty columns, all nulls, etc.)
- Return ONLY executable Python code, no explanations outside code comments
"""
        
        try:
            # Construct full prompt with system context
            full_prompt = f"""You are an expert data scientist. Generate clean, well-documented Python code for data analysis.

{prompt}"""
            
            response = self.model.generate_content(
                full_prompt,
                generation_config={
                    'temperature': 0.3,
                    'max_output_tokens': 1500,
                }
            )
            
            code = response.text
            
            # Extract code from markdown if present
            if "```python" in code:
                code = code.split("```python")[1].split("```")[0].strip()
            elif "```" in code:
                code = code.split("```")[1].split("```")[0].strip()
            
            return code
            
        except Exception as e:
            print(f"Code generation failed for {section_name}: {e}")
            return f"# Error generating code for {section_name}\nprint('Section generation failed: {e}')"
    
    def generate_markdown(self, section_name: str, content: str = "") -> str:
        """
        Generate markdown explanation for a section
        """
        section_titles = {
            "data_overview": "## 📊 Dataset Overview",
            "missing_values": "## 🔍 Missing Values Analysis",
            "statistical_summary": "## 📈 Statistical Summary",
            "distributions": "## 📉 Data Distributions",
            "correlations": "## 🔗 Correlation Analysis",
            "target_analysis": "## 🎯 Target Variable Analysis",
            "outliers": "## ⚠️ Outlier Detection"
        }
        
        descriptions = {
            "data_overview": "Let's start by understanding the basic structure and characteristics of our dataset.",
            "missing_values": "Identifying and quantifying missing data is crucial for data quality assessment.",
            "statistical_summary": "Key statistical measures provide insight into the central tendencies and spread of our data.",
            "distributions": "Visualizing distributions helps identify patterns, skewness, and potential data quality issues.",
            "correlations": "Understanding relationships between variables is essential for feature selection and modeling.",
            "target_analysis": "Analyzing the target variable reveals class balance and distribution characteristics.",
            "outliers": "Detecting outliers helps identify data anomalies that may require special handling."
        }
        
        title = section_titles.get(section_name, f"## {section_name.replace('_', ' ').title()}")
        desc = descriptions.get(section_name, "")
        
        markdown = f"{title}\n\n{desc}"
        if content:
            markdown += f"\n\n{content}"
        
        return markdown
