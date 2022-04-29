from django.urls import path 

from . import views 

urlpatterns = [ 
    path('', views.HomeView.as_view(), name='home'),
    path('group_chat/<str:group_name>/', views.GroupChatView.as_view(), name='group_chat'),
    
]