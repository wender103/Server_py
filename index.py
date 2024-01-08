import http.server
import socketserver
import subprocess
import json
import binascii
import socket

class MyRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        print(f"Recebida solicitação GET para {self.path}")

        if self.path == '/open_spotify':
            self.handle_open_spotify()
        elif self.path == '/ligar_pc':
            self.handle_ligar_pc()
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
            else:
                response_data = {"status": "error", "message": "Comando não reconhecido"}
                self.wfile.write(json.dumps(response_data).encode())
        else:
            # Servir arquivos estáticos
            super().do_GET()

    def handle_open_spotify(self):
        # Lógica para manipular a rota /open_spotify
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")  # Isso permite qualquer origem
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

        response_data = {"status": "success", "message": "Conexão estabelecida"}
        self.wfile.write(json.dumps(response_data).encode())

    def handle_ligar_pc(self):
        # Lógica para manipular a rota /ligar_pc
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

    def ligar_pc(self):
        # Código para ligar o PC
        #AC-22-0B-2E-13-5C
        mac_address = '00-1A-7D-DA-71-10'
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

PORT = 8000
Handler = MyRequestHandler

with socketserver.TCPServer(("0.0.0.0", PORT), Handler) as httpd:
    print(f"Servindo na porta {PORT}")
    httpd.serve_forever()