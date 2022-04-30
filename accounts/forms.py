from django import forms as django_forms
from django.contrib.auth import forms, models 
from django.contrib.auth import get_user_model 

User  = get_user_model()


class UserCreationForm(django_forms.ModelForm):

    class Meta:
        model = User
        fields = ('username', 'email', 'password')  
        widgets = {
            'password' : django_forms.PasswordInput(),
        }

    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        self.fields['email'].required = True 

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if User.objects.filter(username__iexact=username):
            self.add_error('username', 'A user with username already exists.')
        return username 

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email__iexact=email):
            self.add_error('email', 'A user with email already exists.')
        return email.lower()


    # def clean(self, *args, **kwargs): 
    #     cleaned_data = super().clean() 
    
class UserLoginForm(django_forms.Form):
    username = django_forms.CharField(max_length=200)
    password = django_forms.CharField(max_length=200, widget=django_forms.PasswordInput())
 

    