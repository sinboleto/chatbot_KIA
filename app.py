from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
import os

app = Flask(__name__)

port = int(os.environ.get('PORT', 5000))

# Twilio credentials
account_sid = 'ACf01ddcd618830097852506cba7b428ef'
auth_token = 'a6626c30c4a87f2f44a6df6d483b8d7b'

# twilio_phone_number = '+15416923070'
twilio_phone_number = '+14155238886' # Sandbox

# Create Twilio client
client = Client(account_sid, auth_token)

# Define the route for handling incoming WhatsApp messages
@app.route('/', methods=['GET', 'POST'])
def webhook():
    if request.method == 'POST':
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
            # forward_to_agent(incoming_message)
            pass

        return str(response)
    else:
        return "Hello, this is the root path."

def forward_to_agent(message):
    # Logic to forward the message to a human agent
    # You can use Twilio Notify, send an email, or integrate with a messaging platform to notify the agent
    agent_phone_number = '+525551078511'
    client.messages.create(
        body=message,
        from_=twilio_phone_number,
        to=agent_phone_number
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port)
