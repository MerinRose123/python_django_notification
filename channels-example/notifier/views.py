from django.shortcuts import render, redirect
from django.shortcuts import HttpResponse
from django.contrib.auth import (
    authenticate,
    login,
    logout,
    update_session_auth_hash,

)
from django.contrib.auth.hashers import make_password
from .models import *
from django.contrib import messages
from .forms import ContactForm, EditForm, LoginForm, PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.utils.safestring import mark_safe
import json
from django.contrib.auth.models import User
from rest_framework.views import APIView
from .serializers import UserSerializer
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status


# to add like to database
@login_required
def like(request):
    if request.method == 'POST':
        user = request.user
        if request.user:
            username = request.user.username
            print(username)
        if Like.objects.filter(author=request.user).exists():
            messages.success(request,'You already likes the page')
        else:
            data = Like(author=user, like=True, username=username)
            data.save()
            print(user)
            messages.success(request, 'Thank you for liking our chat application')
        return redirect('../home')
    else:
        return redirect('../home')



# The chat page where chats can be made
@login_required
def room(request):
    user = request.user
    print(user)
    return render(request, 'chat.html', {
        'room_name_json': mark_safe(json.dumps('lobby')), 'user': user})


# deleting a user
@login_required
def delete(request):
    instance = User.objects.get(username=request.user)
    instance.delete()
    messages.success(request, 'Account deleted Successfully.We are sad that you deleted your account')
    return redirect('../')


# Viewing the details of all the users in the home page
@login_required
def homeview(request):
    data = User.objects.all()
    return render(request, 'home.html', {'userlogin': data})


# To logout an already logged in user
@login_required
def logoutview(request):
    logout(request)
    response = redirect('/')
    return response


# To change tha password of an existing user.The problem is that the user will get out of the session automatically
@login_required
def passwordchange(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.POST)
        password = form.data["current_password"]
        new_password = form.data["new_password"]
        new_password1 = form.data["confirm_new_password"]
        # Checking whether the two entered new passwords are same
        if new_password1 == new_password:
            if form.is_valid():
                u = User.objects.get(username=request.user)
                # Checking if the current password entered by the user is correct
                if u.check_password(password):
                    # Changing the password in the database
                    u.set_password(new_password)
                    u.save()
                    update_session_auth_hash(request, request.user)  # this function is not working
                    messages.success(request, 'Password Changed Successfully.')
                    return redirect('../login/')
                else:
                    messages.error(request, 'Current password is not correct.')
                    return redirect('../passwordchange/')
            else:
                messages.error(request, 'form error.')
                return redirect('../passwordchange/')
        else:
            messages.error(request, 'The two new passwords are not same.')
            return redirect('../passwordchange/')
    else:
        form = PasswordChangeForm()
    return render(request, 'passwordchange.html', {'form': form})


# To edit the details of the current user
@login_required
def edit(request):
    if request.method == 'POST':
        # rendering the model form and changing details
        form = EditForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'User profile updated.')
            return redirect('../home/')

    else:
        form = EditForm(instance=request.user)
    return render(request, 'edit.html', {'form': form})


# To login a current user
def loginview(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        username = form.data['username']
        password = form.data["password"]
        # Authenticating the user by checking in the database
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, username + ' you are now logged in..!!!.')
            response = redirect('../home/')
            return response
        else:
            messages.error(request, 'username or password are not correct.')
            return render(request, 'login.html', {'form': form})
    else:
        form = LoginForm()
        return render(request, 'login.html', {'form': form})


# Registering a new user
def register(request):
    # processing the data after the user has entered the details in the form
    if request.method == 'POST':
        form = ContactForm(request.POST)
        first_name = form.data['first_name']
        last_name = form.data['last_name']
        username = form.data['username']
        mail = form.data['mail']
        password = form.data["password"]
        password2 = form.data["password_again"]
        password3 = make_password(password)
        # checking if the the two passwords are same.
        if password == password2:
            # Checking if the username already exists in the database
            if User.objects.filter(username=username).exists():
                print("username taken")
                return HttpResponse('username already exists')
            else:
                # Creating a new user with given details
                q = User(first_name=first_name, last_name=last_name, username=username, email=mail,
                         password=password3)
                q.save()
                messages.success(request, 'user registered successfully.')
                response = redirect('../login/')
                return response
        else:
            return HttpResponse('passwords are not same')
    else:
        # Rendering the form in html initially
        form = ContactForm()
    return render(request, 'register.html', {'form': form})


class UserCreate(APIView):
    """
    Creates the user using the rest framework.
    """

    def post(self, request, format='json'):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)