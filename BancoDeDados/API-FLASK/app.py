from flask import Flask, request, send_from_directory
from flask_cors import CORS
import json
import os

app = Flask(__name__, static_folder='www')  
CORS(app)

@app.route("/")
def homepage():
    return app.send_static_file("login.html")

@app.route("/<path:path>")
def static_files(path):
    return send_from_directory('www', path)

@app.route("/dados.json")
def serve_dados():
    return send_from_directory('.', 'dados.json')

@app.route("/consulta", methods=["GET"])
def consulta_cadastro():
    documento = request.args.get("doc")
    registro = dados(documento)
    return json.dumps(registro), 200, {'Content-Type': 'application/json'}

@app.route("/cadastro", methods=["POST"])
def cadastrar():
    payload = request.json
    cpf = payload.get("cpf")
    valores = payload.get("dados")
    
    if not cpf or not valores:
        return "Erro: CPF ou dados inválidos", 400
    
    dados_pessoas = carregar_arquivo()
    if cpf in dados_pessoas:
        return "Erro: CPF já existente", 400  
    
    salvar_dados(cpf, valores)
    return "Dados cadastrados com sucesso", 200

@app.route("/login", methods=["GET"])
def login():
    documento = request.args.get("doc")
    email = request.args.get("email")
    
    if not documento or not email:
        return json.dumps({"erro": "CPF e email são obrigatórios"}), 400, {'Content-Type': 'application/json'}
    
    registro = dados(documento)
    
    if registro["email"] == "Nao encontrado":
        return json.dumps({"erro": "Cliente não encontrado"}), 404, {'Content-Type': 'application/json'}
    
    if registro["email"] != email:
        return json.dumps({"erro": "Email ou CPF incorreto"}), 400, {'Content-Type': 'application/json'}
    
    return json.dumps(registro), 200, {'Content-Type': 'application/json'}

@app.route("/deletar", methods=["DELETE"])
def deletar_cliente():
    cpf = request.args.get("cpf")
    if not cpf:
        return "Erro: CPF não fornecido", 400
    
    dados_pessoas = carregar_arquivo()
    if cpf in dados_pessoas:
        del dados_pessoas[cpf]
        gravar_arquivo(dados_pessoas)
        return f"Cliente com CPF {cpf} deletado com sucesso", 200
    else:
        return "Erro: Cliente não encontrado", 404

def carregar_arquivo():
    caminho_arquivo = "dados.json"
    if os.path.exists(caminho_arquivo):  
        try:
            with open(caminho_arquivo, "r", encoding="utf-8") as arq:
                return json.load(arq)
        except (json.JSONDecodeError, FileNotFoundError):  
            return {}  
    else:
        return {}  

def gravar_arquivo(dados):
    dados_ordenados = {k: v for k, v in sorted(dados.items(), key=lambda item: item[1].get("nome", ""))}
    caminho_arquivo = "dados.json"
    with open(caminho_arquivo, "w", encoding="utf-8") as arq:
        json.dump(dados_ordenados, arq, indent=4, ensure_ascii=False)  

def salvar_dados(cpf, registro):
    dados_pessoas = carregar_arquivo()  
    dados_pessoas[cpf] = registro  
    gravar_arquivo(dados_pessoas)  

def dados(cpf):
    dados_pessoas = carregar_arquivo()  
    vazio = {
        "nome": "Nao encontrado",
        "data_nascimento": "Nao encontrado",
        "email": "Nao encontrado",
    }
    return dados_pessoas.get(cpf, vazio)  

if __name__ == "__main__":
    app.run(debug=True)
