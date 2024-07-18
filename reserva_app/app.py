from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

def linha_para_usuarios(linha):
    dados = linha.strip().split(",")
    return {
        'email': dados[0],
        'senha': dados[1],
     }

def arquivo():
     with open("dados/usuarios.csv") as usuarios:
            for linha in usuarios:
                lista_usuarios = []
                usuario = linha_para_usuarios(linha)
                lista_usuarios.append(usuario)
                

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        with open("usuarios.txt", "w") as usuarios:
            
            email = request.form.get('email')
            senha = request.form.get('password')
            print(f"EMAIL: {email}")
            print(f"SENHA: {senha}")
            
            usuarios.write(arquivo())
                   
        return redirect(url_for("cadastrar_sala"))           
    else:
        return render_template("login.html")

@app.route("/cadastro", methods=["GET","POST"])
def cadastro():
    if request.method == "POST":
        return redirect(url_for("reservas"))
    else:
        return render_template("cadastro.html")

@app.route("/cadastrar-sala")
def cadastrar_sala():
    return render_template("cadastrar-sala.html")

@app.route("/detalhe-reserva")
def detalhe_reserva():
    return render_template("detalhe-reserva.html")

@app.route("/listar-salas")
def listar_salas():
    return render_template("listar-salas.html")

@app.route("/reservar-sala")
def reservar_sala():
    return render_template("reservar_sala.html")

@app.route("/reservas")
def reservas():
    return render_template("reservas.html")

