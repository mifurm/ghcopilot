# Quick Start Guide - Azure AI Integration

## 🚀 Get Started in 5 Minutes

### Step 1: Get Azure Credentials (2 min)

1. Go to [Azure AI Foundry](https://ai.azure.com)
2. Create a project or select existing
3. Deploy a model (gpt-4 or gpt-35-turbo recommended)
4. Copy your:
   - Endpoint URL
   - API Key
   - Deployment Name

### Step 2: Configure Application (1 min)

```bash
# Copy environment template
cp .env.example .env

# Edit the .env file
nano .env  # or: code .env
```

Update these values in `.env`:
```env
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_API_KEY=your-actual-api-key
AZURE_OPENAI_DEPLOYMENT_NAME=your-deployment-name
USE_AZURE_AI=true
```

### Step 3: Install Dependencies (1 min)

```bash
pip install -r requirements.txt
```

### Step 4: Test Configuration (30 sec)

```bash
python test_azure_ai.py
```

Expected output: ✅ All tests passed!

### Step 5: Run the App (30 sec)

```bash
python app.py
```

Open http://localhost:5000 and start chatting! 🎉

---

## 🆘 Need Help?

- **Detailed Setup**: See [AZURE_SETUP.md](AZURE_SETUP.md)
- **Troubleshooting**: Check the troubleshooting section in AZURE_SETUP.md
- **Azure AI Portal**: [https://ai.azure.com](https://ai.azure.com)

## 🎯 What Works Now

With Azure AI configured, your chat bot can:
- ✅ Have natural conversations about trip planning
- ✅ Remember context from previous messages
- ✅ Provide personalized recommendations
- ✅ Suggest kid-friendly activities
- ✅ Give detailed travel advice
- ✅ Answer follow-up questions intelligently

## 💡 Pro Tips

1. **Start Simple**: Use `gpt-35-turbo` for testing (cheaper)
2. **Monitor Costs**: Check Azure Portal regularly
3. **Set Limits**: Configure `AZURE_OPENAI_MAX_TOKENS` in .env
4. **Test First**: Always run `test_azure_ai.py` before deploying

## 🔧 Configuration Options

Customize in `.env`:

```env
# Response creativity (0.0 = focused, 1.0 = creative)
AZURE_OPENAI_TEMPERATURE=0.7

# Maximum response length
AZURE_OPENAI_MAX_TOKENS=1000

# Disable AI for testing
USE_AZURE_AI=false
```

---

**Ready to go?** Run `python app.py` and start planning trips! 🧳✈️
