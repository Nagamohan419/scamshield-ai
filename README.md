
# 🛡️ ScamShield AI

### AI-Powered Scam Message Analyzer & Response Assistant

ScamShield AI is an open-source, AI-powered fraud-awareness application that helps users identify suspicious messages, understand potential scam indicators, and receive personalized safety guidance.

Built with Python, Streamlit, an Excel-based fraud-pattern rule engine, and Google's Gemma 4 model.

## 🚀 Features

### 🔍 AI Scam Message Analyzer
- Analyze suspicious SMS, WhatsApp, banking, UPI, job, shopping, and investment messages.
- Combine Excel-based keyword rules with Gemma 4 analysis.
- Display concern levels: High, Review, Low, and Inconclusive.
- Explain potential warning signs and recommended actions.

### 🤖 Context-Aware Scam Response Agent
- Generate personalized guidance based on the message assessment.
- Provide verification checklists for legitimate-looking or inconclusive messages.
- Suggest account-protection steps when sensitive information has been shared.
- Provide financial-fraud reporting guidance when relevant.

### 🌐 Multilingual Guidance
- English
- Hindi
- Telugu

AI-generated explanations and safety plans can be translated into the selected language.

### 📄 Downloadable Scam Reports
Generate a text report containing:
- Original message
- AI assessment
- Warning signs
- Rule-engine findings
- Personalized safety plan
- Reporting guidance

### 🚨 Report a Scam — India
Find official reporting resources, including:
- National Cybercrime Helpline: 1930
- National Cyber Crime Reporting Portal
- Chakshu — Sanchar Saathi
- Official suspect-reporting resources

ScamShield does not submit complaints automatically.

## 🛠️ Technology Stack

- Python
- Streamlit
- Google Gemma 4 via Google GenAI SDK
- Pandas
- OpenPyXL
- Python-dotenv
- Pytest

## 📁 Project Structure

```text
scamshield-ai/
├── Scam_Message_Analyzer.py
├── pages/
│   └── 1_🚨_Report_a_Scam.py
├── src/
│   ├── __init__.py
│   ├── dataset.py
│   ├── rules.py
│   ├── gemma_service.py
│   ├── response_agent.py
│   └── translation_service.py
├── data/
│   └── ScamShield_Fraud_Dataset.xlsx
├── tests/
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
└── LICENSE
```

## ⚙️ Local Installation

Clone the repository:

```bash
git clone https://github.com/YOUR_USERNAME/scamshield-ai.git
cd scamshield-ai
```

Create a Python virtual environment:

```bash
python -m venv .venv
```

Activate it on Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

Create a `.env` file using `.env.example` as a reference.

Add your Google AI Studio API key:

```env
GEMINI_API_KEY=your_private_api_key
GEMMA_MODEL=gemma-4-26b-a4b-it
```

Run the application:

```bash
python -m streamlit run Scam_Message_Analyzer.py
```

## 🔐 Privacy and Security

- Do not enter real passwords, OTPs, PINs, or sensitive financial information.
- Message analysis uses a hosted AI model, so submitted content is sent to the configured AI service.
- The application does not automatically submit cybercrime complaints.
- API keys must be stored in environment variables or deployment secrets.
- Downloaded reports may contain the original submitted message.

## ⚠️ Disclaimer

ScamShield AI provides educational fraud-awareness guidance. It does not guarantee that a message is fraudulent or legitimate.

For suspected financial cyber fraud in India, contact your bank or payment provider promptly and use official reporting channels.

Official portal: https://cybercrime.gov.in/

## 📜 License

MIT License. See LICENSE for details.
