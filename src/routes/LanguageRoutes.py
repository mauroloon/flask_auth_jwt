from flask import Blueprint, request, jsonify

import traceback

# Logger
from src.utils.Logger import Logger
# Security
from src.utils.Security import Security
# Services
from src.services.LanguageService import LanguageService

main = Blueprint('language_blueprint', __name__)


@main.route('/')
def get_languages():
    has_access = Security.verify_token(request.headers)

    if has_access:
        try:
            languages = LanguageService.get_languages()
            if (len(languages) > 0):
                return jsonify({'languages': languages, 'message': "SUCCESS", 'success': True})
            else:
                return jsonify({'message': "NOTFOUND", 'success': True})
        except Exception as ex:
            Logger.add_to_log("error", str(ex))
            Logger.add_to_log("error", traceback.format_exc())

            return jsonify({'message': "ERROR", 'success': False})
    else:
        response = jsonify({'message': 'Unauthorized'})
        return response, 401
    
    

import requests

# Configura tu clave privada de Conekta
conekta_private_key = "tu_clave_privada"

# Endpoint de Conekta para crear checkouts
checkout_url = "https://api.conekta.io/checkouts"

# Datos del checkout
checkout_data = {
    'amount': 20000,
    'currency': 'MXN',
    'reference_id': 'orden_123',
    'description': 'Compra de prueba',
    'items': [{
        'name': 'Producto de prueba',
        'unit_price': 20000,
        'quantity': 1
    }],
    'charges': [{
        'payment_method': {
            'type': 'oxxo_cash'
        }
    }]
}

# Encabezados de la solicitud con tu clave privada
headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/vnd.conekta-v2.0.0+json',
    'Authorization': f"Basic {conekta_private_key}"
}

# Realiza la solicitud POST
response = requests.post(checkout_url, json=checkout_data, headers=headers)

# Verifica el estado de la respuesta
if response.status_code == 200:
    checkout_info = response.json()
    print("URL del Checkout:", checkout_info['payment_order']['hosted_link']['url'])
else:
    print("Error en la solicitud:", response.status_code, response.text)