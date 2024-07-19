from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

def verifica_usuario():
    if request.method == "POST":
        with open("usuarios.csv") as usuarios:
                       
            for linha in usuarios:
                dados = linha.split(",").strip()
                print(dados)
        return redirect(url_for("cadastrar_sala"))           
    else:
        return render_template("login.html")


               
def salvar_usuario(email, senha):
    texto = f"\n{email},{senha}"
    with open("usuarios.csv", "a") as usuarios:
        usuarios.write(texto)
        
def salvar_sala(tipo, capacidade, descricao):
    texto = f"\n{tipo},{capacidade},{descricao}"
    with open("salas.csv", "a") as salas:
        salas.write(texto)
 

@app.route("/", methods=["GET","POST"])
def cadastro():
    if request.method == "POST":
        with open("usuarios.csv", "w") as usuarios:
            
            email = request.form.get('email')
            senha = request.form.get('password')
            print(f"EMAIL: {email}")
            print(f"SENHA: {senha}")
            
            salvar_usuario(email, senha)
                   
        return redirect(url_for("cadastrar_sala"))           
    else:
        return render_template("cadastro.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
       
        emaill = request.form.get('EMAIL')
        senhaa = request.form.get('PASSWORD')
        print(f"EMAILll: {emaill}")
        print(f"SENHAaa: {senhaa}")
                    
        return redirect(url_for("cadastrar_sala"))           
    else:
        return render_template("login.html")



@app.route("/cadastrar-sala")
def cadastrar_sala():
    if request.method == "POST":
        with open("usuarios.csv", "w") as usuarios:
      
            tipo = request.form.get('tipo')
            capacidade = request.form.get('capacidade')
            descricao = request.form.get('descricao')

            print(f"tipo: {tipo}")
            print(f"capacidade: {capacidade}")
            print(f"descricao: {descricao}")

            salvar_sala(tipo,capacidade,descricao)
            
        return redirect(url_for("reservas"))           
    else:
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

