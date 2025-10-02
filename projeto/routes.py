#criar as rotas do nosso site
from flask import render_template, url_for, redirect
from projeto import app
from flask_login import login_required #importando função login_required
from projeto.forms import FormLogin, FormCriarConta, FormFoto #importando as classes do arquivo forms.py
from projeto.models import Usuario, Foto
from projeto import database, bcrypt
from flask_login import login_user, logout_user, current_user
import os #pra poder salvar a foto no servidor
from werkzeug.utils import secure_filename # pra ter um nome seguro para as fotos que usuario subir


@app.route("/", methods=["GET", "POST"]) 
def homepage():
    form_login = FormLogin() #o form que aparece na home é o de login
    if form_login.validate_on_submit():#verifica se usuario clicou e se o clique tá válido, com todos os campos corretamente preenchidos
        usuario = Usuario.query.filter_by(email=form_login.email.data).first() #vai no BD buscar o usuário do email digitado
        if usuario and bcrypt.check_password_hash(usuario.senha, form_login.senha.data): #se o usuário existe E se a senha do bcrypt é igual à senha que ele digitou:
            login_user(usuario)
            return redirect(url_for("perfil", id_usuario=usuario.id)) # redireciona para a página de perfil, passando o usuário correto
    return render_template("homepage.html", form=form_login)



#tem que colocar o methods=[] sempre que tiver um formulário dentro da página 
@app.route("/criarconta", methods=["GET", "POST"])
def criarconta():
    form_criarconta = FormCriarConta() #o form que aparece aqui é o de criar conta
    if form_criarconta.validate_on_submit(): #verifica se usuario clicou e se o clique tá válido, com todos os campos corretamente preenchidos
        senha = bcrypt.generate_password_hash(form_criarconta.senha.data) #gera um código criptografado a partir da senha.data
        usuario = Usuario(username=form_criarconta.username.data, 
                          senha=senha,
                          email=form_criarconta.email.data)
        
        #criação do usuário no BD em 2 passos:
        database.session.add(usuario) #abre sessão temporária no BD, por eficiência mesmo
        database.session.commit() 

        login_user(usuario, remember=True) # dps de criar conta, faz o login

        return redirect(url_for("perfil", id_usuario=usuario.id)) # redireciona para a página de perfil, passando o usuário correto
    return render_template("criarconta.html", form=form_criarconta)


@app.route("/perfil/<id_usuario>", methods=["GET", "POST"])
@login_required #atributo para limitar acesso à pág de perfil
def perfil(id_usuario):
    if int(id_usuario) == int(current_user.id): #se o usuário for o próprio usuário atual
        # o usuário está vendo o próprio perfil
        form_foto = FormFoto()
        if form_foto.validate_on_submit():
            arquivo = form_foto.foto.data
            nome_seguro = secure_filename(arquivo.filename) #cria um nome seguro para os arquivos

            #salvar o arquivo na pasta fotos_posts
            caminho = os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config["UPLOAD_FOLDER"], nome_seguro)
            #"os.path.dirname(__file__)": caminho desse arquivo aqui (routes.py, representado pelo __file__)
            #"app.config["UPLOAD_FOLDER"]": caminho da pasta, configurada no arquivo __init__.py
            #"nome_seguro": nome seguro do arquivo
            arquivo.save(caminho)
            #registrar esse arquivo no BD
            foto = Foto(imagem=nome_seguro, id_usuario=current_user.id)
            database.session.add(foto) #adiciona nossa foto no BD
            database.session.commit() #sallva modificação no BD

        return render_template("perfil.html", usuario=current_user, form=form_foto)
    else:
        usuario = Usuario.query.get(int(id_usuario))
        return render_template("perfil.html", usuario=usuario, form=None)


@app.route("/logout")
@login_required
def logout():
    logout_user() #poderia ser "logout_user(current_user)" mas seria redundante
    return redirect(url_for("homepage"))

@app.route("/feed")
@login_required
def feed():
    fotos = Foto.query.order_by(Foto.data_criacao).all() #variável 'foto' recebe as fotos por ordem de criação, da mais antiga pra mais nova. Incluir [:100] no fim da linha pra exibir apenas as 100 primeiras fotos postadas no site
    return render_template("feed.html", fotos=fotos)
