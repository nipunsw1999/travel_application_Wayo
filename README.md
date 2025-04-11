# 🌍 Wayo – Travel Recommendation using AI

**Way + Go = Wayo**  
An AI-powered assistant for planning your next travel adventure.

> 🚀 Powered by [H2O Wave](https://h2o.ai/products/h2o-wave/)

---

## ✨ Features

- Ask travel questions and get smart answers
- Plan your trip with AI-generated recommendations
- Meal planning support for travelers
- Works with multiple AI providers (OpenAI, Gemini)
- Available in two versions: Streamlit prototype and H2O Wave production UI

---

## 🌐 Live Demo

👉 Try the deployed prototype version on Streamlit:  
**[wayotravel.streamlit.app](https://wayotravel.streamlit.app)**

---

## 📦 Installation

Clone the repository:
```bash
git clone https://github.com/nipunsw1999/travel_application_Wayo.git
cd travel_application_Wayo
🔧 Set up Virtual Environment
On Linux/macOS:

bash
Copy
python3 -m venv venv
source venv/bin/activate
On Windows:

bash
Copy
python -m venv venv
venv\Scripts\activate
📥 Install Dependencies

bash
Copy
pip install -r requirements.txt
🔐 Environment Variables
Create a .env file in the root directory and add the following API keys:

env
Copy
OPENAI_API_KEY=
GOOGLE_API_KEY=
GOOGLE_SEARCH_ENGINE_ID=
GEMINI_API_KEY=
You can get the keys from:

OpenAI

Google Programmable Search

Google AI Studio (Gemini)

🚀 Running the App

▶️ Run Streamlit Version (Prototype)

bash
Copy
streamlit run streamlit_app.py
💡 Run H2O Wave Version (Production)
Make sure H2O Wave is installed and running.

bash
Copy
wave run wave_app.py
🧠 Powered by

OpenAI GPT

Gemini Pro (Google AI)

Google Search API

H2O Wave Framework
