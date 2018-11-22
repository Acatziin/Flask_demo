from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from wtforms.fields.html5 import EmailField

class NoteForm(Form):
    title = StringField('Title', [validators.Length(min=1, max=45)])
    description = TextAreaField('Description', [validators.Length(min=5)])

class RegisterForm(Form):
  name = StringField('Nombre', [validators.Length(min=1, max=45)])
  username = StringField('Nombre de usuario', [validators.Length(min=4,max=45)])
  email = EmailField('Correo electrónico', [
    validators.Email("Ingrese un email valido"),
    validators.DataRequired("Este campo es requerido")])
  password = PasswordField('Contraseña (mínimo 4 dìgitos)', [
    validators.DataRequired(), 
    validators.EqualTo("confirm",message = 'La contraseñas no coinciden'),
    validators.Length(min=4)])
  confirm = PasswordField('Confirmar contraseña')

class LoginForm(Form):
    username = StringField('Nombre de usuario', [
      validators.required(),
      validators.Length(min=4,max=45)])
    password = PasswordField('Contraseña', [validators.DataRequired()])

class EditDataForm(Form):
  name = StringField('Nombre', [
    validators.Length(min=1, max=45),
    validators.DataRequired("Este campo es requerido")])
  email = EmailField('Correo electrónico', [
    validators.Email("Ingrese un email valido"),
    validators.DataRequired("Este campo es requerido")])
  password = PasswordField('Contraseña (mínimo 4 dìgitos)', [
    validators.EqualTo("confirm",message = 'Las contraseñas no coinciden'),
    validators.Length(min=4)])
  confirm = PasswordField('Confirmar contraseña')