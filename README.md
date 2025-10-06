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
- Azure OpenAI / Azure AI Foundry account and API key
- See [AZURE_SETUP.md](AZURE_SETUP.md) for detailed setup instructions

```bash
git clone https://github.com/your-username/family-trip-planner.git
cd family-trip-planner

# Install dependencies
pip install -r requirements.txt

# Configure Azure AI (IMPORTANT!)
cp .env.example .env
# Edit .env and add your Azure OpenAI credentials
# See AZURE_SETUP.md for detailed instructions

# Run the app
python app.py
```

Then open your browser and go to http://localhost:5000.

**⚠️ Important**: Configure your Azure AI credentials in `.env` before running. See [AZURE_SETUP.md](AZURE_SETUP.md) for complete setup instructions.

🧠 How GitHub Copilot Helped
This app was built using GitHub Copilot with the following prompt-driven development steps:
- Set up a basic Flask app with a chat interface.
_"Create a Flask web app with a simple HTML form to send and receive chat messages."_
- Make sure you will add the LLM integration using the model from Azure AI Foundry
_"Make sure you will add the LLM integration using the model from Azure AI Foundry also adding respective env file"_
- Store user input in a session or temporary memory.
_"Add session support to store user messages and bot responses."_
- Create a function to parse trip details from user input.
_"Write a function that extracts destination, travel dates, and number of travelers from a message."_
- Integrate OpenAI or local NLP model for chatbot responses.
_"Connect the chat input to an OpenAI GPT model to generate travel planning responses."_
- Add JSON files with potential flights, hotels and fun activites. Later on I will put them in the database. I need them for testing purposes.
_"Add JSON files with potential flights, hotels and fun activites. Later on I will put them in the database."_
- Add logic to suggest kid-friendly activities in the destination.
_"Based on the destination, suggest activities suitable for children."_
- Include a calendar picker for selecting travel dates.
_"Add a date picker to the chat interface for selecting start and end dates."_
- Store trip plans in a local JSON file or SQLite database.
_"Save trip details and chat history to a local database for future reference."_
- Add a feature to recommend hotels or accommodations.
_"Create a function that recommends family-friendly hotels in the selected destination."_
- Implement a summary view of the planned trip.
_"Generate a summary of the trip including dates, destination, activities, and accommodations."_
- Enable export of trip plan to PDF or email.
_"Add functionality to export the trip summary to a PDF or send it via email."_
- Explain to me the whole code showing key things
_"Explain to me the whole code showing key things"_
- Draw a diagram using markdown to present the architecture of the solution
_"Draw a diagram using markdown to present the architecture of the solution"_
- Add a Dockerfile to repo
_"Add a Dockerfile to repo"_
- Create a Bicep file to create a simple infrastructure in Azure to host the app and deploy it using a container
_"Create a Bicep file to create a simple infrastructure in Azure to host the app and deploy it using a container"

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


