from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, PasswordField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo


class RegistrationForm(FlaskForm):
    username = StringField('Nazwa użytkownika', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Hasło', validators=[DataRequired()])
    confirm_password = PasswordField('Potwierdź hasło', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Zarejestruj')


class LoginForm(FlaskForm):
    username = StringField('Nazwa użytkownika', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Hasło', validators=[DataRequired()])
    remember = BooleanField('Zapamiętaj mnie')
    submit = SubmitField('Zaloguj')


class AddItemForm(FlaskForm):
    isbn = StringField('ISBN', validators=[DataRequired(), Length(min=12, max=12)])
    title = StringField('Tytuł', validators=[DataRequired()])
    subtitle = StringField('Podtytuł')
    author = StringField('Autor', validators=[DataRequired()])
    published = StringField('Wydano')
    publisher = StringField('Wydawca')
    pages = IntegerField('Ilość stron')
    description = StringField('Opis')
    website = StringField('Strona internetowa')
    submit = SubmitField('Dodaj')
