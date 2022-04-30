 
from pydoc import doc
from click import password_option
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.generic import View
# from django.contrib.auth.models import User 
from django.contrib.sites.shortcuts import get_current_site 
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from django.contrib.auth import get_user_model, authenticate, login, logout

import uuid

from requests import JSONDecodeError 

from accounts.forms import UserCreationForm, UserLoginForm
from accounts.tasks import send_mail_task
# Create your views here.

User = get_user_model()

class CreateUserView(View):

    def get(self, request):    
        return render(request, 'accounts/signup.html', {
            'form': UserCreationForm()
        })

    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid(): 
            obj = form.save(commit=False)
            # print(form.cleaned_data)
            current_site = get_current_site(request)
            token = str(uuid.uuid4())
            domain = current_site.domain
            protocol = "http"
            # url = protocol + '://' + domain + '/accounts/activate/' + token + '/'
            url = protocol + '://' + domain + reverse('activate_token', kwargs={'token': token})
            # print(url)
            obj.token = token 
            obj.save()
            send_mail_task.delay(obj.username, obj.email, url)

            return JsonResponse({'status': True}, status=200)
        print(form.errors)
        return JsonResponse({
           'errors': form.errors,
           'status': False, 
        }, status=200)


def logout_user(request):
    logout(request)
    return redirect('home')

class LoginUserView(View):

    def get(self, request, *args, **kwargs):
        form_class = UserLoginForm
        return render(request, 'accounts/login.html', {
            'form': form_class
        }) 

    def post(self, request, *args, **kwargs): 
        form = UserLoginForm(request.POST)
        if form.is_valid(): 
            print(form.cleaned_data.get('username'), form.cleaned_data.get('password'))
            user = authenticate(username=form.cleaned_data.get('username'), password=form.cleaned_data.get('password'))
            print(user)
            if user:
                login(self.request, user)
                return JsonResponse({'status': True}, status=200)
        print(form.errors)
        return JsonResponse({'status': False}, status=200)
    
class ActivateUserToken(View):

    def get(self, request, *args, **kwargs):
        token = kwargs.get('token') 
        user = User.objects.filter(token=token)
        if user.exists():
            user_obj = user.first()
            user_obj.activated = True 
            user_obj.save()
            messages.success(request, f'{user_obj.username}\'s account is activated successfully.')
        else:
            messages.warning(request, f'Invalid token')
        return redirect('home')

    