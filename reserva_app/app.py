from flask import Flask, render_template, request, redirect, url_for, flash
from datetime import datetime
import unicodedata

app = Flask(__name__)
app.secret_key = 'abgl' #define uma chave secreta para sessões e mensagens do flash

usuarioatual = None #variável global que armazena o usuário logado

#função para salvar um novo usuário no arquivo CSV
def salvar_usuario(nome, sobrenome,email, senha):
    texto = f"{nome},{sobrenome},{email},{senha}\n"
    with open("usuarios.csv", "a") as arquivo_usuarios:
        arquivo_usuarios.write(texto)
    
#função para salvar uma nova sala no arquivo CSV       
def salvar_sala(tipo, capacidade, descricao):
    texto = f"{tipo},{capacidade},{descricao}\n"
    with open("salas.csv", "a") as arquivo_salas:
        arquivo_salas.write(texto)

#função para salvar uma nova reserva no arquivo CSV        
def salvar_reserva(sala, inicio, fim, usuario):      
    texto = f"{sala},{inicio},{fim},{usuario}\n"       
    with open("reservas.csv", "a") as arquivo_reservas:
        arquivo_reservas.write(texto)
     
def remove_accents(input_str):
    nfkd_form = unicodedata.normalize('NFKD', input_str)
    return ''.join([c for c in nfkd_form if not unicodedata.combining(c)])     
            
#função para ler as salas do arquivo CSV    
def ler_salas():
    salas = []
    with open("salas.csv", "r") as arquivo_salas:
        for linha in arquivo_salas:
            dados = linha.strip().split(",")
            sala = {
                "tipo": dados[0],
                "capacidade": dados[1],
                "descricao": remove_accents(dados[2])
            }
            salas.append(sala)
    return salas  

#função para ler as reservas do arquivo CSV
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
    return list(reversed(reservas))


#função para verificar se tem conflito de horário antes de reservar
def horario(sala, inicionovo, fimnovo):
    reservas = ler_reservas()
    for reserva in reservas:
        if reserva["sala"] == sala:
            inicioexist = reserva["inicio"]
            fimexist = reserva["fim"]
            if not (fimnovo <= inicioexist or inicionovo >= fimexist):
                return True
    return False

#rota para exibir o formulario de cadastro
@app.route("/", methods=["GET"])
def cadastro_form():
    return render_template("cadastro.html")

#rota para processar o cadastro do usuário
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

#rota para exibir o formulario de cadastro de uma sala
@app.route("/cadastro-sala", methods=["GET"])
def cadastrar_sala_form():
        return render_template("cadastrar-sala.html")

#rota para processar o cadastro de uma nova sala 
@app.route("/cadastro-sala", methods=["POST"])
def cadastrar_sala():      
    tipo = request.form.get('tipo')
    capacidade = request.form.get('capacidade')
    descricao = request.form.get('descricao')
    dado = descricao.replace("\r\n", " ")
    print(dado)
    salvar_sala(tipo,capacidade,dado)               
    return redirect(url_for("reservar_sala_form"))         
        
#função para verificar se o email e a senha estao cadastrados
def verifica_login(email2, senha2):
        with open("usuarios.csv", mode='r') as usuarios:
            for linha in usuarios:
                dados = linha.strip().split(",")
                if len(dados) < 4:
                    continue 
                nome = dados[0]
                email = dados[2]
                senha = dados[3]

                if email2 == email and senha2 == senha: 
                    return nome  
        return None 

#rota para exibir e processar o formulario de login
@app.route("/login", methods=["GET", "POST"])
def login():
    global usuarioatual
    if request.method == "POST":
        email2 = request.form.get("email-login")
        senha2 = request.form.get("password-login")

        nome_usuario = verifica_login(email2, senha2)
        if nome_usuario:
            usuarioatual = nome_usuario 
            return redirect(url_for("cadastrar_sala"))  
        else:
            flash("E-mail ou senha está errado")
            return redirect(url_for("login"))
    return render_template("login.html")

#rota para exibir o formulario de reserva de sala
@app.route("/reservar-sala", methods=["GET"])
def reservar_sala_form():
    salas = ler_salas()
    return render_template("reservar-sala.html", salas=salas)

#rota para processar a reserva de uma sala
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

#rota para exibir os detalhes de uma reserva
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

#rota para listar todas as salas
@app.route("/listar-salas")
def listar_salas():
    salas = ler_salas()
    return render_template("listar-salas.html", salas=salas)

#rota para listar todas as reservas, com filtro por sala
@app.route("/reservas", methods=["GET"])
def reservas():
    sala_filtro = request.args.get('sala', '')
    reservas = ler_reservas()
    if sala_filtro:
        reservas = [reserva for reserva in reservas if sala_filtro.lower() in reserva["sala"].lower()]
    return render_template("reservas.html", reservas=reservas)



app.run(debug=True, port= 5001)
