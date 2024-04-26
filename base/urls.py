from django.urls import path
from django.views.generic.base import TemplateView

from base import views
from server.config import ALLOWED_HOST

urlpatterns = [
    path('', views.home, name='home'),
    path('docs/', TemplateView.as_view(template_name='docs.html', extra_context={'title': 'Docs','url':ALLOWED_HOST}), name='docs'),
    path('error/', TemplateView.as_view(template_name='error.html', extra_context={'title': 'Oops!'}), name='error'),
    path('register/', views.register, name='register'),
    path('resetpassword/', views.resetpassword, name='resetpassword'),
    path('login/', views.login, name='login'),
    path('logoff/', views.logoff, name='logoff'),
    path('token/', views.token, name='token'),
    path('sketch/', views.sketch, name='sketch'),
]
