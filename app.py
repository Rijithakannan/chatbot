from flask import Flask, request, jsonify
from flask_cors import CORS

# Initialize Flask app
app = Flask(__name__)
# Enable CORS for the frontend running on a different port/location
CORS(app)

# --- SIMULATED EXTERNAL API FUNCTION ---
def get_weather_data(city):
    """Simulates calling a real external weather API."""
    city = city.lower()
    if "london" in city:
        return f"The current temperature in London is 12°C with light rain."
    elif "tokyo" in city:
        return f"Tokyo is sunny with a temperature of 25°C."
    else:
        return None

# --- CHATBOT API ENDPOINT ---
@app.route('/api/chat', methods=['POST'])
def chat():
    """Receives user message and provides a response."""
    data = request.get_json()
    user_message = data.get('message', '').lower().strip()
    
    response_text = ""
    
    # 1. Intent Recognition and API Integration Logic
    if "weather" in user_message:
        # Extract city (simple logic)
        city = next((word for word in user_message.split() if word in ["london", "tokyo", "mumbai"]), None)
        
        if city:
            # Call the simulated external API
            api_response = get_weather_data(city)
            if api_response:
                response_text = api_response
            else:
                response_text = "Sorry, I don't have weather data for that city."
        else:
            response_text = "Which city's weather are you asking about?"
            
    # 2. General Responses (Fallback)
    elif "hello" in user_message or "hi" in user_message:
        response_text = "Hello! I am your API-integrated chatbot. How can I assist you today?"
    elif "help" in user_message:
        response_text = "I can answer general questions and fetch weather data for major cities like London or Tokyo. Try asking: 'What is the weather in London?'"
    else:
        response_text = "I'm not sure how to respond to that. Try asking about the weather or asking for 'help'."
        
    return jsonify({"response": response_text})

# --- RUN SERVER ---
if __name__ == '__main__':
    # Runs the server on port 5000 (common Flask port)
    app.run(debug=True, port=5000)