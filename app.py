import fdb
from flask import Flask, jsonify, request
import jwt
import datetime
from functools import wraps

# Inicializando a aplicação
app = Flask(__name__)
app.config['SECRET_KEY'] = "O Lucca é corno"
con = fdb.connect(dsn='150.164.100.122:/var/www/dados/scntestes.gdb', 
                  user='sysdba', password='abdsys')
cur = con.cursor()

def Query(dado, tabela, quando):
    cur.execute("SELECT "+dado+" FROM "+tabela+" WHERE "+quando)
    for a in cur:
        return a[0]

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None 
        #http://127.0.0.1:5000/route?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyIjoiMDM4LjE2Ni44MjYtNjkiLCJleHAiOjE1NzA0NzkzNDJ9.lAFsh878O5VhL-sJ1sI0cu17-LwCBPaFi_bUTP5yZl0
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if not token:
            return jsonify(message = "Token is missing")
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
            current_user_id = str(data['info']['NUMAUT'])
        except:
            return jsonify(message = "Token is invalid")
        return f(int(current_user_id), *args, **kwargs)
    return decorated 

@app.route('/dados_pessoais/<int:NUMAUT>', methods=['GET'])
#@token_required 
def dadosAlunos(NUMAUT):
    return jsonify( nome = Query(dado="NOME", tabela="ALUNO", quando="NUMAUT='"+str(NUMAUT)+"'"),
                    cpf = Query(dado="CPF", tabela="ALUNO", quando="NUMAUT='"+str(NUMAUT)+"'"),
                    sexo = Query(dado="SEXO", tabela="ALUNO", quando="NUMAUT='"+str(NUMAUT)+"'"),
                    estado = Query(dado="RESESTADO", tabela="ALUNO", quando="NUMAUT='"+str(NUMAUT)+"'"),
                    cidade = Query(dado="RESCIDADE", tabela="ALUNO", quando="NUMAUT='"+str(NUMAUT)+"'"),
                    bairro = Query(dado="RESBAIRRO", tabela="ALUNO", quando="NUMAUT='"+str(NUMAUT)+"'"),
                    rua = Query(dado="RESRUA", tabela="ALUNO", quando="NUMAUT='"+str(NUMAUT)+"'"),
                    cep = Query(dado="RESCEP", tabela="ALUNO", quando="NUMAUT='"+str(NUMAUT)+"'"),
                    celular = Query(dado="CELULAR", tabela="ALUNO", quando="NUMAUT='"+str(NUMAUT)+"'"),
                    #senha = Query(dado="SENHAINT", tabela="ALUNO", quando="NUMAUT='"+str(NUMAUT)+"'"),
                    email = Query(dado="EMAIL", tabela="ALUNO", quando="NUMAUT='"+str(NUMAUT)+"'"))

@app.route('/exames_proficiencia', methods=['GET'])
@token_required 
def exameProficiencia(NUMAUT):
    json_exames = []
    for j in range(0):
        j = Query(dado="", tabela="", quando="NUMAUT='"+NUMAUT+"'")
        json_exames.append(j)
    return jsonify({"Exames de Proficiência" : json_exames})

@app.route('/login', methods=['POST'])
def login():
    json_data = request.get_json(force=True)
    cpf = str(json_data['cpf'])
    cpf = cpf[:3]+'.'+cpf[3:6]+'.'+cpf[6:9]+'-'+cpf[9:11]
    id = str(Query(dado="NUMAUT", tabela="ALUNO", quando="CPF='"+cpf+"'"))
    if id:  #Testa se é aluno
        EhAluno = True  
        senha = Query(dado="SENHAINT", tabela="ALUNO", quando="NUMAUT='"+id+"'")
    else:
        return jsonify(token = "Login incorreto")
    #else:   #Se for professor (Não sei se a tabela está certa)
    #    EhAluno = False  
    #    id = Query(dado="NUMAUT", tabela="PROFESSOR", quando="CPF='"+cpf+"'")
    #    Query(dado="SENHAINT", tabela="PROFESSOR", quando="NUMAUT='"+id+"'")
    if json_data['senha'] == senha:
        token = jwt.encode({"info":{'NUMAUT':id, "Aluno":EhAluno}, 'exp':datetime.datetime.utcnow()+datetime.timedelta(days=1)}, app.config['SECRET_KEY'])
        return jsonify(token = token.decode('UTF-8'), aluno = EhAluno)
    return jsonify(token = "Senha incorreta")

@app.route('/')
#@token_required 
def index_():
    return "KOE"

if __name__ == '__main__':
    app.run(debug=True)
