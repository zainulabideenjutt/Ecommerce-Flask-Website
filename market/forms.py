from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField,TextAreaField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError
from market.models import User


class ItemRegisterForm(FlaskForm):
    name = StringField(label='Item Name :', validators=[
                       DataRequired(), Length(min=2, max=30)])
    price = IntegerField(label='Item Price:', validators=[
                         DataRequired()])
    barcode = StringField(label='Item Barcode :', validators=[
                          DataRequired(), Length(min=8, max=12)])
    description = TextAreaField(label='Item Description :', validators=[
                              DataRequired(), Length(min=10, max=1024)])
    submit = SubmitField(label='Create Item')

class RegisterForm(FlaskForm):
    def validate_username(self, username_to_check):
        user = User.query.filter_by(username=username_to_check.data).first()
        if user:
            raise ValidationError(
                'Username! Already Exists.Please try another one!')

    def validate_email_address(self, email_address_to_check):
        email = User.query.filter_by(
            email_address=email_address_to_check.data).first()
        if email:
            raise ValidationError(
                'Email_Address! Already Exists.Please try another one!')

    username = StringField(label='User Name : ', validators=[
                           Length(min=2, max=30), DataRequired()])
    email_address = StringField(label='Email : ', validators=[
                                Email(), DataRequired()])
    password1 = PasswordField(label='Password :', validators=[
                              Length(min=6), DataRequired()])
    password2 = PasswordField(label='Confirm Password :', validators=[
                              DataRequired(), EqualTo('password1')])
    submit = SubmitField(label='Create Account')


class LoginForm(FlaskForm):
    username = StringField(label='User Name : ', validators=[DataRequired()])
    password = PasswordField(label='Password :', validators=[DataRequired()])
    submit = SubmitField(label='Sign in')


class PurchaseForm(FlaskForm):
    submit = SubmitField(label='Purchase Item!')


class SellForm(FlaskForm):
    submit = SubmitField(label='Sell Item!')
