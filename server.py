from flask import Flask
from flask import request
import socket
import binascii
from flask_sslify import SSLify

app = Flask(__name__)
sslify = SSLify(app)

def wake_on_lan(mac_address):
    # Cria um socket UDP
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    # Endereço de broadcast e porta padrão para WoL
    #192.168.1.255
    #192.168.0.114
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

# Endereço MAC do seu PC
#AC-22-0B-2E-13-5C
# wake_on_lan('AC-22-0B-2E-13-5C')

@app.route('/wake-on-lan', methods=['POST'])
def wake_on_lan_endpoint():
    mac_address = request.json.get('mac_address')
    wake_on_lan(mac_address)
    return 'Magic Packet enviado com sucesso!'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)