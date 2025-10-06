🧳 Family Trip Planner Chat App

A simple Python-based chat application that helps you plan a trip to a specific country, on specific dates, with your wife and children. Built with the help of **GitHub Copilot**.

## ✨ Features

- Chat interface to interact with a trip planning bot
- Extracts destination, travel dates, and family details from user input
- Suggests kid-friendly activities and accommodations
- Stores trip plans locally
- Generates trip summary
- Exports trip plan to PDF or email

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- Flask
- OpenAI API key (optional for GPT integration)

```bash
git clone https://github.com/your-username/family-trip-planner.git
cd family-trip-planner
pip install -r requirements.txt
python app.py
```

Then open your browser and go to http://localhost:5000.

🧠 How GitHub Copilot Helped
This app was built using GitHub Copilot with the following prompt-driven development steps:
- Create a Flask app with a chat interface
- Store user messages and bot responses
- Extract trip details from chat input
- Suggest kid-friendly activities based on destination
- Add calendar picker for travel dates
- Save trip plans to JSON or SQLite
- Recommend family-friendly hotels
- Summarize trip details
- Export trip plan to PDF
- Send trip summary via email

📁 Project Structure
```
family-trip-planner/
│
├── templates/
│   └── chat.html
├── static/
│   └── style.css
├── app.py
├── planner.py
├── utils.py
├── trip_data.json
└── README.md
```

📬 Contact
Created by [Michal Furmankiewicz (Furman)] — Sr Solution Engineer
Feel free to reach out for consulting or GitHub Copilot demos!

[![Open in GitHub Codespaces](https://img.shields.io/badge/Open%20in-GitHub%20Codespaces-blue?logo=github)](https://github.com/codespaces/new?repository=https://github.com/mifurm/ghcopilot)


