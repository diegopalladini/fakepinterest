from flask import Flask #importa o Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt


app = Flask(__name__) #cria a aplicação
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///comunidade2.db" #linha de config do BD
app.config["SECRET_KEY"] = "7cf1df1f88fb19011d0bf7381b75b40a" #linha de config do login
app.config["UPLOAD_FOLDER"] = "static/fotos_posts" #pasta de upload das fotos do usuario

database = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "homepage" # se um usuário não estiver logado, pra onde ele será redirecionado

from projeto import routes #importa o arquivo de rotas do projeto. 
#Importante vir depois pq primeiro o flask precisa criar o app e só depois importar as rotas
