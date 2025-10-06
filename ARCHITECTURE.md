# Architecture Overview

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER'S BROWSER                          │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │              chat.html (Frontend UI)                     │  │
│  │  ┌────────────────────────────────────────────────────┐  │  │
│  │  │  Chat Interface                                    │  │  │
│  │  │  - Message input                                   │  │  │
│  │  │  - Chat history display                            │  │  │
│  │  │  - Session indicator                               │  │  │
│  │  │  - Azure AI status badge                           │  │  │
│  │  └────────────────────────────────────────────────────┘  │  │
│  │                                                            │  │
│  │  ┌────────────────────────────────────────────────────┐  │  │
│  │  │  JavaScript Logic                                  │  │  │
│  │  │  - sendMessage()                                   │  │  │
│  │  │  - saveMessageToSession() → localStorage          │  │  │
│  │  │  - loadHistory() ← localStorage                   │  │  │
│  │  │  - checkAzureAIStatus()                           │  │  │
│  │  └────────────────────────────────────────────────────┘  │  │
│  └──────────────────────────────────────────────────────────┘  │
│                              ▲                                  │
│                              │ HTTP/JSON                        │
│                              ▼                                  │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                      FLASK SERVER (app.py)                      │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  API Endpoints                                           │  │
│  │  ┌────────────────┐  ┌──────────────┐  ┌─────────────┐  │  │
│  │  │ POST /api/chat │  │ GET /api/    │  │ GET /api/   │  │  │
│  │  │                │  │   history    │  │   ai-status │  │  │
│  │  └───────┬────────┘  └──────┬───────┘  └──────┬──────┘  │  │
│  │          │                  │                  │         │  │
│  │          ▼                  ▼                  ▼         │  │
│  │  ┌───────────────────────────────────────────────────┐  │  │
│  │  │  Business Logic                                   │  │  │
│  │  │  - generate_response(message)                     │  │  │
│  │  │  - chat_history (in-memory storage)               │  │  │
│  │  │  - Request/Response handling                      │  │  │
│  │  └────────────────────┬──────────────────────────────┘  │  │
│  │                       │                                  │  │
│  │                       ▼                                  │  │
│  │  ┌───────────────────────────────────────────────────┐  │  │
│  │  │  Environment Config (.env)                        │  │  │
│  │  │  - load_dotenv()                                  │  │  │
│  │  │  - SECRET_KEY, Azure credentials                  │  │  │
│  │  └───────────────────────────────────────────────────┘  │  │
│  └──────────────────────────────────────────────────────────┘  │
│                              │                                  │
│                              ▼                                  │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                  AZURE AI MODULE (azure_ai.py)                  │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  AzureAIService Class                                    │  │
│  │  ┌────────────────────────────────────────────────────┐  │  │
│  │  │  __init__()                                        │  │  │
│  │  │  - Load credentials from environment               │  │  │
│  │  │  - Validate configuration                          │  │  │
│  │  │  - Initialize Azure OpenAI client                  │  │  │
│  │  └────────────────────────────────────────────────────┘  │  │
│  │                                                            │  │
│  │  ┌────────────────────────────────────────────────────┐  │  │
│  │  │  generate_chat_response()                          │  │  │
│  │  │  - Build messages with system prompt               │  │  │
│  │  │  - Include conversation history (last 10 msgs)     │  │  │
│  │  │  - Call Azure OpenAI API                           │  │  │
│  │  │  - Handle errors with fallback                     │  │  │
│  │  └────────────────────────────────────────────────────┘  │  │
│  │                                                            │  │
│  │  ┌────────────────────────────────────────────────────┐  │  │
│  │  │  Helper Functions                                  │  │  │
│  │  │  - _validate_credentials()                         │  │  │
│  │  │  - _build_messages()                               │  │  │
│  │  │  - _fallback_response()                            │  │  │
│  │  │  - get_configuration_status()                      │  │  │
│  │  └────────────────────────────────────────────────────┘  │  │
│  └──────────────────────────────────────────────────────────┘  │
│                              │                                  │
│                              ▼                                  │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                      AZURE AI FOUNDRY                           │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  Azure OpenAI Service                                    │  │
│  │  ┌────────────────────────────────────────────────────┐  │  │
│  │  │  Your Deployment                                   │  │  │
│  │  │  - Model: gpt-4 / gpt-35-turbo / gpt-4o          │  │  │
│  │  │  - Endpoint: https://your-resource.openai.azure...│  │  │
│  │  │  - API Key: Protected credential                  │  │  │
│  │  └────────────────────────────────────────────────────┘  │  │
│  │                                                            │  │
│  │  ┌────────────────────────────────────────────────────┐  │  │
│  │  │  Processing                                        │  │  │
│  │  │  1. Receive API request with messages              │  │  │
│  │  │  2. Process with GPT model                         │  │  │
│  │  │  3. Generate contextual response                   │  │  │
│  │  │  4. Return JSON response                           │  │  │
│  │  └────────────────────────────────────────────────────┘  │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                    BROWSER STORAGE (localStorage)               │
│                                                                 │
│  Key: 'family_trip_planner_chat_history'                       │
│  Value: [                                                       │
│    {role: 'user', message: '...', timestamp: '...'},          │
│    {role: 'bot', message: '...', timestamp: '...'},           │
│    ...                                                          │
│  ]                                                              │
│                                                                 │
│  - Persists across page refreshes                              │
│  - Survives browser close/reopen                               │
│  - Cleared manually via "Clear Chat" button                    │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📊 Data Flow Diagram

