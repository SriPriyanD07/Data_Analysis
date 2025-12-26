# Quick Setup Guide

## 🎯 First Time Setup (5 minutes)

### Step 1: Get Your Google API Key
1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the key

### Step 2: Configure Environment
1. Navigate to project directory: `cd Data_Analysis`
2. Copy the example env file: `cp .env.example .env`
3. Open `.env` in a text editor
4. Replace `your_google_api_key_here` with your actual API key
5. Save the file

### Step 3: Install & Run
```bash
# Install dependencies
pip install -r requirements.txt

# Start the server (Windows)
start.bat

# OR start manually
cd backend
python main.py
```

### Step 4: Access the App
Open your browser and go to: `http://localhost:8000/app`

## 📝 Test with Sample Data

1. Use the included sample: `test_data/sample_iris.csv`
2. Task description: "Perform comprehensive exploratory data analysis"
3. Click "Generate Notebook"
4. Download the generated `.ipynb` file
5. Open in Jupyter Notebook/Lab

## 🎨 Project Structure Explained

```
Data_Analysis/
│
├── backend/              # Server-side code
│   ├── main.py          # FastAPI application
│   ├── intent_parser.py # Understands your task description
│   ├── code_generator.py# Generates Python code using Gemini
│   ├── notebook_builder.py # Creates Jupyter notebooks
│   ├── uploads/         # Temporary CSV storage
│   └── outputs/         # Generated notebooks
│
├── frontend/            # User interface
│   ├── index.html       # Web application
│   └── style.css        # Styling
│
├── test_data/           # Sample datasets
│   └── sample_iris.csv  # Classic iris dataset
│
├── .env.example         # Template for API key
├── .gitignore          # Git ignore rules
├── requirements.txt     # Python packages
├── README.md           # Full documentation
├── LICENSE             # MIT License
└── start.bat           # Quick start script (Windows)
```

## 🔍 What Happens When You Generate?

1. **Upload**: CSV file is saved to `backend/uploads/`
2. **Parse Intent**: AI analyzes your task description
3. **Generate Code**: Gemini creates Python code for each analysis section
4. **Build Notebook**: Code is assembled into a Jupyter notebook
5. **Save**: Notebook saved to `backend/outputs/`
6. **Download**: You get the `.ipynb` file!

## 💡 Tips

- **Task Descriptions**: Be specific! 
  - Good: "Analyze customer churn with focus on demographics"
  - Basic: "Do EDA"
  
- **CSV Format**: Ensure your CSV has:
  - Header row with column names
  - Consistent data types per column
  - UTF-8 encoding

- **Generated Notebooks**: Open with:
  - Jupyter Notebook: `jupyter notebook`
  - Jupyter Lab: `jupyter lab`
  - VS Code with Jupyter extension
  - Google Colab (upload the file)

## 🐛 Common Issues

**"API Key Error"**
- Check your `.env` file has the correct key
- Verify key is from Google AI Studio
- Restart the server after changing `.env`

**"Module Not Found"**
- Run: `pip install -r requirements.txt`
- Check Python version: `python --version` (need 3.8+)

**"Port Already in Use"**
- Change port in `main.py`: `uvicorn.run(app, host="0.0.0.0", port=8001)`

## 📚 Next Steps

1. Generate a notebook with your own data
2. Explore the generated code
3. Customize prompts in `code_generator.py`
4. Star the repo if you find it useful! ⭐

## 🤝 Need Help?

- Check the [full README](README.md)
- Open an issue on GitHub
- Review the code comments

---

**Happy Analyzing! 🎉**
