from django.shortcuts import render, redirect
from django.contrib import messages
from forms import Register, Login
from models import User
import bcrypt

def index(request):
    form = Register()
    login = Login()
    context = {
        'form': form,
        'form2': login,
    }
    return render(request, "login_reg/index.html", context)

def register(request):
    # try:
    #     request.session['registered']
    # except KeyError:
    #     request.session['registered'] = []
    form = Register(request.POST)
    form2 = Login()
    if request.method == 'POST':
        if form.is_valid():
            email = form.cleaned_data['email']
            create = User.objects.create(first_name = form.cleaned_data['first_name'], 
            last_name = form.cleaned_data['last_name'], email = form.cleaned_data['email'], 
            password = bcrypt.hashpw(form.cleaned_data['password'].encode('utf8'), bcrypt.gensalt()
            ))
            # create.save()
            # request.session['registered'] = form.cleaned_data['first_name']
            messages.add_message(request, messages.INFO, form.cleaned_data['first_name'], extra_tags="name")
            messages.add_message(request, messages.INFO, "registered!", extra_tags="register")
            return redirect('/success')
    context = {
        "form": form,
        "form2": form2,
    }
    return render(request, "login_reg/index.html", context)

def login(request):
    # try:
    #     request.session['login']
    # except KeyError:
    #     request.session['login'] = []
    form = Register()
    login = Login(request.POST)
    if request.method == 'POST':
        if login.is_valid():    
            print "valid"
            email = login.cleaned_data['email']
            # request.session['login'] = User.objects.get(email=email).first_name
            messages.add_message(request, messages.INFO, User.objects.get(email=email).first_name, extra_tags="name")
            messages.add_message(request, messages.INFO, "logged in!", extra_tags="login")
            return redirect('/success')
            
    print "failed login form check"
    context = {
        "form": form,
        "form2": login,
    }
    return render(request, "login_reg/index.html", context)

def success(request):
    # context = {
    #     'reg': request.session['login'],
    # }
    # request.session.clear()
    return render(request, "login_reg/success.html")