#criar os formularios do nosso site
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FileField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from projeto.models import Usuario

class FormLogin(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    senha = PasswordField("Senha", validators=[DataRequired()])
    botao_confirmacao = SubmitField("Fazer Login")

    def validate_email(self, email): #função para validar o email
        usuario = Usuario.query.filter_by(email=email.data).first()
        if not usuario: #se já existe um usuário com esse email
            raise ValidationError("Usuário inexistente. Crie uma conta.")


class FormCriarConta(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    username = StringField("Nome de usuário", validators=[DataRequired()])
    senha = PasswordField("Senha", validators=[DataRequired(), Length(6,20)])
    confirmacao_senha = PasswordField("Confirmação de Senha", validators=[DataRequired(), EqualTo("senha")])
    botao_confirmacao = SubmitField("Criar Conta")

    def validate_email(self, email): #função para validar o email
        usuario = Usuario.query.filter_by(email=email.data).first()
        if usuario: #se já existe um usuário com esse email
            raise ValidationError("Email já cadastrado. Faça login para continuar")
        
class FormFoto(FlaskForm): #formulário de envio de fotos pelo usuario
    foto = FileField("Foto", validators=[DataRequired()])
    botao_confirmacao = SubmitField("Enviar")
