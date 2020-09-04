from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth import login,logout,authenticate
from django.urls import reverse
from django.contrib.auth.forms import UserCreationForm
# usercreationform is django build in form,we can override this in forms.py file


def logout_view(request):
    """Log the user out."""
    logout(request)  # we call build in logout function which requires the request  object as an argument
    return HttpResponseRedirect(reverse('index')) # after successfully logout it redirects 'index' url name,we can also define the redirect in settings in place of view function


def register(request):
    """Register a new user"""
    if request.method != 'POST':
        # display a blank registration form when method when request is get,put etc
        form = UserCreationForm() # usercreationform is django build in form,if the method is not post then we make an instance of UserCreationForm with no initital data
    else:
        form = UserCreationForm(data=request.POST) # make an instance of UserCreationForm based on submitted data,process completed data on request is POST
        if form.is_valid(): # check the username has appropriate characters,the password match and the user isn't trying to do anythin malicious
            new_user = form.save() # the save method returns the newly created user object,which we store in 'new_user'
            # log the user in and then redirect to home page
            # check the username where username for register and then login,and two password which one user type in registration
            authenticated_user = authenticate(username=new_user.username,password=request.POST['password1']) # after save the form to 'new_user' then we check the username and password which is 2 steps process,authenticate() with the arguments new_user.username and their password and matching two password which is given from user in registration
            login(request,authenticated_user)  # call login() function with the request and authenticated_user objects which creates valid session for the new user
            return HttpResponseRedirect(reverse('index'))
    context = {'form':form}
    return render(request,'users/register.html',context)