### User Sends Message:

```
[User types message]
        ↓
[JavaScript captures input]
        ↓
[Save to localStorage] ← Browser storage
        ↓
[POST /api/chat] → Flask app
        ↓
[generate_response()] → azure_ai.py
        ↓
[AzureAIService.generate_chat_response()]
        ↓
[Build message array with history]
        ↓
[Call Azure OpenAI API] → Azure AI Foundry
        ↓
[GPT model processes request]
        ↓
[Generate contextual response] ← AI Magic! 🤖
        ↓
[Return response] → azure_ai.py
        ↓
[Return to Flask] → app.py
        ↓
[Add to chat_history]
        ↓
[JSON response] → Browser
        ↓
[JavaScript displays message]
        ↓
[Save to localStorage] ← Browser storage
        ↓
[Update UI]
```

---

## 🔐 Security Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                   CREDENTIAL MANAGEMENT                     │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  .env.example (Template)         .env (Actual Secrets)     │
│  ✅ Committed to Git              ❌ NEVER commit          │
│  ✅ Placeholder values             ✅ Real credentials      │
│  ✅ Documentation                  ✅ In .gitignore         │
│                                                             │
│                           ↓                                 │
│                    ┌─────────────┐                          │
│                    │  load_dotenv()                         │
│                    └──────┬──────┘                          │
│                           ↓                                 │
│                  Environment Variables                      │
│                  (Runtime only, not in code)                │
│                           ↓                                 │
│            ┌──────────────┴──────────────┐                 │
│            ▼                              ▼                 │
│    Azure OpenAI Client           Flask App Config          │
│    (azure_ai.py)                 (app.py)                  │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 📦 File Structure

```
family-trip-planner/
│
├── 🐍 Python Application
│   ├── app.py                    # Flask server & API endpoints
│   ├── azure_ai.py               # Azure AI Foundry integration
│   └── test_azure_ai.py          # Automated test suite
│
├── 🎨 Frontend
│   ├── templates/
│   │   └── chat.html             # Chat UI with localStorage
│   └── static/
│       └── style.css             # Styling with indicators
│
├── ⚙️ Configuration
│   ├── .env.example              # Template (commit this)
│   ├── .env                      # Your secrets (DO NOT commit)
│   ├── .gitignore                # Protects sensitive files
│   └── requirements.txt          # Python dependencies
│
├── 📚 Documentation
│   ├── README.md                 # Main project README
│   ├── AZURE_SETUP.md            # Detailed setup (20+ pages)
│   ├── QUICKSTART.md             # 5-minute quick start
│   ├── AZURE_AI_SUMMARY.md       # Technical implementation
│   ├── AZURE_INTEGRATION_GUIDE.md # Complete integration guide
│   ├── SESSION_STORAGE.md        # Browser storage docs
│   └── ARCHITECTURE.md           # This file
│
└── 📊 Data (Runtime)
    ├── chat_history              # In-memory (server-side)
    └── localStorage              # Browser-side persistence
```

---

## 🔄 State Management

### Server-Side State (app.py)

```python
chat_history = []  # In-memory list

# Structure:
[
  {
    'role': 'user',
    'message': 'I want to go to Paris',
    'timestamp': '2025-10-06T12:34:56.789Z'
  },
  {
    'role': 'bot',
    'message': 'Paris is wonderful! When are you planning...',
    'timestamp': '2025-10-06T12:34:58.123Z'
  }
]

# Note: Cleared on server restart
# For production: Use database (SQLite, PostgreSQL, etc.)
```

### Client-Side State (localStorage)

```javascript
localStorage.setItem('family_trip_planner_chat_history', JSON.stringify([
  // Same structure as server-side
  // Persists across sessions
  // Survives page refresh
  // User can clear
]))
```

---

## 🌐 API Endpoints

```
┌─────────────────────────────────────────────────────────┐
│  GET /                                                  │
│  → Serves chat.html                                     │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│  POST /api/chat                                         │
│  Body: { "message": "user message" }                    │
│  Response: { "response": "bot message", "timestamp": ...}│
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│  GET /api/history                                       │
│  Response: { "history": [ {role, message, timestamp} ]}│
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│  POST /api/clear                                        │
│  Response: { "status": "success", "message": "..." }    │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│  GET /api/ai-status                                     │
│  Response: {                                            │
│    "configured": true/false,                            │
│    "use_azure_ai": true/false,                          │
│    "deployment_name": "...",                            │
│    ...                                                  │
│  }                                                      │
└─────────────────────────────────────────────────────────┘
```

---

## 🧪 Testing Architecture

