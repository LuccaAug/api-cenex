import fdb
from flask import Flask, jsonify, request
import jwt
import datetime
from functools import wraps

# Inicializando a aplicação
app = Flask(__name__)
app.config['SECRET_KEY'] = "O Lucca é corno"

def Query(cur, dado, tabela, quando):
    cur.execute("SELECT "+dado+" FROM "+tabela+" WHERE "+quando)
    for a in cur:
        print(a)
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
    con = fdb.connect(dsn='150.164.100.122:/var/www/dados/scntestes.gdb', 
                    user='sysdba', password='abdsys')
    cur = con.cursor()

    nome = Query(cur, dado="NOME", tabela="ALUNO", quando="NUMAUT='"+str(NUMAUT)+"'")
    cpf = Query(cur, dado="CPF", tabela="ALUNO", quando="NUMAUT='"+str(NUMAUT)+"'")
    sexo = Query(cur, dado="SEXO", tabela="ALUNO", quando="NUMAUT='"+str(NUMAUT)+"'")
    estado = Query(cur, dado="RESESTADO", tabela="ALUNO", quando="NUMAUT='"+str(NUMAUT)+"'")
    cidade = Query(cur, dado="RESCIDADE", tabela="ALUNO", quando="NUMAUT='"+str(NUMAUT)+"'")
    bairro = Query(cur, dado="RESBAIRRO", tabela="ALUNO", quando="NUMAUT='"+str(NUMAUT)+"'")
    rua = Query(cur, dado="RESRUA", tabela="ALUNO", quando="NUMAUT='"+str(NUMAUT)+"'")
    cep = Query(cur, dado="RESCEP", tabela="ALUNO", quando="NUMAUT='"+str(NUMAUT)+"'")
    celular = Query(cur, dado="CELULAR", tabela="ALUNO", quando="NUMAUT='"+str(NUMAUT)+"'")
    senha = Query(cur, dado="SENHAINT", tabela="ALUNO", quando="NUMAUT='"+str(NUMAUT)+"'")
    email = Query(cur, dado="EMAIL", tabela="ALUNO", quando="NUMAUT='"+str(NUMAUT)+"'")
    id_AlunoTurma = Query(cur, dado="NUMTURMA", tabela="ALUNOTURMA", quando="NUMALUNO='"+str(NUMAUT)+"'")

    con.close()
    return jsonify( nome = nome,
                    cpf = cpf,
                    sexo = sexo,
                    estado = estado,
                    cidade = cidade,
                    bairro = bairro,
                    rua = rua,
                    cep = cep,
                    celular = celular,
                    #senha = senha,
                    #id_AlunoTurma = id_AlunoTurma,
                    email = email)

@app.route('/turmas/<NUMAUT>/', methods=['GET'])
#@token_required 
def turmas(NUMAUT):
    json_exames = []
    con = fdb.connect(dsn='150.164.100.122:/var/www/dados/scntestes.gdb', 
                    user='sysdba', password='abdsys')
    cur = con.cursor()

    turmas = Query(cur, dado="NUMTURMA", tabela="ALUNOTURMA", quando="NUMALUNO='"+str(NUMAUT)+"'")
    
    con.close()
    return jsonify( status = True,
                    turmas = turmas,
                    )

