# 🩺 AI Medical Report Explainer

An AI-powered web application that helps users understand their blood test reports in simple and easy-to-understand language.

## 🚀 Features

- Upload blood test reports in PDF format.
- Extract text from PDF reports.
- Analyze blood test values automatically.
- Compare results with reference ranges.
- Identify Normal, High, and Low values.
- Generate simple explanations using Google Gemini AI.
- Download professional medical analysis reports as PDF.

## 🛠️ Technologies Used

- Python
- Streamlit
- Google Gemini AI
- Pandas
- PyMuPDF
- ReportLab

## 📂 Project Structure

```text
AI-Medical-Report-Explainer/
│
├── app.py
├── ai_explainer.py
├── pdf_extractor.py
├── report_analyzer.py
├── requirements.txt
└── .gitignore
```

## ⚙️ Installation and Setup

1. Clone the repository:

```bash
git clone https://github.com/sumant973/AI-Medical-Report-Explainer.git
```

2. Open the project folder:

```bash
cd AI-Medical-Report-Explainer
```

3. Create a virtual environment:

```bash
python -m venv venv
```

4. Activate the environment (Windows):

```bash
venv\Scripts\activate
```

5. Install dependencies:

```bash
pip install -r requirements.txt
```

6. Create a `.env` file and add your Gemini API key:

```text
GEMINI_API_KEY=your_api_key_here
```

7. Run the application:

```bash
streamlit run app.py
```

## ⚠️ Disclaimer

This application provides informational explanations only and is not a substitute for professional medical advice, diagnosis, or treatment. Always consult a qualified healthcare professional.

## 👨‍💻 Developer

**Sumant Kumar Singh**

B.Tech Computer Science and Engineering  
MIT ADT University, Pune

GitHub: https://github.com/sumant973

## Application Screenshots

### 1. Home Page
![Home Page](Screenshot%202026-11-22%20222248.png)

### 2. Blood Test Analysis
![Blood Test Analysis](Screenshot 2 filename)

### 3. AI Medical Report Explanation
![AI Explanation](Screenshot 3 filename)

### 4. Download Medical Report PDF
![PDF Download](Screenshot 4 filename)
