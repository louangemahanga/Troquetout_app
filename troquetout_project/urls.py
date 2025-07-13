# troquetout_project/urls.py
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views # Gardez si vous utilisez les vues de reset de mot de passe de Django
# from django.conf import settings # Pas besoin d'importer settings ici, déjà importé via static
from django.conf.urls.static import static 
from django.conf import settings # Importation de settings pour static files
# from troquetout_app import views # Plus besoin d'importer les vues de l'app directement ici si elles sont incluses via include()

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('troquetout_app.urls')), # CECI EST LE CHEMIN PRINCIPAL POUR TOUTES LES URLS DE VOTRE APP

    # --- Nettoyage des URLs en conflit/doublons ---
    # Ces lignes sont supprimées car elles sont déjà définies (et mieux gérées) dans troquetout_app/urls.py
    # path('/logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'), # SUPPRIMÉ : Conflit avec votre vue personnalisée
    # path('accounts/login/', auth_views.LoginView.as_view(template_name='troquetout_app/login.html'), name='login'), # SUPPRIMÉ : Vous avez déjà une vue login dans votre app
    # path('search/', views.search_annonces, name='search_annonces'), # SUPPRIMÉ : Déjà dans troquetout_app/urls.py
    # --- Fin du nettoyage ---

    # --- Vues de réinitialisation de mot de passe (gérées par Django, elles peuvent rester ici) ---
    path('accounts/password_reset/',
         auth_views.PasswordResetView.as_view(
             template_name='troquetout_app/password_reset_form.html',
             email_template_name='troquetout_app/password_reset_email.html',
             subject_template_name='troquetout_app/password_reset_subject.txt'
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
    # --- Fin des vues de réinitialisation ---
]

# Servir les fichiers médias en mode développement
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)