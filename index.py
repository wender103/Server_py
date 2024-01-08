from flask import Flask, jsonify
from flask_cors import CORS
import subprocess
import json
import binascii
import socket

app = Flask(__name__)
CORS(app)

@app.route('/open_spotify', methods=['GET', 'POST', 'OPTIONS'])
def open_spotify():
    handle_open_spotify()
    return jsonify({"status": "success", "message": "Conexão estabelecida"})

@app.route('/ligar_pc', methods=['GET', 'POST', 'OPTIONS'])
def ligar_pc():
    handle_ligar_pc()
    return jsonify({"status": "success", "message": "PC ligado"})

def handle_open_spotify():
    add_cors_headers()
    # Lógica para manipular a rota /open_spotify

def handle_ligar_pc():
    add_cors_headers()
    # Lógica para manipular a rota /ligar_pc
    ligar_pc()

def add_cors_headers():
    # Adiciona cabeçalhos CORS
    headers = {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
        "Access-Control-Allow-Headers": "Content-Type"
    }
    for key, value in headers.items():
        app.response_class.default_headers[key] = value

def ligar_pc():
    # Código para ligar o PC
    # AC-22-0B-2E-13-5C
    # 00-1A-7D-DA-71-10
    mac_address = 'AC-22-0B-2E-13-5C'
    # Cria um socket UDP
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    # Endereço de broadcast e porta padrão para WoL
    broadcast_address = ('192.168.1.255', 7)

    # Formata o Magic Packet usando o endereço MAC
    mac_address = mac_address.replace('-', '').replace(':', '')

    # Adiciona um zero à frente se o comprimento da string for ímpar
    if len(mac_address) % 2 != 0:
        mac_address = '0' + mac_address

    try:
        mac_hex = binascii.unhexlify(mac_address)
        magic_packet = b'\xff' * 6 + mac_hex * 16

        # Envia o Magic Packet
        s.sendto(magic_packet, broadcast_address)
        print("Magic Packet enviado com sucesso!")

    except binascii.Error:
        print("Erro: A string contém caracteres não hexadecimais.")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)