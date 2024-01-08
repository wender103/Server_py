import http.server
import socketserver
import subprocess
import json
import binascii
import socket
import logging
from urllib.parse import parse_qs

# Configuração de logging
logging.basicConfig(level=logging.INFO)

class MyRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/open_spotify':
            # Adicionar cabeçalhos CORS
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")  # Isso permite qualquer origem
            self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
            self.send_header("Access-Control-Allow-Headers", "Content-Type")
            self.end_headers()

            response_data = {"status": "success", "message": "Conexão estabelecida"}
            self.wfile.write(json.dumps(response_data).encode())

            # Log de sucesso no servidor
            logging.info("Conexão estabelecida com sucesso.")

        elif self.path == '/ligar_pc':
            # Adicionar cabeçalhos CORS
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")  # Isso permite qualquer origem
            self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
            self.send_header("Access-Control-Allow-Headers", "Content-Type")
            self.end_headers()

            # Ligar o PC aqui
            self.ligar_pc()

            response_data = {"status": "success", "message": "PC ligado"}
            self.wfile.write(json.dumps(response_data).encode())

            # Log de sucesso no servidor
            logging.info("PC ligado com sucesso.")

        else:
            # Servir arquivos estáticos
            super().do_GET()

    def do_OPTIONS(self):
        # Adicionar cabeçalhos CORS para lidar com solicitações OPTIONS
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")  # Isso permite qualquer origem
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_POST(self):
        if self.path == '/open_spotify':
            # Obter o corpo da solicitação
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            comando = json.loads(post_data)

            # Adicionar cabeçalhos CORS
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")  # Isso permite qualquer origem
            self.end_headers()

            # Analisar o objeto e realizar ações correspondentes
            if comando.get('Comando') == 'Abrir' and comando.get('Programa') == 'Spotify':
                # Comando para abrir o Spotify no Windows (ajuste conforme necessário)
                command = "start spotify"
                subprocess.Popen(command, shell=True)

                response_data = {"status": "success", "message": "Comando executado"}
                self.wfile.write(json.dumps(response_data).encode())

                # Log de sucesso no servidor
                logging.info("Comando 'Abrir Spotify' executado com sucesso.")
            else:
                response_data = {"status": "error", "message": "Comando não reconhecido"}
                self.wfile.write(json.dumps(response_data).encode())
                # Log de erro no servidor
                logging.error("Comando não reconhecido.")

        else:
            # Servir arquivos estáticos
            super().do_GET()

    def ligar_pc(self):
        # Código para ligar o PC
        #AC-22-0B-2E-13-5C
        #00-1A-7D-DA-71-10
        mac_address = 'AC-22-0B-2E-13-5C'
        # Cria um socket UDP
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

        # Endereço de broadcast e porta padrão para WoL
        # broadcast_address = ('192.168.1.255', 7)
        broadcast_address = ('255.255.255.255', 7)

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
            # Log de erro no servidor
            logging.error("Erro: A string contém caracteres não hexadecimais.")

PORT = 8000
Handler = MyRequestHandler

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print(f"Servindo na porta {PORT}")
    # Log de sucesso no servidor
    logging.info(f"Servindo na porta {PORT}")
    httpd.serve_forever()
