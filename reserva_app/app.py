from flask import Flask, render_template, request, redirect, url_for, flash
from datetime import datetime
from reserva_app.conexao_bd import conexao_fechar, conexao_abrir
import unicodedata

app = Flask(__name__)
app.secret_key = 'abgl' #define uma chave secreta para sessões e mensagens do flash

con = conexao_abrir("127.0.0.1", "estudante1", "123", "teste_python")

usuarioatual = None #variável global que armazena o usuário logado

#função para salvar um novo usuário no Banco de Dados
def salvar_usuario(nome, sobrenome,email, senha):
 #  texto = f"{nome},{sobrenome},{email},{senha}\n"
  #  with open("usuarios.csv", "a") as arquivo_usuarios:
  #      arquivo_usuarios.write(texto)
    cursor = con.cursor()
    sql = "INSERT INTO usuário (nome, email, senha, sobrenome) VALUES (%s, %s, %s, %s)"
    cursor.execute(sql, (nome, email, senha, sobrenome))
    con.commit() 
    cursor.close()
    
#função para salvar uma nova sala no Banco de dados 
def salvar_sala(tipo, capacidade, descricao, ativa=1):
    cursor = con.cursor()
    sql = "INSERT INTO sala (tipo, capacidade, descricao, ativa) VALUES (%s, %s, %s, %s)"
    cursor.execute(sql, (tipo, capacidade, descricao, ativa))
    con.commit() 
    cursor.close()


#função para salvar uma nova reserva no Banco de dados      
def salvar_reserva(Sala_idsala, inicio, fim, Usuário_idusuario):      
    #texto = f"{sala},{inicio},{fim},{usuario}\n"       
    #with open("reservas.csv", "a") as arquivo_reservas:
    #    arquivo_reservas.write(texto)
    cursor = con.cursor()
    sql = "INSERT INTO reserva_sala (idsala, inicio, fim, idusuario) VALUES (%s, %s, %s, %s)"
    cursor.execute(sql, (Sala_idsala, inicio, fim, Usuário_idusuario))
    con.commit() 
    cursor.close()
     
def remove_accents(input_str):
    nfkd_form = unicodedata.normalize('NFKD', input_str)
    return ''.join([c for c in nfkd_form if not unicodedata.combining(c)])     
            
#função para ler as salas 
def ler_salas():
    salas = []
    cursor = con.cursor(dictionary=True)
    sql = "SELECT idsala, tipo, capacidade, descricao,ativa FROM sala"  # Certifique-se de que `id` está incluído na consulta.
    cursor.execute(sql)

    for registro in cursor:
        sala = {
            "idsala": registro['idsala'],
            "tipo": registro['tipo'],
            "capacidade": registro['capacidade'],
            "descricao": remove_accents(registro['descricao']),
            "ativa": registro['ativa'] 
        }
        salas.append(sala)

    cursor.close()
    return salas
 

#função para ler as reservas 
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
    cursor = con.cursor(dictionary=True)
    sql = "SELECT * FROM usuário WHERE email = %s AND senha = %s"
    cursor.execute(sql, (email2, senha2))
    usuario = cursor.fetchone()
    cursor.close()
    
    if usuario:
        return usuario['nome']  # Retorna o nome do usuário logado
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


@app.route("/excluir-sala/<int:id>", methods=["POST"])
def excluir_sala(id):
    cursor = con.cursor()
    sql = "DELETE FROM sala WHERE idsala = %s"
    cursor.execute(sql, (id,))
    con.commit()
    cursor.close()
    return redirect(url_for("listar_salas"))

@app.route("/desativar-sala/<int:id>", methods=["POST"])
def desativar_sala(id):
    cursor = con.cursor()
    sql = "UPDATE sala SET ativa = 0 WHERE idsala = %s"
    cursor.execute(sql, (id,))
    con.commit()
    cursor.close()
    return redirect(url_for("listar_salas"))

@app.route("/ativar-sala/<int:id>", methods=["POST"])
def ativar_sala(id):
    cursor = con.cursor()
    sql = "UPDATE sala SET ativa = 1 WHERE idsala = %s"
    cursor.execute(sql, (id,))
    con.commit()
    cursor.close()
    return redirect(url_for("listar_salas"))

@app.route("/editar-sala/<int:idsala>", methods=["GET", "POST"])
def editar_sala(idsala):
    cursor = con.cursor(dictionary=True)
    if request.method == "POST":
        tipo = request.form.get("tipo")
        capacidade = request.form.get("capacidade")
        descricao = request.form.get("descricao")
        sql = "UPDATE sala SET tipo = %s, capacidade = %s, descricao = %s WHERE idsala = %s"
        cursor.execute(sql, (tipo, capacidade, descricao, idsala))
        con.commit()
        cursor.close()
        return redirect(url_for("listar_salas"))
    else:
        sql = "SELECT * FROM sala WHERE idsala = %s"
        cursor.execute(sql, (idsala,))
        sala = cursor.fetchone()
        cursor.close()
        return render_template("editar-sala.html", sala=sala)
    
conexao_fechar(con)    
app.run(debug=True, port= 5001)
