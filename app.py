from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
from dotenv import load_dotenv
import os
from unidecode import unidecode

app = Flask(__name__)

port = int(os.environ.get('PORT', 5000))

# Load environment variables from .env file
load_dotenv()

# Twilio credentials
account_sid = os.environ.get('ACCOUNT_SID')
auth_token = os.environ.get('AUTH_TOKEN')
twilio_phone_number = os.environ.get('TWILIO_PHONE_NUMBER')

# Create Twilio client
client = Client(account_sid, auth_token)

# Define the route for handling incoming WhatsApp messages
@app.route('/', methods=['GET', 'POST'])
def webhook():
    if request.method == 'POST':
        incoming_message = unidecode(request.values.get('Body', '').lower())
        response = MessagingResponse()

        lista_saludo = ['hola','buenos dias','buenas tardes','buenas noches']
        lista_FAQ_1 = ['cuando','fecha','hora','donde','direccion','duracion']
        lista_FAQ_2 = ['hospedaje']
        lista_FAQ_3 = ['estacionamiento','valet parking']
        lista_FAQ_4 = ['dress code','codigo vestimenta','vestimenta']
        lista_FAQ_5 = ['agenda']

        # Check if the incoming message is a frequently asked question
        if incoming_message in lista_saludo:
            response.message("Hola ¿Cómo te puedo ayudar?")
        
        elif incoming_message in lista_FAQ_1:
            respuesta_FAQ_1 = """Esta es la información general del evento:
            Fecha: 08 de agosto de 2023
            Cita: 19:00 hrs
            Venue: Foro Codere
            Dirección: Av. Industria Militar s/n esq. Periférico. Col. Lomas de Sotelo,
            Del. Miguel Hidalgo. Link: https://goo.gl/maps/AiDZWCWrWLwViW817
            Acceso a estacionamiento y a venue por puerta 1 y 2 del Hipódromo de las Américas"""
            response.message(respuesta_FAQ_1)
        
        elif incoming_message in lista_FAQ_2:
            respuesta_FAQ_2 = """Contamos con alizanza con el hotel Hyatt Regency Mexico City Insurgentes.
            Link: https://goo.gl/maps/HCqTAzWbhSrvB58NA.
            Para reservaciones contactar a: asistente@amdk.mx.
            Habrá transportación del hotel a Foro Codere"""
            response.message(respuesta_FAQ_2)
        
        elif incoming_message in lista_FAQ_3:
            respuesta_FAQ_3 = """El venue cuenta con estacionamiento privado y servicio de valet parking"""
            response.message(respuesta_FAQ_3)
        
        elif incoming_message in lista_FAQ_4:
            respuesta_FAQ_4 = """El dress code es smart business. Te proponemos algunas opciones:
            - Combinación de prendas
            - Camisas lisas, corbata opcional
            - Tejidos como la lana, el tweed y el algodón
            - Blazers con falda, vestidos por la rodilla, camisas lisas o pantalones de sastre
            - Joyas sencillas y lisas, si se llevan
            - Cinturones y zapatos cerrados pulidos
            - Maletines, bolsos de mano o elegantes
            La paleta de colores suele ser de tonos neutros como el negro, el azul marino, el gris, el beige y el crema"""
            response.message(respuesta_FAQ_4)

        elif incoming_message in lista_FAQ_5:
            respuesta_FAQ_5 = """El itinerario del evento será el siguiente:
            19:00 - Registro
            20:00 - Bienvenida
            20:15 - Presentación
            21:15 - Cena"""
            response.message(respuesta_FAQ_5)

        # If it's not a frequently asked question, escalate the conversation to a human agent
        else:
            # forward_to_agent(incoming_message)
            response.message("""Para responder a su pregunta a continuación, un asesor lo atenderá por este medio. 
            Gracias por su paciencia""")
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
