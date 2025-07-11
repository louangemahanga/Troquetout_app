# troquetout_project/urls.py
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views # Importe les vues d'authentification de Django
from django.conf import settings # Pour les fichiers médias
from django.conf.urls.static import static # Pour les fichiers médias
from troquetout_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('troquetout_app.urls')), # Inclut les URLs de ton application
    path('search/', views.search_annonces, name='search_annonces'), #
    

    # Personnalisation des vues de réinitialisation de mot de passe
    path('accounts/password_reset/',
         auth_views.PasswordResetView.as_view(
             template_name='troquetout_app/password_reset_form.html',
             email_template_name='troquetout_app/password_reset_email.html', # Notre template d'email
             subject_template_name='troquetout_app/password_reset_subject.txt' # Si tu veux personnaliser l'objet de l'email
         ),
         name='password_reset'),
    path('accounts/password_reset/done/',
         auth_views.PasswordResetDoneView.as_view(template_name='troquetout_app/password_reset_done.html'),
         name='password_reset_done'),
    path('accounts/reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='troquetout_app/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('accounts/reset/done/',
         auth_views.PasswordResetCompleteView.as_view(template_name='troquetout_app/password_reset_complete.html'),
         name='password_reset_complete'),

    # Ajoute les URLs pour la connexion et déconnexion si elles ne sont pas déjà dans troquetout_app.urls
    path('accounts/login/', auth_views.LoginView.as_view(template_name='troquetout_app/login.html'), name='login'), # Assurez-vous que login.html existe
    path('/logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'), # Redirige vers la page d'accueil après déconnexion
]

# Servir les fichiers médias en mode développement
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)