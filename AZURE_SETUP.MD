# Azure AI Foundry Setup Guide

## 🚀 Complete Setup Instructions for Azure AI Integration

This guide will walk you through setting up Azure AI Foundry (Azure OpenAI) for the Family Trip Planner Chat App.

---

## 📋 Prerequisites

1. **Azure Account**: You need an active Azure subscription
   - Sign up at [https://azure.microsoft.com/free/](https://azure.microsoft.com/free/)
   
2. **Access to Azure OpenAI Service**
   - Azure OpenAI requires approval: [Apply here](https://aka.ms/oai/access)
   - Or use Azure AI Foundry which may have different requirements

---

## 🔧 Step 1: Create Azure OpenAI Resource

### Option A: Using Azure Portal

1. **Go to Azure Portal**: [https://portal.azure.com](https://portal.azure.com)

2. **Create a new resource**:
   - Click "+ Create a resource"
   - Search for "Azure OpenAI" or "Azure AI Services"
   - Click "Create"

3. **Configure the resource**:
   - **Subscription**: Select your Azure subscription
   - **Resource Group**: Create new or use existing
   - **Region**: Choose a region (e.g., East US, West Europe)
   - **Name**: Give it a unique name (e.g., `family-trip-planner-ai`)
   - **Pricing Tier**: Select Standard S0

4. **Review and Create**: Click "Review + Create", then "Create"

5. **Wait for deployment**: This takes 1-2 minutes

### Option B: Using Azure AI Foundry

1. **Go to Azure AI Foundry**: [https://ai.azure.com](https://ai.azure.com)

2. **Create a new project**:
   - Click "New project"
   - Give it a name and select region
   - This will automatically create necessary resources

3. **Deploy a model** (see Step 2)

---

## 🤖 Step 2: Deploy a Model

1. **Navigate to Azure AI Foundry** or **Azure OpenAI Studio**:
   - Azure AI Foundry: [https://ai.azure.com](https://ai.azure.com)
   - Or Azure OpenAI Studio: [https://oai.azure.com](https://oai.azure.com)

2. **Select your resource** from the list

3. **Deploy a model**:
   - Click "Deployments" in the left menu
   - Click "+ Create new deployment" or "+ Deploy model"
   
4. **Choose a model**:
   - **Recommended for chat**: 
     - `gpt-4` (best quality, higher cost)
     - `gpt-4o` (optimized, good balance)
     - `gpt-35-turbo` (faster, lower cost)
   
5. **Configure deployment**:
   - **Deployment name**: Choose a name (e.g., `gpt-4-trip-planner`)
   - **Model version**: Select latest available
   - **Deployment type**: Standard
   - Click "Create"

6. **Note down the deployment name** - you'll need this!

---

## 🔑 Step 3: Get Your Credentials

### Get Endpoint and API Key

1. **In Azure Portal**:
   - Go to your Azure OpenAI resource
   - Click "Keys and Endpoint" in the left menu
   - Copy:
     - **Endpoint** (e.g., `https://your-resource.openai.azure.com/`)
     - **KEY 1** (your API key)

2. **In Azure AI Foundry**:
   - Go to your project
   - Click on "Settings" or "Keys and endpoints"
   - Copy the endpoint and key

---

## ⚙️ Step 4: Configure Your Application

1. **Navigate to your project directory**:
   ```bash
   cd /workspaces/ghcopilot
   ```

2. **Copy the example environment file**:
   ```bash
   cp .env.example .env
   ```

3. **Edit the `.env` file**:
   ```bash
   nano .env
   # or use VS Code: code .env
   ```

4. **Fill in your Azure credentials**:
   ```env
   # Replace these with your actual values
   AZURE_OPENAI_ENDPOINT=https://your-resource-name.openai.azure.com/
   AZURE_OPENAI_API_KEY=your-actual-api-key-here
   AZURE_OPENAI_API_VERSION=2024-08-01-preview
   AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4-trip-planner
   AZURE_OPENAI_MODEL_NAME=gpt-4
   AZURE_OPENAI_TEMPERATURE=0.7
   AZURE_OPENAI_MAX_TOKENS=1000
   USE_AZURE_AI=true
   ```

5. **Save the file**

---

## 📦 Step 5: Install Dependencies

```bash
# Install required Python packages
pip install -r requirements.txt
```

The requirements include:
- `openai==1.52.0` - Azure OpenAI SDK
- `python-dotenv==1.0.0` - Environment variable management
- `azure-identity==1.18.0` - Azure authentication

---

## 🧪 Step 6: Test Your Setup

### Option 1: Check AI Status via API

1. **Start the Flask app**:
   ```bash
   python app.py
   ```

2. **Test the AI status endpoint**:
   ```bash
   curl http://localhost:5000/api/ai-status
   ```

   Expected response:
   ```json
   {
     "configured": true,
     "use_azure_ai": true,
     "endpoint_set": true,
     "api_key_set": true,
     "deployment_name": "gpt-4-trip-planner",
     "model_name": "gpt-4",
     "client_initialized": true
   }
   ```

### Option 2: Test via Chat Interface

1. **Open your browser**: http://localhost:5000

2. **Send a test message**: "Hello, I want to plan a trip to Paris"

3. **Verify AI response**: 
   - Should receive a personalized, detailed response
   - Not a generic keyword-based response

### Option 3: Test with Python Script

Create a test file `test_azure_ai.py`:

```python
from azure_ai import get_azure_ai_response, get_ai_status

# Check status
status = get_ai_status()
print("Azure AI Status:", status)

if status['configured']:
    # Test response
    response = get_azure_ai_response("Hello, I want to plan a family trip to Tokyo")
    print("\nAI Response:", response)
else:
    print("\nAzure AI is not properly configured.")
    print("Please check your .env file.")
```

Run it:
```bash
python test_azure_ai.py
```

---

## 🔒 Security Best Practices

### 1. Protect Your .env File

Add to `.gitignore`:
```bash
echo ".env" >> .gitignore
```

### 2. Never Commit Secrets

- ❌ Never commit `.env` file to Git
- ✅ Only commit `.env.example` with placeholder values
- ✅ Share credentials securely (e.g., Azure Key Vault, password manager)

### 3. Rotate Keys Regularly

- Regenerate API keys periodically in Azure Portal
- Update `.env` file after rotation

### 4. Use Azure Key Vault (Production)

For production deployments:
```python
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

credential = DefaultAzureCredential()
client = SecretClient(vault_url="https://your-vault.vault.azure.net/", credential=credential)
api_key = client.get_secret("azure-openai-key").value
```

---

## 💰 Cost Management

### Understand Pricing

Azure OpenAI pricing is based on tokens:
- **gpt-4**: ~$0.03 per 1K input tokens, ~$0.06 per 1K output tokens
- **gpt-4o**: ~$0.005 per 1K input tokens, ~$0.015 per 1K output tokens  
- **gpt-35-turbo**: ~$0.0005 per 1K input tokens, ~$0.0015 per 1K output tokens

**Approximate conversation costs**:
- Simple chat (200 tokens): $0.001 - $0.012
- Detailed response (1000 tokens): $0.005 - $0.06

### Monitor Usage

1. **Azure Portal**:
   - Go to your Azure OpenAI resource
   - Click "Metrics" to view usage

2. **Set Budget Alerts**:
   - Go to "Cost Management"
   - Create budget alerts

3. **Control Costs in Code**:
   ```python
   # In .env file
   AZURE_OPENAI_MAX_TOKENS=500  # Limit response length
   AZURE_OPENAI_TEMPERATURE=0.5  # More deterministic = potentially fewer retries
   ```

---

## 🐛 Troubleshooting

### Issue 1: "Authentication Failed"

**Problem**: API key is invalid or expired

**Solution**:
1. Verify API key in Azure Portal (Keys and Endpoint)
2. Make sure you copied the entire key
3. Check for extra spaces in `.env` file
4. Try regenerating the key

### Issue 2: "Resource Not Found"

**Problem**: Endpoint URL is incorrect

**Solution**:
1. Verify endpoint in Azure Portal
2. Must be in format: `https://your-resource.openai.azure.com/`
3. Include trailing slash
4. Don't include `/openai/` in the path

### Issue 3: "Deployment Not Found"

**Problem**: Deployment name doesn't match

**Solution**:
1. Check deployment name in Azure AI Foundry/Studio
2. Must match exactly (case-sensitive)
3. Verify deployment is in "Succeeded" state

### Issue 4: "Rate Limit Exceeded"

**Problem**: Too many requests

**Solution**:
1. Implement rate limiting in your app
2. Add retry logic with exponential backoff
3. Upgrade to higher pricing tier
4. Request quota increase in Azure Portal

### Issue 5: "Client Not Initialized"

**Problem**: Azure AI client failed to initialize

**Solution**:
1. Check all credentials are set
2. Run: `python -c "from azure_ai import get_ai_status; print(get_ai_status())"`
3. Verify no placeholders like `your-api-key-here`
4. Check Python package versions: `pip list | grep openai`

---

## 📚 Additional Resources

### Documentation
- [Azure OpenAI Documentation](https://learn.microsoft.com/azure/ai-services/openai/)
- [Azure AI Foundry Documentation](https://learn.microsoft.com/azure/ai-studio/)
- [OpenAI Python SDK](https://github.com/openai/openai-python)

### Azure AI Foundry
- [Azure AI Foundry Portal](https://ai.azure.com)
- [Model Catalog](https://ai.azure.com/explore/models)
- [Pricing Calculator](https://azure.microsoft.com/pricing/calculator/)

### Community
- [Azure AI Discord](https://discord.gg/azure)
- [Microsoft Q&A](https://learn.microsoft.com/answers/)
- [Stack Overflow - azure-openai](https://stackoverflow.com/questions/tagged/azure-openai)

---

## ✅ Quick Checklist

Before going live, verify:

- [ ] Azure OpenAI resource created
- [ ] Model deployed successfully
- [ ] Endpoint and API key copied to `.env`
- [ ] Deployment name matches exactly
- [ ] `.env` file added to `.gitignore`
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] AI status endpoint returns `"configured": true`
- [ ] Chat responses are AI-generated (not fallback)
- [ ] Budget alerts configured in Azure
- [ ] Keys stored securely (not in code)

---

## 🎉 Success!

If everything is configured correctly:
- Your chat app will use Azure AI for intelligent responses
- Responses will be contextual and helpful for trip planning
- The app will gracefully fall back if Azure AI is unavailable

**Need help?** Check the troubleshooting section or create an issue in the repository.

---

**Last Updated**: October 2025  
**Maintained by**: Michal Furmankiewicz (Furman) - Sr Solution Engineer