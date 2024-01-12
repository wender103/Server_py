from flask import Flask, render_template
from wakeonlan import send_magic_packet

app = Flask(__name__)

# Substitua 'AC-22-0B-2E-13-5C' pelo endereço MAC do seu adaptador de rede
endereco_mac = 'AC-22-0B-2E-13-5C'

# Função para ligar o computador usando Wake-on-LAN
def ligar_computador():
    send_magic_packet(endereco_mac)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ligar', methods=['POST'])
def ligar():
    ligar_computador()
    return 'Comando para ligar o computador enviado com sucesso!'

if __name__ == '__main__':
    app.run(debug=True)