from flask import Flask, render_template, request, redirect, url_for

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
    return redirect(url_for("reservar_sala"))           
        


# @app.route("/login", methods=["GET", "POST"])
# def login():
#         email = request.form.get('email-login')
#         senha = request.form.get('password-login')
#         verifica_usuario(email, senha)
   
#         return render_template("login.html")




@app.route("/reservar-sala", methods=["GET"])
def reservar_sala_form():
    return render_template("reservar-sala.html")

@app.route("/reservar-sala", methods=["POST"])
def reservar_sala():
    return render_template("reservar-sala.html")

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
