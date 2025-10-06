"""
Azure AI Foundry Integration Module
Handles communication with Azure OpenAI services for the Family Trip Planner
"""

import os
import logging
from typing import List, Dict, Optional
from openai import AzureOpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AzureAIService:
    """Service class for Azure AI Foundry / Azure OpenAI integration"""
    
    def __init__(self):
        """Initialize Azure OpenAI client with credentials from environment"""
        self.endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
        self.api_key = os.getenv("AZURE_OPENAI_API_KEY")
        self.api_version = os.getenv("AZURE_OPENAI_API_VERSION", "2024-08-01-preview")
        self.deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")
        self.model_name = os.getenv("AZURE_OPENAI_MODEL_NAME", "gpt-4")
        self.temperature = float(os.getenv("AZURE_OPENAI_TEMPERATURE", "0.7"))
        self.max_tokens = int(os.getenv("AZURE_OPENAI_MAX_TOKENS", "1000"))
        self.use_azure_ai = os.getenv("USE_AZURE_AI", "true").lower() == "true"
        
        # Initialize client if credentials are available
        self.client = None
        if self._validate_credentials():
            try:
                # Initialize Azure OpenAI client with minimal parameters
                self.client = AzureOpenAI(
                    api_key=self.api_key,
                    api_version=self.api_version,
                    azure_endpoint=self.endpoint,
                    max_retries=2,
                    timeout=30.0
                )
                logger.info(f"Azure AI client initialized successfully with deployment: {self.deployment_name}")
            except TypeError as e:
                # Handle version compatibility issues
                logger.warning(f"Trying alternative client initialization due to: {str(e)}")
                try:
                    self.client = AzureOpenAI(
                        api_key=self.api_key,
                        api_version=self.api_version,
                        azure_endpoint=self.endpoint
                    )
                    logger.info(f"Azure AI client initialized successfully (alternative method)")
                except Exception as e2:
                    logger.error(f"Failed to initialize Azure AI client: {str(e2)}")
                    self.client = None
            except Exception as e:
                logger.error(f"Failed to initialize Azure AI client: {str(e)}")
                self.client = None
        else:
            logger.warning("Azure AI credentials not configured. Using fallback responses.")
    
    def _validate_credentials(self) -> bool:
        """Validate that required credentials are present"""
        if not self.use_azure_ai:
            return False
        
        required_vars = [
            ("AZURE_OPENAI_ENDPOINT", self.endpoint),
            ("AZURE_OPENAI_API_KEY", self.api_key),
            ("AZURE_OPENAI_DEPLOYMENT_NAME", self.deployment_name)
        ]
        
        missing = [name for name, value in required_vars if not value or value.startswith("your-")]
        
        if missing:
            logger.warning(f"Missing or placeholder Azure AI credentials: {', '.join(missing)}")
            return False
        
        return True
    
    def generate_chat_response(
        self,
        user_message: str,
        conversation_history: Optional[List[Dict[str, str]]] = None
    ) -> str:
        """
        Generate a chat response using Azure OpenAI
        
        Args:
            user_message: The user's message
            conversation_history: Previous conversation messages (optional)
        
        Returns:
            Generated response string
        """
        if not self.client:
            return self._fallback_response(user_message)
        
        try:
            # Build messages for the API call
            messages = self._build_messages(user_message, conversation_history)
            
            # Call Azure OpenAI
            response = self.client.chat.completions.create(
                model=self.deployment_name,
                messages=messages,
                temperature=self.temperature,
                max_tokens=self.max_tokens,
                top_p=0.95,
                frequency_penalty=0,
                presence_penalty=0
            )
            
            # Extract and return the response
            assistant_message = response.choices[0].message.content
            logger.info(f"Generated response with {len(assistant_message)} characters")
            
            return assistant_message
        
        except Exception as e:
            logger.error(f"Error calling Azure OpenAI: {str(e)}")
            return self._fallback_response(user_message)
    
    def _build_messages(
        self,
        user_message: str,
        conversation_history: Optional[List[Dict[str, str]]] = None
    ) -> List[Dict[str, str]]:
        """Build the messages array for the API call"""
        
        # System message to set the context
        system_message = {
            "role": "system",
            "content": """You are a helpful and enthusiastic Family Trip Planner assistant. 
Your goal is to help families plan amazing vacations, especially with children.

You should:
- Be warm, friendly, and encouraging
- Ask clarifying questions about destination, dates, and family composition
- Suggest kid-friendly activities and attractions
- Recommend family-friendly accommodations
- Consider safety, convenience, and fun for all ages
- Provide practical tips for traveling with children
- Be concise but informative

Remember to gather key information:
1. Destination (country/city)
2. Travel dates
3. Number of adults and children (with ages)
4. Interests and preferences
5. Budget considerations
"""
        }
        
        messages = [system_message]
        
        # Add conversation history if available
        if conversation_history:
            for msg in conversation_history[-10:]:  # Keep last 10 messages for context
                if msg.get("role") in ["user", "assistant"]:
                    messages.append({
                        "role": msg["role"],
                        "content": msg["message"]
                    })
        
        # Add current user message
        messages.append({
            "role": "user",
            "content": user_message
        })
        
        return messages
    
    def _fallback_response(self, message: str) -> str:
        """Generate a simple fallback response when Azure AI is unavailable"""
        message_lower = message.lower()
        
        # Simple keyword-based responses
        if any(word in message_lower for word in ['hello', 'hi', 'hey']):
            return "Hello! I'm your Family Trip Planner assistant. How can I help you plan your trip today? (Note: Azure AI is currently not configured. Please set up your Azure credentials for enhanced responses.)"
        
        elif 'help' in message_lower:
            return "I can help you plan a family trip! Tell me about your destination, travel dates, and who's traveling with you. (Note: For better assistance, please configure Azure AI credentials.)"
        
        elif any(word in message_lower for word in ['bye', 'goodbye']):
            return "Goodbye! Have a great trip! Don't forget to configure Azure AI for enhanced trip planning assistance."
        
        elif any(word in message_lower for word in ['destination', 'where', 'country', 'city']):
            return "Great! What destination are you considering? I can help you plan activities and find accommodations. (Azure AI integration will provide more detailed recommendations once configured.)"
        
        elif any(word in message_lower for word in ['date', 'when', 'travel']):
            return "When are you planning to travel? Having specific dates helps with planning activities and booking accommodations. (Configure Azure AI for personalized suggestions.)"
        
        elif any(word in message_lower for word in ['child', 'kid', 'family']):
            return "Tell me more about your family! How many children and their ages? This helps me suggest age-appropriate activities. (Enhanced suggestions available with Azure AI integration.)"
        
        else:
            return f"I received your message about: '{message}'. I'm currently running in basic mode. Please configure Azure OpenAI credentials in the .env file for AI-powered trip planning assistance!"
    
    def is_configured(self) -> bool:
        """Check if Azure AI is properly configured"""
        return self.client is not None and self.use_azure_ai
    
    def get_configuration_status(self) -> Dict[str, any]:
        """Get the current configuration status"""
        return {
            "configured": self.is_configured(),
            "use_azure_ai": self.use_azure_ai,
            "endpoint_set": bool(self.endpoint and not self.endpoint.startswith("your-")),
            "api_key_set": bool(self.api_key and not self.api_key.startswith("your-")),
            "deployment_name": self.deployment_name if self.is_configured() else "not configured",
            "model_name": self.model_name,
            "client_initialized": self.client is not None
        }


# Create a singleton instance
azure_ai_service = AzureAIService()


def get_azure_ai_response(
    user_message: str,
    conversation_history: Optional[List[Dict[str, str]]] = None
) -> str:
    """
    Convenience function to get a response from Azure AI
    
    Args:
        user_message: The user's message
        conversation_history: Previous conversation messages (optional)
    
    Returns:
        Generated response string
    """
    return azure_ai_service.generate_chat_response(user_message, conversation_history)


def get_ai_status() -> Dict[str, any]:
    """Get the current AI service configuration status"""
    return azure_ai_service.get_configuration_status()