@app.route('/turma_especifica/<NUMAUT>/<id_Turma>', methods=['GET'])
#@token_required 
def turma_especifica(NUMAUT, id_Turma):
    json_exames = []
    con = fdb.connect(dsn='150.164.100.122:/var/www/dados/scntestes.gdb', 
                    user='sysdba', password='abdsys')
    cur = con.cursor()

    id_AlunoTurma = Query(cur, dado="NOTA", tabela="ALUNOTURMA", quando="NUMALUNO='"+str(NUMAUT)+"' AND NUMTURMA='"+str(id_Turma)+"'")
    if id_AlunoTurma == None: return jsonify(status=False)
    nota = Query(cur, dado="NOTA", tabela="ALUNOTURMA", quando="NUMAUT='"+str(id_AlunoTurma)+"'")
    freq = Query(cur, dado="FREQ", tabela="ALUNOTURMA", quando="NUMAUT='"+str(id_AlunoTurma)+"'")
    resultado = Query(cur, dado="RESULTADO", tabela="ALUNOTURMA", quando="NUMAUT='"+str(id_AlunoTurma)+"'")
    numfaltas = Query(cur, dado="NUMFALTAS", tabela="ALUNOTURMA", quando="NUMAUT='"+str(id_AlunoTurma)+"'")
    nota01 = Query(cur, dado="NOTA01", tabela="ALUNOTURMA", quando="NUMAUT='"+str(id_AlunoTurma)+"'")
    nota02 = Query(cur, dado="NOTA02", tabela="ALUNOTURMA", quando="NUMAUT='"+str(id_AlunoTurma)+"'")
    nota03 = Query(cur, dado="NOTA03", tabela="ALUNOTURMA", quando="NUMAUT='"+str(id_AlunoTurma)+"'")
    nota04 = Query(cur, dado="NOTA04", tabela="ALUNOTURMA", quando="NUMAUT='"+str(id_AlunoTurma)+"'")
    nota05 = Query(cur, dado="NOTA05", tabela="ALUNOTURMA", quando="NUMAUT='"+str(id_AlunoTurma)+"'")
    nota06 = Query(cur, dado="NOTA06", tabela="ALUNOTURMA", quando="NUMAUT='"+str(id_AlunoTurma)+"'")
    nota07 = Query(cur, dado="NOTA07", tabela="ALUNOTURMA", quando="NUMAUT='"+str(id_AlunoTurma)+"'")
    nota08 = Query(cur, dado="NOTA08", tabela="ALUNOTURMA", quando="NUMAUT='"+str(id_AlunoTurma)+"'")
    nota09 = Query(cur, dado="NOTA09", tabela="ALUNOTURMA", quando="NUMAUT='"+str(id_AlunoTurma)+"'")
    nota10 = Query(cur, dado="NOTA10", tabela="ALUNOTURMA", quando="NUMAUT='"+str(id_AlunoTurma)+"'")
    desistentes = Query(cur, dado="DESISTENTE", tabela="ALUNOTURMA", quando="NUMAUT='"+str(id_AlunoTurma)+"'")

    con.close()
    return jsonify( status = True,
                    freq = freq,
                    resultado = resultado,
                    numfaltas = numfaltas,
                    nota = nota,
                    nota01 = nota01,
                    nota02 = nota02,
                    nota03 = nota03,
                    nota04 = nota04,
                    nota05 = nota05,
                    nota06 = nota06,
                    nota07 = nota07,
                    nota08 = nota08,
                    nota09 = nota09,
                    nota10 = nota10,
                    desistentes = desistentes)

@app.route('/exames_proficiencia', methods=['GET'])
@token_required 
def exameProficiencia(NUMAUT):
    json_exames = []
    con = fdb.connect(dsn='150.164.100.122:/var/www/dados/scntestes.gdb', 
                    user='sysdba', password='abdsys')
    cur = con.cursor()

    for j in range(0):
        j = Query(cur, dado="", tabela="", quando="NUMAUT='"+NUMAUT+"'")
        json_exames.append(j)

    con.close()
    return jsonify({"Exames de Proficiência" : json_exames})

@app.route('/login', methods=['POST'])
def login():
    json_data = request.get_json(force=True)
    con = fdb.connect(dsn='150.164.100.122:/var/www/dados/scntestes.gdb', 
                    user='sysdba', password='abdsys')
    cur = con.cursor()
    cpf = str(json_data['cpf'])
    cpf = cpf[:3]+'.'+cpf[3:6]+'.'+cpf[6:9]+'-'+cpf[9:11]
    id = str(Query(cur, dado="NUMAUT", tabela="ALUNO", quando="CPF='"+cpf+"'"))
    if id:  #Testa se é aluno
        EhAluno = True  
        senha = Query(cur, dado="SENHAINT", tabela="ALUNO", quando="NUMAUT='"+id+"'")
    else:
        con.close()
        return jsonify(token = "Login incorreto")
    #else:   #Se for professor (Não sei se a tabela está certa)
    #    EhAluno = False  
    #    id = Query(cur, dado="NUMAUT", tabela="PROFESSOR", quando="CPF='"+cpf+"'")
    #    Query(cur, dado="SENHAINT", tabela="PROFESSOR", quando="NUMAUT='"+id+"'")
    if json_data['senha'] == senha:
        token = jwt.encode({"info":{'NUMAUT':id, "Aluno":EhAluno}, 'exp':datetime.datetime.utcnow()+datetime.timedelta(days=1)}, app.config['SECRET_KEY'])
        con.close()
        return jsonify(token = token.decode('UTF-8'), aluno = EhAluno)
    con.close()
    return jsonify(token = "Senha incorreta")

@app.route('/')
#@token_required 
def index_():
    return "Seja Bem vindo a rota de teste da API do Cenex !!!"

if __name__ == '__main__':
    app.run(debug=False)