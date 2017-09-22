from django import forms
from models import User
import re, bcrypt

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
PASSWORD_REGEX = re.compile(r'\d.*[A-Z]|[A-Z].*\d') #searches for a upper case followed by a number and the |(or operator) looks for a number then a upper case
NAME_REGEX = re.compile(r'\W.*[A-Za-z]|[A-Za-z]\.*\W|\d.*[A-Za-z]|[A-Za-z].*\d')

class Register(forms.Form):
    first_name = forms.CharField(label='First Name', max_length=255)
    last_name = forms.CharField(label='Last Name', max_length=255)
    email = forms.CharField(label='Email', max_length=255)
    password = forms.CharField(widget=forms.PasswordInput, label='Password', max_length=255)
    confirm_password = forms.CharField(widget=forms.PasswordInput, label='Confirm Pw', max_length=255)

    def clean(self):
        cleaned_data = super(Register, self).clean()
        first_name = cleaned_data.get("first_name")
        last_name = cleaned_data.get("last_name")
        email = cleaned_data.get("email")
        password = cleaned_data.get("password")
        confirm_pw = cleaned_data.get("confirm_password")
        if NAME_REGEX.search(first_name):
            msg = "Invalid first name!"
            self.add_error('first_name', msg)
        if NAME_REGEX.search(last_name):
            msg = "Invalid last name!"
            self.add_error('last_name', msg)
        if not EMAIL_REGEX.match(email):
            msg = "Invalid Email Address"
            self.add_error('email', msg)
        if User.objects.filter(email = email):
            msg = "Email address has already been used"
            self.add_error('email', msg)
        if password != confirm_pw:
            msg = "Your password and confirm password do not match!"
            self.add_error('password', msg)
            self.add_error('confirm_password', msg)

class Login(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput, label='Password', max_length=255)
    email = forms.CharField(label='Email', max_length=255)

    def clean(self):
        cleaned_data = super(Login, self).clean()
        email = cleaned_data.get("email")
        password = cleaned_data.get("password")
        if not User.objects.filter(email = email):
            msg = "Email not registered in database"
            self.add_error('email', msg)
            return True #ty chuck and rodrigo
        if bcrypt.checkpw(password.encode('utf8'), User.objects.get(email=email).password.encode('utf8')) != True:
            msg = "Incorrect password!"
            self.add_error('password', msg)