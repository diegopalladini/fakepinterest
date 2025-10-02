#criar a estrutura do banco de dados

from projeto import database # importando o database dentro do arquivo __init__.py
from projeto import login_manager # buscando o login_manager dentro do arquivo __init__.py
from datetime import datetime #só pra usar no Foto.data_criacao
from flask_login import UserMixin #ele quem diz qual a classe que gerencia a estrutura de logins. No nosso caso, a classe Usuario, então ele entra como parâmetro


#funcao necessária para fazer login de usuário
@login_manager.user_loader
def load_usuario(id_usuario):
    return Usuario.query.get(int(id_usuario)) #retorna pra gente um usuário específico que ele pesquisa("query") e pega("get") dentro do BD



class Usuario(database.Model, UserMixin): #criando uma classe que o BD vai entender (database.Model)
    id = database.Column(database.Integer, primary_key=True)
    username = database.Column(database.String, nullable=False)
    email = database.Column(database.String, nullable=False, unique=True)
    senha = database.Column(database.String, nullable=False)
    fotos = database.relationship("Foto", backref="usuario", lazy=True)

class Foto(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    imagem = database.Column(database.String, default="default.png")
    data_criacao = database.Column(database.DateTime, nullable=False, default=datetime.now())
    id_usuario = database.Column(database.Integer, database.ForeignKey('usuario.id'), nullable=False)