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

@login_required
def user_logout(request):
    logout(request)
    return redirect('main:user_login')
    
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            return redirect('main:user_login')
    else:
        form = SignUpForm()
    return render(request, 'main/signup.html', {'form': form})

def user_login(request):
    message = ''
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return redirect('home:home')
            else:
                HttpResponse('Account is disabled')
        if user is None:
            message = 'Sorry the username or password you entered is incorrect please try again'
    else:
        message = ''
    return render(request, 'main/user_login.html', {'message': message})

@login_required
def edit_profile(request):
    if request.method=='POST':
        form = EditProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            #return redirect('main:home')
            return redirect(reverse('home:home')) 
    else:
        form = EditProfileForm(instance=request.user)
        args = {'form':form}
        return render(request, 'main/edit_profile.html', args)


# This is for handling friend requests

@login_required
def send_friend_request(request, id):
	if request.user.is_authenticated():
		user = get_object_or_404(User, id=id)
		frequest, created = FriendRequest.objects.get_or_create(
			from_user=request.user,
			to_user=user)
		return HttpResponseRedirect('/users')

@login_required
def cancel_friend_request(request, id):
	if request.user.is_authenticated():
		user = get_object_or_404(User, id=id)
		frequest = FriendRequest.objects.filter(
			from_user=request.user,
			to_user=user).first()
		frequest.delete()
		return HttpResponseRedirect('/users')

@login_required
def accept_friend_request(request, id):
	from_user = get_object_or_404(User, id=id)
	frequest = FriendRequest.objects.filter(from_user=from_user, to_user=request.user).first()
	user1 = frequest.to_user
	user2 = from_user
	user1.profile.friends.add(user2.profile)
	user2.profile.friends.add(user1.profile)
	frequest.delete()
	return HttpResponseRedirect('/users/{}'.format(request.user.profile.slug))

@login_required
def delete_friend_request(request, id):
	from_user = get_object_or_404(User, id=id)
	frequest = FriendRequest.objects.filter(from_user=from_user, to_user=request.user).first()
	frequest.delete()
	return HttpResponseRedirect('/users/{}'.format(request.user.profile.slug))