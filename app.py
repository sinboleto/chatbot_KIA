from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
from dotenv import load_dotenv
import os
from unidecode import unidecode
import re
from itertools import combinations

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
        # Convierte a minusculas, sin acentos y sin caracteres especiales
        incoming_message = re.sub(r'\W+', ' ',unidecode(request.values.get('Body', '').lower().strip()))
        response = MessagingResponse()

        bienvenida = 'Bienvenido al chatbot del evento del octavo aniversario de KIA. Escribe "hola" para comenzar'

        lista_saludo = ['hola','buenos dias','buenas tardes','buenas noches']
        lista_FAQ_1 = ['cuando','fecha','hora','donde','lugar','venue','salon','direccion','duracion']
        lista_FAQ_2 = ['hospedaje','hotel','hoteles','alojamiento']
        lista_FAQ_3 = ['estacionamiento','valet parking','estacionarse','estacionar','dejar coche']
        lista_FAQ_4 = ['dress code','codigo vestimenta','vestimenta','vestirse']
        lista_FAQ_5 = ['agenda','itinerario']
        lista_despedida = ['adios','hasta luego']

        # Check if the incoming message is a frequently asked question
        if bienvenida == incoming_message or compare_sentence_with_list(incoming_message, lista_saludo):
            response.message("Hola ¿Cómo te puedo ayudar?\nSoy un chatbot y estoy programado para responder dudas sobre la información general del evento, recomendaciones de hospedaje, dress code y agenda del evento. Cualquier otra duda, un asesor lo atenderá por este medio")
        
        elif compare_sentence_with_list(incoming_message, lista_FAQ_1):
            respuesta_FAQ_1 = """Esta es la información general del evento:\nFecha: 08 de agosto de 2023\nCita: 19:00 hrs\nVenue: Foro Codere\nDirección: Av. Industria Militar s/n esq. Periférico. Col. Lomas de Sotelo, Del. Miguel Hidalgo.\nLink: https://goo.gl/maps/AiDZWCWrWLwViW817\nAcceso a estacionamiento y a venue por puerta 1 y 2 del Hipódromo de las Américas"""
            response.message(respuesta_FAQ_1)
        
        elif compare_sentence_with_list(incoming_message, lista_FAQ_2):
            respuesta_FAQ_2 = """Contamos con alizanza con el hotel Hyatt Regency Mexico City Insurgentes.\nLink: https://goo.gl/maps/HCqTAzWbhSrvB58NA.\nPara reservaciones contactar a: asistente@amdk.mx.\nHabrá transportación del hotel a Foro Codere"""
            response.message(respuesta_FAQ_2)
        
        elif compare_sentence_with_list(incoming_message, lista_FAQ_3):
            respuesta_FAQ_3 = """El venue cuenta con estacionamiento privado y servicio de valet parking"""
            response.message(respuesta_FAQ_3)
        
        elif compare_sentence_with_list(incoming_message, lista_FAQ_4):
            respuesta_FAQ_4 = """El dress code es smart business. Te proponemos algunas opciones:\n- Combinación de prendas\n- Camisas lisas, corbata opcional\n- Tejidos como la lana, el tweed y el algodón\n- Blazers con falda, vestidos por la rodilla, camisas lisas o pantalones de sastre\n- Joyas sencillas y lisas, si se llevan\n- Cinturones y zapatos cerrados pulidos\n- Maletines, bolsos de mano o elegantes\nLa paleta de colores suele ser de tonos neutros como el negro, el azul marino, el gris, el beige y el crema"""
            response.message(respuesta_FAQ_4)

        elif compare_sentence_with_list(incoming_message, lista_FAQ_5):
            respuesta_FAQ_5 = """El itinerario del evento será el siguiente:\n19:00 hrs - Registro\n20:00 hrs - Bienvenida\n20:15 hrs - Presentación\n21:15 hrs - Cena"""
            response.message(respuesta_FAQ_5)

        elif compare_sentence_with_list(incoming_message, lista_despedida):
            respuesta_FAQ_6 = """Fue un gusto ayudarte. Hasta luego"""
            response.message(respuesta_FAQ_6)

        # If it's not a frequently asked question, escalate the conversation to a human agent
        else:
            response.message("""Para responder a su pregunta, a continuación un asesor lo atenderá por este medio. Gracias por su paciencia""")
            forward_to_agent(incoming_message)
            pass

        return str(response)
    else:
        return "Inicio exitoso"


def forward_to_agent(message):
    # Logic to forward the message to a human agent
    # You can use Twilio Notify, send an email, or integrate with a messaging platform to notify the agent
    agent_phone_number = '+525551078511'
    try:
        client.messages.create(
            body=message,
            from_=twilio_phone_number,
            to=agent_phone_number
        )
    except:
        pass


def get_word_combinations(sentence):
    combinations_list = []
    word_list = sentence.split()
    
    for r in range(1, len(word_list) + 1):
        combinations_list.extend(combinations(word_list, r))

    combinations_list = [' '.join(t) for t in combinations_list]

    return combinations_list


def compare_sentence_with_list(sentence, word_list):
    
    if sentence in word_list:
        return True
    
    sentence_words = get_word_combinations(sentence)
    # sentence_words = sentence.split()
    
    for word in sentence_words:
        if word in word_list:
            return True
    
    return False

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port)
