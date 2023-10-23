from django.contrib.auth import views as authViews
from django.urls import path

from .views import user_login

urlpatterns = [
    path('login/', user_login, name="login"),
    path('exit/', authViews.LogoutView.as_view(next_page='/accounts/login/'), name='exit'),
]
