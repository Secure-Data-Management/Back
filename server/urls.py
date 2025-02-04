from django.urls import path
from server import views


app_name = 'backend'
urlpatterns = [
    path('', views.home, name='home'),
    path('keys/get_params', views.get_params, name='get_params'),
    path('keys/get_generator', views.get_generator, name='get_generator'),
    path('keys/add_key', views.add_key, name='add_key'),
    path('keys/get_key', views.get_key, name='get_key'),
    path('keys/get_users', views.get_users, name='get_users'),
    path('keys/get_username', views.get_username, name='get_username'),
    path('file/upload', views.upload, name='upload'),
    path('search', views.search, name="search")
]