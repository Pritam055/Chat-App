 
from pydoc import doc
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.generic import CreateView, View, FormView
# from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.contrib.sites.shortcuts import get_current_site 
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import get_user_model

import uuid 

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

class LoginUserView(FormView):
    form_class = UserLoginForm
    template_name = 'accounts/login.html'


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

    