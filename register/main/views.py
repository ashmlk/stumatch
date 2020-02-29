from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, redirect
from .forms import SignUpForm, EditProfileForm, PasswordResetForm
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash

def main_page(request):
    return render(request,'login.html')

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('main:main_page'))  
    
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            return redirect('main:main_page')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

def user_login(request):
    if request.user.is_authenticated:
        username = request.user.username
        return redirect(reverse('home:home', kwargs={'username': username})) 
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:              
                login(request,user)
                messages.info(request, "Successfully signed in")
                #return redirect('main:home')
                return redirect(reverse('home:home', kwargs={'username': username})) 
            else:
                message = 'Sorry, the username or password you entered is not valid please try again.'
                return render(request, 'login.html', {'message':message})
        else:
            message = 'Sorry, the username or password you entered is not valid please try again.'
            return render(request, 'login.html', {'message':message})
    else:
        form=AuthenticationForm()
        return render(request, 'login.html', {"form":form})

@login_required
def edit_profile(request,username):
    if request.method=='POST':
        form = EditProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            username = request.user.username
            #return redirect('main:home')
            return redirect(reverse('home:home', kwargs={'username': username})) 
    else:
        form = EditProfileForm(instance=request.user)
        args = {'form':form}
        return render(request, 'edit_profile.html', args)
# views users homePage
def user_homepage(request):
    pass