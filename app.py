from flask import Flask, render_template, request, jsonify
from datetime import datetime
from dotenv import load_dotenv
import os

# Import Azure AI service
from azure_ai import get_azure_ai_response, get_ai_status

# Import trip extraction utilities
from trip_extractor import extract_trip_details, format_trip_summary

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')

# Store chat messages in memory (in production, use a database)
chat_history = []

@app.route('/')
def index():
    """Render the chat interface"""
    return render_template('chat.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    """Handle chat messages"""
    data = request.get_json()
    user_message = data.get('message', '')
    
    if not user_message:
        return jsonify({'error': 'No message provided'}), 400
    
    # Store user message
    chat_history.append({
        'role': 'user',
        'message': user_message,
        'timestamp': datetime.now().isoformat()
    })
    
    # Generate bot response (simple echo bot for now)
    bot_response = generate_response(user_message)
    
    # Store bot response
    chat_history.append({
        'role': 'bot',
        'message': bot_response,
        'timestamp': datetime.now().isoformat()
    })
    
    return jsonify({
        'response': bot_response,
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/history', methods=['GET'])
def get_history():
    """Get chat history"""
    return jsonify({'history': chat_history})

@app.route('/api/clear', methods=['POST'])
def clear_history():
    """Clear chat history"""
    global chat_history
    chat_history = []
    return jsonify({'status': 'success', 'message': 'Chat history cleared'})

@app.route('/api/ai-status', methods=['GET'])
def ai_status():
    """Get Azure AI configuration status"""
    status = get_ai_status()
    return jsonify(status)

@app.route('/api/extract-details', methods=['POST'])
def extract_details():
    """Extract trip details from a message"""
    data = request.get_json()
    message = data.get('message', '')
    
    if not message:
        return jsonify({'error': 'No message provided'}), 400
    
    # Extract trip details
    details = extract_trip_details(message)
    summary = format_trip_summary(details)
    
    return jsonify({
        'details': details,
        'summary': summary
    })

def generate_response(message):
    """Generate a bot response based on user message using Azure AI"""
    try:
        # Extract trip details from the message
        trip_details = extract_trip_details(message)
        has_trip_info = any([
            trip_details.get('destination'),
            trip_details.get('dates', {}).get('start_date'),
            trip_details.get('travelers', {}).get('total', 0) > 0,
            trip_details.get('duration'),
            len(trip_details.get('children', [])) > 0
        ])
        
        # Convert chat history to format expected by Azure AI
        conversation_history = []
        for msg in chat_history:
            conversation_history.append({
                "role": "assistant" if msg["role"] == "bot" else msg["role"],
                "message": msg["message"]
            })
        
        # Get response from Azure AI service
        response = get_azure_ai_response(message, conversation_history)
        
        # If trip details were extracted, append them to the response
        if has_trip_info:
            trip_summary = format_trip_summary(trip_details)
            response += f"\n\n{trip_summary}"
        
        return response
    
    except Exception as e:
        # Fallback to simple response if Azure AI fails
        print(f"Error generating AI response: {str(e)}")
        return f"I received your message: '{message}'. I'm having trouble connecting to the AI service right now. Please check the Azure AI configuration."

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
