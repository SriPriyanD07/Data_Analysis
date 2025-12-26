# 🚀 Agentic Notebook Generator

> **AI-Powered Data Analysis Automation** - Automatically generate comprehensive EDA (Exploratory Data Analysis) notebooks using Google Gemini AI

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104.1-009688.svg)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

## 📋 Overview

The **Agentic Notebook Generator** is an intelligent system that transforms raw CSV datasets into comprehensive Jupyter notebooks with professional exploratory data analysis. Simply upload your data and describe what you want to analyze - the AI agent handles the rest!

### ✨ Key Features

- 🤖 **AI-Powered Code Generation** using Google Gemini Pro
- 📊 **Automated EDA** with statistical summaries, visualizations, and insights
- 🎯 **Intent Parsing** to understand your analysis goals
- 📈 **Professional Visualizations** with matplotlib and seaborn
- 🌐 **Modern Web Interface** for easy interaction
- ⚡ **Fast API Backend** for robust processing
- 📓 **Ready-to-Use Notebooks** in standard Jupyter format

## 🎥 Demo

Upload your CSV → Describe your analysis goals → Get a complete notebook with:
- Dataset overview
- Missing value analysis
- Statistical summaries
- Distribution plots
- Correlation heatmaps
- Outlier detection
- Target variable analysis

## 🏗️ Architecture

```
agentic-notebook/
├── backend/
│   ├── main.py                 # FastAPI server
│   ├── intent_parser.py        # AI-powered intent extraction
│   ├── code_generator.py       # Gemini-based code generation
│   ├── notebook_builder.py     # Jupyter notebook construction
│   ├── uploads/                # Uploaded CSV files
│   └── outputs/                # Generated notebooks
├── frontend/
│   ├── index.html             # Web interface
│   └── style.css              # Styling
├── test_data/
│   └── sample_iris.csv        # Sample dataset for testing
├── requirements.txt           # Python dependencies
├── .env.example              # Environment template
└── start.bat                 # Quick start script
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Google API Key ([Get one here](https://makersuite.google.com/app/apikey))
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/SriPriyanD07/Data_Analysis.git
   cd Data_Analysis
   ```

2. **Set up environment variables**
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` and add your Google API key:
   ```
   GOOGLE_API_KEY=your_api_key_here
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   
   **Windows:**
   ```bash
   start.bat
   ```
   
   **Mac/Linux:**
   ```bash
   cd backend
   python main.py
   ```

5. **Open in browser**
   
   Navigate to: `http://localhost:8000/app`

## 📖 Usage

### Via Web Interface

1. Open `http://localhost:8000/app` in your browser
2. Click "Choose File" and select your CSV dataset
3. Enter a task description (e.g., "Perform comprehensive EDA" or "Analyze customer churn patterns")
4. Click "Generate Notebook"
5. Download your generated `.ipynb` file

### Via API

```python
import requests

# Upload file and generate notebook
files = {'file': open('data.csv', 'rb')}
data = {'task_description': 'Perform comprehensive EDA'}

response = requests.post(
    'http://localhost:8000/api/generate',
    files=files,
    data=data
)

print(response.json())
```

### API Endpoints

- `GET /` - API information
- `POST /api/generate` - Generate notebook from CSV
- `GET /api/download/{filename}` - Download generated notebook
- `GET /api/notebooks` - List all generated notebooks
- `GET /app` - Web interface

## 🧪 Example

**Input:**
- CSV: Customer data with demographics and purchase history
- Task: "Analyze customer behavior and identify patterns"

**Output:**
A complete Jupyter notebook with:
1. Data loading and overview (shape, columns, types)
2. Missing value analysis with visualizations
3. Statistical summary for all features
4. Distribution plots for numerical features
5. Correlation analysis with heatmap
6. Category analysis for categorical features
7. Outlier detection

## 🔧 Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `GOOGLE_API_KEY` | Your Google Gemini API key | Yes |

### Customization

Edit `backend/code_generator.py` to customize:
- Analysis sections
- Visualization styles
- Code generation prompts
- Model parameters (temperature, max tokens)

## 🛠️ Technology Stack

### Backend
- **FastAPI** - Modern, fast web framework
- **Google Gemini Pro** - AI code generation
- **Pandas** - Data manipulation
- **Matplotlib/Seaborn** - Visualizations
- **Nbformat** - Jupyter notebook creation

### Frontend
- **HTML5/CSS3** - Modern web interface
- **Vanilla JavaScript** - Interactive UI
- **Responsive Design** - Works on all devices

## 📊 Supported Analysis Types

- ✅ Exploratory Data Analysis (EDA)
- ✅ Classification problem setup
- ✅ Regression problem setup
- ✅ Correlation analysis
- ✅ Distribution analysis
- ✅ Outlier detection
- ✅ Missing value analysis

## 🗺️ Roadmap

### Phase 1 (Current) - MVP
- [x] Basic EDA notebook generation
- [x] Web interface
- [x] Google Gemini integration

### Phase 2 - Enhanced Analysis
- [ ] Advanced statistical tests
- [ ] Feature engineering suggestions
- [ ] Model recommendation

### Phase 3 - Interactive Notebooks
- [ ] Parameter tuning interface
- [ ] Real-time notebook preview
- [ ] Custom section templates

### Phase 4 - Advanced Features
- [ ] Multi-file analysis
- [ ] Time series support
- [ ] Automated reporting

### Phase 5 - Intelligence
- [ ] Self-correcting code
- [ ] Iterative refinement
- [ ] Insight generation

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Google Gemini AI for powerful code generation
- FastAPI for the excellent web framework
- The open-source data science community

## 📞 Contact

**Sri Priyan D**
- GitHub: [@SriPriyanD07](https://github.com/SriPriyanD07)
- Repository: [Data_Analysis](https://github.com/SriPriyanD07/Data_Analysis)

## ⚠️ Important Notes

1. **API Key Security**: Never commit your `.env` file with your actual API key
2. **Rate Limits**: Be aware of Google Gemini API rate limits and quotas
3. **Data Privacy**: Uploaded data is stored locally - ensure sensitive data is handled appropriately
4. **Cost**: Google Gemini API usage may incur costs depending on your plan

## 🐛 Troubleshooting

### Common Issues

**Server won't start:**
- Check if Python 3.8+ is installed: `python --version`
- Ensure all dependencies are installed: `pip install -r requirements.txt`
- Verify your API key is set in `.env`

**Notebook generation fails:**
- Verify your Google API key is valid
- Check your API quota hasn't been exceeded
- Ensure CSV file is properly formatted

**Import errors:**
- Reinstall dependencies: `pip install -r requirements.txt --force-reinstall`

---

**Made with ❤️ for the Data Science Community**

*Star ⭐ this repository if you find it helpful!*
