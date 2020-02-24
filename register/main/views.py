from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from .forms import SignUpForm
from django.contrib import messages

def index(request):
    return render(request,'index.html')

def home(request):
    return render(request,'home.html')

def view(response):
    return render(response, "main/view.html", {})

@login_required
def special(request):
    return HttpResponse("You are logged in !")

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

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
            return redirect('index')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse('Account has been inactive')
        else:
            message = 'Sorry, the username or password you entered is not valid please try again.'
            return render(request, 'index.html', {'message':message})
    else:
        return render(request, 'index.html', {})
    
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