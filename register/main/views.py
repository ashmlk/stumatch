from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, redirect
from .forms import SignUpForm
from django.contrib import messages

def main_page(request):
    return render(request,'login.html')

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
            user.refresh_from_db()  # load the profile instance created by the signal
            user.profile.university = form.cleaned_data.get('university')
            user.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            #user_login(request, user)
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
                return HttpResponseRedirect('home')
            else:
                message = 'Sorry, the username or password you entered is not valid please try again.'
                return render(request, 'login.html', {'message':message})
        else:
            message = 'Sorry, the username or password you entered is not valid please try again.'
            return render(request, 'login.html', {'message':message})
    else:
        form=AuthenticationForm()
        return render(request, 'login.html', {"form":form})

# inside views.py
def create(response):
    if response.method == "POST":
	    form = CreateNewList(response.POST)

    if form.is_valid():
	    n = form.cleaned_data["name"]
	    c = Course(name=n)
	    c.save()
	    response.user.course.add(c)  # adds the course to the current logged in user

	    return HttpResponseRedirect("/%i" %c.id)

    else:
        form = CreateNewList()

    return render(response, "main/create.html", {"form":form})

#shows the users courses for specific users
def user_index(response, id):
    ls = Course.objects.get(id=id)
 
    if response.method == "POST":
	    if response.POST.get("save"):
		    item.save()
 
    elif response.POST.get("newItem"):
	    txt = response.POST.get("new")
 
	    if len(txt) > 2:
	        ls.item_set.create(text=txt, complete=False)
	    else:
	        print("invalid")
 
    return render(response, "main/list.html", {"ls":ls})