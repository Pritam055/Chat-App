from django.urls import path  

from . import views 

urlpatterns = [ 
    path('signup/', views.CreateUserView.as_view(), name='signup'),
    path('logout/', views.logout_user, name='logout'),
    path('login/', views.LoginUserView.as_view(), name='login'),
    path('activate/<str:token>/', views.ActivateUserToken.as_view(), name='activate_token' ),
    
]