from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
app = Flask(__name__)

usuarioatual = None



def salvar_usuario(nome, sobrenome,email, senha):
    texto = f"{nome},{sobrenome},{email},{senha}\n"
    with open("usuarios.csv", "a") as arquivo_usuarios:
        arquivo_usuarios.write(texto)
    
        
def salvar_sala(tipo, capacidade, descricao):
    texto = f"{tipo},{capacidade},{descricao}\n"
    with open("salas.csv", "a") as arquivo_salas:
        arquivo_salas.write(texto)
        
def salvar_reserva(sala, inicio, fim, usuario):      
    texto = f"{sala},{inicio},{fim},{usuario}\n"       
    with open("reservas.csv", "a") as arquivo_reservas:
        arquivo_reservas.write(texto)
            
    
def ler_salas():
    salas = []
    with open("salas.csv", "r") as arquivo_salas:
        for linha in arquivo_salas:
            dados = linha.strip().split(",")
            sala = {
                "tipo": dados[0],
                "capacidade": dados[1],
                "descricao": dados[2]
            }
            salas.append(sala)
    return salas  


def ler_reservas():
    reservas = []
    with open("reservas.csv", "r") as arquivo_reservas:
        for linha in arquivo_reservas:
            dados = linha.strip().split(",")
            reservas.append({
                "sala": dados[0],
                "inicio": datetime.fromisoformat(dados[1]),
                "fim": datetime.fromisoformat(dados[2]),
                "usuario": dados[3]
            })
    return reservas

def horario(sala, inicionovo, fimnovo):
    reservas = ler_reservas()
    for reserva in reservas:
        if reserva["sala"] == sala:
            inicioexist = reserva["inicio"]
            fimexist = reserva["fim"]
            if not (fimnovo <= inicioexist or inicionovo >= fimexist):
                return True
    return False
 
@app.route("/", methods=["GET"])
def cadastro_form():
    return render_template("cadastro.html")


@app.route("/", methods=["POST"])
def cadastro():
    global usuarioatual
    nome = request.form.get('nome-cadastro')
    sobrenome = request.form.get('sobrenome-cadastro')
    email = request.form.get('email-cadastro')
    senha = request.form.get('password-cadastro')
    salvar_usuario(nome, sobrenome, email, senha) 
    usuarioatual = nome          
    return redirect(url_for("cadastrar_sala_form"))

@app.route("/cadastro-sala", methods=["GET"])
def cadastrar_sala_form():
        return render_template("cadastrar-sala.html")
    
@app.route("/cadastro-sala", methods=["POST"])
def cadastrar_sala():      
    tipo = request.form.get('tipo')
    capacidade = request.form.get('capacidade')
    descricao = request.form.get('descricao')
    dado = descricao.replace("\r\n", " ")
    print(dado)
    salvar_sala(tipo,capacidade,dado)               
    return redirect(url_for("reservar_sala_form"))         
        

def verifica_login(email2, senha2):
         with open("usuarios.csv") as usuarios:
            login = [] #verificação por nome e senha
            for linha in usuarios:
                dados = linha.strip().split(",") #salva nome, sobre, email e senha
                email = dados[0] #salva email
                senha = dados[-1] #salva senha
                email2 = "gabriel" #atribui valor já existente para forçar mensagem
                senha2 = "teste" #atribui valor já existente para forçar mensagem
                if email2 == email and senha2 == senha:
                    print(f"Deu bom, login correto de acesso é: {email} & {senha}") #sucesso no login 
                    break
                else:
                    print("Deu ruim") #fracasso no login
                
         return redirect(url_for("cadastrar_sala"))           



@app.route("/login", methods=["GET"])
def login():  
    email2 = request.form.get("email-login")
    senha2 = request.form.get("password-login") 
    verifica_login(email2, senha2)  
    return render_template("login.html")


#@app.route("/login", methods=["POST"])
#def verifica_usuario():                    # comentado porque independemente do que acontece no método POST da
 #   email2 = request.form("email-login")   # rota login, ele entende que tem que adicionar um novo usuário 
  #  senha2 = request.form("password-login")#no usuarios.csv


@app.route("/reservar-sala", methods=["GET"])
def reservar_sala_form():
    salas = ler_salas()
    return render_template("reservar-sala.html", salas=salas)

@app.route("/reservar-sala", methods=["POST"])
def reservar_sala():
    global usuarioatual
    sala = request.form.get('sala')
    inicio = request.form.get('inicio')
    fim = request.form.get('fim')

    ininovo = datetime.fromisoformat(inicio)
    fimnovo = datetime.fromisoformat(fim)

    if horario(sala, ininovo, fimnovo):
        return "Já existe uma reserva nesse horário"

    salvar_reserva(sala, inicio, fim, usuarioatual)
    return redirect(url_for("detalhe_reserva", sala=sala, inicio=inicio, fim=fim, usuario=usuarioatual))

@app.route("/detalhe-reserva")
def detalhe_reserva():
    sala = request.args.get('sala')
    inicio = request.args.get('inicio')
    fim = request.args.get('fim')
    usuario = request.args.get('usuario')
    inicio_dt = datetime.fromisoformat(inicio)
    fim_dt = datetime.fromisoformat(fim)
    inicio_formatado = inicio_dt.strftime('%d/%m/%Y %H:%M')
    fim_formatado = fim_dt.strftime('%d/%m/%Y %H:%M')
    
    return render_template("detalhe-reserva.html", sala=sala, inicio=inicio_formatado, fim=fim_formatado, usuario=usuario)

@app.route("/listar-salas")
def listar_salas():
    salas = ler_salas()
    return render_template("listar-salas.html", salas=salas)

@app.route("/reservas")
def reservas():
    reservas = ler_reservas()
    return render_template("reservas.html", reservas=reservas)


app.run(debug=True)
