from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, redirect
from .forms import SignUpForm, EditProfileForm, PasswordResetForm
from django.contrib import messages

def main_page(request):
    return render(request,'login.html')

#This was added recentely
@login_required
def home(request):
    return render(request,'home.html')

def view(response):
    return render(response, 'view.html', {})

@login_required
def user_logout(request):
    logout(request)
    return redirect('main:main_page')
    messages.info("Logged out successfully", request)
    
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
    '''
    Using different method for getting username, tried this and didnt work either
    '''
    #if request.user.is_authenticated():
        #return HttpResponseRedirect('main:home')
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:              
                login(request,user)
                messages.info(request, "Successfully signed in")
                return redirect('main:home')
                #return HttpResponseRedirect(reverse('main:home', kwargs={'username': username})) 
            else:
                message = 'Sorry, the username or password you entered is not valid please try again.'
                return render(request, 'login.html', {'message':message})
        else:
            message = 'Sorry, the username or password you entered is not valid please try again.'
            return render(request, 'login.html', {'message':message})
    else:
        form=AuthenticationForm()
        return render(request, 'login.html', {"form":form})

def edit_profile(request):
    if request.method=='POST':
        form = EditProfileForm(response.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('main:home')
    else:
        form = EditProfileForm(instance=request.user)
        args = {'form':form}
        return render(request, 'edit_profile.html', args)

def reset_password(request):
    if request.method == 'POST':
        form = PasswordResetForm(data=request.POST, user=request.user)

        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect(reverse('main:home'))
        else:
            return redirect(reverse('home:reset_password'))
    else:
        form = PasswordChangeForm(user=request.user)
        args = {'form': form}
        return render(request, 'main/reset_password.html', args)