```
┌──────────────────────────────────────────────────────┐
│           test_azure_ai.py Test Suite                │
├──────────────────────────────────────────────────────┤
│                                                      │
│  ┌────────────────────────────────────────────┐    │
│  │  Test 1: Configuration Status              │    │
│  │  - Check environment variables             │    │
│  │  - Validate credentials                    │    │
│  │  - Verify client initialization            │    │
│  └────────────────────────────────────────────┘    │
│                     ↓                               │
│  ┌────────────────────────────────────────────┐    │
│  │  Test 2: Simple Response                   │    │
│  │  - Send basic greeting                     │    │
│  │  - Verify AI responds                      │    │
│  │  - Check response quality                  │    │
│  └────────────────────────────────────────────┘    │
│                     ↓                               │
│  ┌────────────────────────────────────────────┐    │
│  │  Test 3: Trip Planning Context             │    │
│  │  - Send trip-specific query                │    │
│  │  - Verify contextual response              │    │
│  │  - Check for relevant keywords             │    │
│  └────────────────────────────────────────────┘    │
│                     ↓                               │
│  ┌────────────────────────────────────────────┐    │
│  │  Test 4: Conversation Memory               │    │
│  │  - Simulate multi-turn conversation        │    │
│  │  - Verify context retention                │    │
│  │  - Check coherent responses                │    │
│  └────────────────────────────────────────────┘    │
│                     ↓                               │
│  ┌────────────────────────────────────────────┐    │
│  │  Summary Report                            │    │
│  │  - Count passed/failed                     │    │
│  │  - Display results                         │    │
│  │  - Exit with status code                   │    │
│  └────────────────────────────────────────────┘    │
└──────────────────────────────────────────────────────┘
```

---

## 💾 Persistence Strategy

### Current (Development)

```
┌──────────────┐       ┌──────────────┐
│   Browser    │       │    Flask     │
│  localStorage│       │  In-Memory   │
│              │       │  chat_history│
│  ✅ Persists │       │  ❌ Lost on  │
│    across    │       │    restart   │
│   sessions   │       │              │
└──────────────┘       └──────────────┘
```

### Future (Production)

```
┌──────────────┐       ┌──────────────┐       ┌──────────────┐
│   Browser    │       │    Flask     │       │   Database   │
│  localStorage│  ←→   │   App.py     │  ←→   │  PostgreSQL  │
│              │       │              │       │   / SQLite   │
│  Fast local  │       │  Business    │       │  Persistent  │
│   access     │       │    Logic     │       │   Storage    │
└──────────────┘       └──────────────┘       └──────────────┘
```

---

## 🔌 Integration Points

### Azure AI Foundry

```
Configuration:
  - Endpoint URL
  - API Key (secured in .env)
  - API Version
  - Deployment Name

Communication:
  - REST API (HTTPS)
  - JSON payloads
  - OAuth 2.0 / API Key auth

Request/Response:
  Request: { model, messages[], temperature, max_tokens }
  Response: { choices[].message.content }
```

### Browser Integration

```
JavaScript → Python:
  - Fetch API (HTTP requests)
  - JSON serialization
  - Error handling

Python → JavaScript:
  - JSON responses
  - HTTP status codes
  - Error messages

Browser Storage:
  - localStorage API
  - JSON serialization
  - 5-10MB limit
```

---

## 🚀 Scalability Considerations

### Current Architecture (Single Instance)

```
Browser ←→ Flask (single process) ←→ Azure AI
        ↓
   localStorage
```

**Limitations:**
- One Flask process
- In-memory state (lost on restart)
- No load balancing

### Production Architecture (Scalable)

```
                    ┌──→ Flask Instance 1 ──┐
Browsers ←→ Load    ├──→ Flask Instance 2 ──┼──→ Azure AI
         Balancer   └──→ Flask Instance N ──┘
                              ↓
                         Database
                    (Shared session store)
```

**Benefits:**
- Multiple Flask instances
- Shared database state
- Horizontal scaling
- High availability

---

## 📊 Monitoring & Observability

### Application Level

```
Python Logging (azure_ai.py):
  - Info: Successful operations
  - Warning: Config issues
  - Error: API failures

Flask Logging (app.py):
  - Request/response logs
  - Error tracking
  - Performance metrics
```

### Azure Level

```
Azure Portal:
  - Token usage metrics
  - Request counts
  - Latency statistics
  - Error rates
  - Cost tracking
```

### Client Level

```
Browser Console:
  - JavaScript errors
  - Network requests
  - localStorage operations
  - Performance timing
```

---

## 🎯 Key Design Decisions

### 1. Environment Variables (.env)
**Why?** Secure credential management, easy configuration per environment

### 2. Singleton Pattern (azure_ai.py)
**Why?** Efficient resource usage, single client instance

### 3. In-Memory Storage (app.py)
**Why?** Simple for development, easy to replace with database

### 4. localStorage (chat.html)
**Why?** Client-side persistence, no server dependency

### 5. Fallback Responses (azure_ai.py)
**Why?** Graceful degradation, always functional

### 6. Conversation History Limit (10 messages)
**Why?** Balance context vs. token cost

---

**Architecture Version**: 1.0.0  
**Last Updated**: October 2025  
**Author**: Michal Furmankiewicz (Furman)
