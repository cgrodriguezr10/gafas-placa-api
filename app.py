from flask import Flask, jsonify, request
from flask_cors import CORS
import os
import re
import base64

app = Flask(__name__)
CORS(app)

placas = {
    "ABC123": {"soat": "VIGENTE", "soat_vence": "2025-12-31", "rtm": "VIGENTE", "rtm_vence": "2025-06-15", "tipo": "Automovil"},
    "XYZ789": {"soat": "VENCIDO", "soat_vence": "2024-08-10", "rtm": "VIGENTE", "rtm_vence": "2025-09-20", "tipo": "Camioneta"},
    "DEF456": {"soat": "VIGENTE", "soat_vence": "2025-11-05", "rtm": "VENCIDO", "rtm_vence": "2024-12-01", "tipo": "Moto"},
    "GHI321": {"soat": "VENCIDO", "soat_vence": "2024-03-15", "rtm": "VENCIDO", "rtm_vence": "2024-01-10", "tipo": "Bus"},
    "JKL654": {"soat": "VIGENTE", "soat_vence": "2026-01-20", "rtm": "VIGENTE", "rtm_vence": "2026-03-10", "tipo": "Automovil"},
    "MNO987": {"soat": "VENCIDO", "soat_vence": "2023-11-30", "rtm": "VENCIDO", "rtm_vence": "2023-09-05", "tipo": "Moto"},
    "PQR147": {"soat": "VIGENTE", "soat_vence": "2025-08-18", "rtm": "VIGENTE", "rtm_vence": "2025-12-22", "tipo": "Camion"},
    "STU258": {"soat": "VENCIDO", "soat_vence": "2024-05-01", "rtm": "VIGENTE", "rtm_vence": "2025-07-30", "tipo": "Automovil"},
    "VWX369": {"soat": "VIGENTE", "soat_vence": "2025-10-10", "rtm": "VENCIDO", "rtm_vence": "2024-11-15", "tipo": "Camioneta"},
    "YZA741": {"soat": "VIGENTE", "soat_vence": "2026-02-28", "rtm": "VIGENTE", "rtm_vence": "2026-01-05", "tipo": "Bus"},
}

def extraer_placa(texto):
    texto = texto.upper().replace(" ", "")
    patron = re.search(r'[A-Z]{3}[0-9]{3}', texto)
    if patron:
        return patron.group()
    patron_moto = re.search(r'[A-Z]{2}[0-9]{4}', texto)
    if patron_moto:
        return patron_moto.group()
    return None

def consultar_placa(placa):
    p = placa.upper().strip()
    if p in placas:
        datos = placas[p]
        if datos["soat"] == "VIGENTE" and datos["rtm"] == "VIGENTE":
            estado = "OK"
        elif datos["soat"] == "VENCIDO" and datos["rtm"] == "VENCIDO":
            estado = "CRITICO"
        else:
            estado = "ALERTA"
        return {"encontrado": True, "placa": p, "estado": estado, **datos}
    return {"encontrado": False, "placa": p}

@app.route('/consultar/<placa>')
def consultar(placa):
    return jsonify(consultar_placa(placa))

@app.route('/leer-imagen', methods=['POST'])
def leer_imagen():
    try:
        datos = request.get_json()
        texto = datos.get('texto', '')
        placa = extraer_placa(texto)
        if placa:
            resultado = consultar_placa(placa)
            return jsonify(resultado)
        return jsonify({"encontrado": False, "placa": "", "error": "No se detecto placa"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/')
def inicio():
    return "API Gafas Placa - OK"

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
