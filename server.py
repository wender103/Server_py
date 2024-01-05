import http.server
import socketserver
import subprocess
import json
from urllib.parse import parse_qs

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

PORT = 8000
Handler = MyRequestHandler

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print(f"Servindo na porta {PORT}")
    httpd.serve_forever()
