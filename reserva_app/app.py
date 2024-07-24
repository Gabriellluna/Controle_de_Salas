from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
app = Flask(__name__)

# def verifica_usuario():
#     if request.method == "POST":
#         with open("usuarios.csv") as usuarios:
                       
#             for linha in usuarios:
#                 dados = linha.split(",").strip()
#                 print(dados)
#         return redirect(url_for("cadastrar_sala"))           
#     else:
#         return render_template("login.html")


               


# def verifica_usuario(email, senha):
#     with open("usuarios.csv") as usuarios:
#         for linha in usuarios:
#             print(linha)

def salvar_usuario(nome, sobrenome,email, senha):
    texto = f"{nome},{sobrenome},{email},{senha}\n"
    with open("usuarios.csv", "a") as arquivo_usuarios:
        arquivo_usuarios.write(texto)
    
        
def salvar_sala(tipo, capacidade, descricao):
    texto = f"{tipo},{capacidade},{descricao}\n"
    with open("salas.csv", "a") as arquivo_salas:
        arquivo_salas.write(texto)
        
def salvar_reserva(sala, inicio, fim):
    
    inicio_dt = inicio.date()
    fim_dt = fim.date()
    
    print(inicio_dt)
    print(fim_dt)
    
    # inicio_dt = datetime.fromisoformat(inicio) 
    # fim_dt = datetime.fromisoformat(fim)
    
    # inicio_formatado = inicio_dt.strftime("%d/%m/%Y - %H:%M")
    # fim_formatado = fim_dt.strftime("%d/%m/%Y - %H:%M")
    
    texto = f"{sala},{inicio_formatado},{fim_formatado}\n"
    
    with open("reservas.csv", "a") as arquivo_reservas:
        arquivo_reservas.write(texto)
       
        
def ler_salas():
    salas = []
    with open("salas.csv", "r") as arquivo_salas:
        for linha in arquivo_salas:
            dados = linha.strip().split(",")
            salas.append(dados[0]) 
    return salas      
 
@app.route("/", methods=["GET"])
def cadastro_form():
    return render_template("cadastro.html")


@app.route("/", methods=["POST"])
def cadastro():
    nome = request.form.get('nome-cadastro')
    sobrenome = request.form.get('sobrenome-cadastro')
    email = request.form.get('email-cadastro')
    senha = request.form.get('password-cadastro')
    print(email)
    salvar_usuario(nome,sobrenome,email, senha)           
    return redirect(url_for("cadastrar_sala"))

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
        


# @app.route("/login", methods=["GET", "POST"])
# def login():
#         email = request.form.get('email-login')
#         senha = request.form.get('password-login')
#         verifica_usuario(email, senha)
   
#         return render_template("login.html")




@app.route("/reservar-sala", methods=["GET"])
def reservar_sala_form():
    salas = ler_salas()
    return render_template("reservar-sala.html", salas=salas)

@app.route("/reservar-sala", methods=["POST"])
def reservar_sala():
    sala = request.form.get('sala')
    inicio = request.form.get('inicio')
    fim = request.form.get('fim')
    print(sala, inicio, fim)
    salvar_reserva(sala, inicio, fim)
    return redirect(url_for("reservar_sala_form"))

@app.route("/detalhe-reserva")
def detalhe_reserva():
    return render_template("detalhe-reserva.html")

@app.route("/listar-salas")
def listar_salas():
    return render_template("listar-salas.html")



@app.route("/reservas")
def reservas():
    return render_template("reservas.html")


app.run(debug=True)
