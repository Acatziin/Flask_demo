from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from wtforms.fields.html5 import EmailField

class NoteForm(Form):
    title = StringField('Title', [validators.Length(min=1, max=45)])
    description = TextAreaField('Description', [validators.Length(min=5)])

class RegisterForm(Form):
  name = StringField('Name', [validators.Length(min=1, max=45)])
  username = StringField('Username', [validators.Length(min=4,max=45)])
  email = EmailField('Email', [
    validators.Email("Ingrese un email valido"),
    validators.DataRequired("Este campo es requerido")])
  password = PasswordField('Password', [
    validators.DataRequired(), 
    validators.EqualTo("confirm",message='Password do not match')])
  confirm = PasswordField('Confirm password')