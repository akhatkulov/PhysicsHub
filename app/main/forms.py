from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField, SubmitField
from wtforms.validators import DataRequired,InputRequired,Length

class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[DataRequired()])
    submit = SubmitField('Submit')

class SignInForm(FlaskForm):
    username = StringField('Taxallus:', validators=[DataRequired()])
    password = PasswordField('Parol:', validators=[DataRequired()])

class SignUpForm(FlaskForm):
    name = StringField('Ism:', validators=[InputRequired()])
    surname = StringField('Familiya:', validators=[InputRequired()])
    username = StringField('Taxallus:', validators=[InputRequired()])
    university = StringField('O\'qish joyi:', validators=[InputRequired()])
    password = PasswordField('Parol:', validators=[InputRequired()])

class UpdateData(FlaskForm):
    name = StringField('Ism:', validators=[InputRequired()])
    surname = StringField('Familiya:', validators=[InputRequired()],render_kw={"placeholder": "********"})
    username = StringField('Taxallus:', validators=[InputRequired()],render_kw={"disabled": "disabled"})
    university = StringField('O\'qish joyi:', validators=[InputRequired()])
    password = PasswordField('Parol:',render_kw={"placeholder": "********"})