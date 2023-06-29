from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client

app = Flask(__name__)

# Twilio credentials
account_sid = 'YOUR_ACCOUNT_SID'
auth_token = 'YOUR_AUTH_TOKEN'
twilio_phone_number = 'YOUR_TWILIO_PHONE_NUMBER'

# Create Twilio client
client = Client(account_sid, auth_token)

# Define the route for handling incoming WhatsApp messages
@app.route('/')
def start():
    return 'App conectada'

@app.route('/webhook', methods=['POST'])
def webhook():
    incoming_message = request.values.get('Body', '').lower()
    response = MessagingResponse()

    # Check if the incoming message is a frequently asked question
    if incoming_message == 'hi':
        response.message("Hello! How can I assist you today?")
    elif incoming_message == 'how are you?':
        response.message("I'm a chatbot. I don't have feelings, but thanks for asking!")
    elif incoming_message == 'what is your name?':
        response.message("I'm a chatbot. You can call me ChatGPT!")

    # If it's not a frequently asked question, escalate the conversation to a human agent
    else:
        forward_to_agent(incoming_message)

    return str(response)

def forward_to_agent(message):
    # Logic to forward the message to a human agent
    # You can use Twilio Notify, send an email, or integrate with a messaging platform to notify the agent
    agent_phone_number = 'AGENT_PHONE_NUMBER'
    client.messages.create(
        body=message,
        from_=twilio_phone_number,
        to=agent_phone_number
    )

if __name__ == '__main__':
    app.run()
