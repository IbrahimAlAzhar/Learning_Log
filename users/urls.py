"""Define URL patterns for users"""
from django.conf.urls import url
from django.contrib.auth.views import login # import django build in login
from django.urls import path

from . import views

urlpatterns = [
    path('login/',login, {'template_name': 'users/login.html'},name='login'), # here view argument is 'login' not views.login,because we're not writing our own view function,we pass a dictionary telling django where to find the template, here use django build in login,we can use django build in login without view function and url also,
    # in build in django search the template in 'registration' folder inside the template folder,here we override this
    path('logout/',views.logout_view,name='logout'), # here we override the logout url and override the view function,if we don't want to create these no problem,django automatically handles 'logout' url and template is 'registration/logout'
    path('register/',views.register,name='register'), # django build in can't create registration only,so we have to create view function,but we use build in 'usercreationform'
]