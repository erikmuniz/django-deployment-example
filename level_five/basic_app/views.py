from django.shortcuts import render
from basic_app.forms import UserForm, UserProfileInfoForm

# ALL THESE IMPORTS REQUIRED FOR USER LOGIN/LOGOUT
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    return render(request, 'basic_app/index.html')

@login_required
def special(request):
    return HttpResponse("You are logged in, Nice!")

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

def register(request):
    # Assume user is NOT registered if clicked this link
    registered = False

    # Check if user submits info
    if request.method == "POST":
        # Grab info off both forms, store in these variables
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)

        # Check if info on forms is valid
        if user_form.is_valid() and profile_form.is_valid():
            # Grab everything from base user form
            user = user_form.save()
            user.set_password(user.password)
            # Save
            user.save()

            # Grab from profile form
            profile = profile_form.save(commit=False)
            profile.user = user
            # Check to see if picture in profile form
            if 'profile_pic' in request.FILES:
                profile.profile_pic = request.FILES['profile_pic']
            # Save
            profile.save()

            # Registered now true
            registered = True
        else:
            # Print errors if info in one of forms not valid
            print(user_form.errors, profile_form.errors)
    else:
        # NO REQUEST YET, METHOD != POST
        # SET THE FORMS
        user_form = UserForm()
        profile_form = UserProfileInfoForm()

    return render(request, 'basic_app/registration.html',
                  {'user_form': user_form,
                  'profile_form':profile_form,
                  'registered':registered})

def user_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Built-in Django function to authenticate user
        user = authenticate(username=username, password=password)

        # If user is authenticated...
        if user:
            # Check if account is active (accounts deactivate over long time periods)
            if user.is_active:
                # Log user in (simple built in django function)
                login(request, user)
                # Once logged in, send user to different page (here: index)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse("ACCOUNT NOT ACTIVE")
        else:
            print("Someone tried to login and failed!")
            # Print username entered and password entered to console
            print("Username: {} and password {}".format(username, password))
            return HttpResponse("INVALID LOGIN DETAILS SUPPLIED")
    else:
        # Display login screen
        return render(request, 'basic_app/login.html', {})
