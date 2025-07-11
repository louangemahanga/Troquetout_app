# troquetout_app/urls.py
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Annonces
    path('annonces/', views.liste_annonces, name='liste_annonces'),
    path('annonces/creer/', views.AnnonceCreateView.as_view(), name='creer_annonce'), # CORRIGÉ
    path('annonces/<int:pk>/', views.detail_annonce, name='detail_annonce'),
    path('annonces/<int:pk>/modifier/', views.AnnonceUpdateView.as_view(), name='modifier_annonce'), # CORRIGÉ
    path('annonces/<int:pk>/supprimer/', views.AnnonceDeleteView.as_view(), name='supprimer_annonce'), # CORRIGÉ
    path('annonces/<int:pk>/proposer/', views.creer_proposition, name='creer_proposition'),
    # path('annonces/<int:pk>/like-dislike/', views.like_dislike_annonce, name='like_dislike_annonce'), # Si vous la décommentez, elle fonctionnera avec la vue corrigée.

    # Recherche
    path('search/', views.search_annonces, name='search_annonces'),

    # Authentification
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Contact & Newsletter
    path('contact/', views.contact_view, name='contact'),
    path('subscribe/', views.subscribe_newsletter, name='subscribe_newsletter'),
    path('subscription-success/', views.subscription_success, name='subscription_success'),

    # Page d'accueil (doit être la dernière pour éviter de surcharger d'autres URL)
    path('', views.index, name='home'),
    # Assurez-vous que le nom est 'subscription_success' et qu'il pointe vers la bonne vue
    path('abonnement/succes/', views.subscription_success, name='subscription_success'),

    # Et la vue qui traite le formulaire d'abonnement (si elle n'est pas déjà là)
    path('abonnement/subscribe/', views.subscribe_newsletter, name='subscribe_newsletter'),
    # path('logout/', views.logout_view, name='logout'), # Conservez celle-ci

    # Nouvelle URL pour la page de succès de déconnexion
    # troquetout_app/urls.py

# ... autres importations et URLs ...

# C'est cette ligne que vous devez modifier :
    path('profile/<int:pk>/', views.UserProfileView.as_view(), name='profile'), # <-- Correction ici !
    path('profile/', views.UserProfileView.as_view(), name='my_profile'), 
    path('faq-aide/', views.FAQHelpView.as_view(), name='faq_aide'),
    path('license/', views.LicenseView.as_view(), name='license'),
    path('politique-confidentialite/', views.PrivacyPolicyView.as_view(), name='privacy_policy'),
    path('conditions-utilisation/', views.TermsOfServiceView.as_view(), name='terms_of_service'),
    path('profile/modifier/', views.UserProfileUpdateView.as_view(), name='modifier_profil'), # <-- Nouvelle URL !
    path('profile/mes-annonces/', views.MesAnnoncesView.as_view(), name='mes_annonces'), # <-- Nouvelle URL !
    path('profile/mes-propositions/', views.MesPropositionsView.as_view(), name='mes_propositions'),
    path('propositions/<int:pk>/annuler/', views.annuler_proposition, name='annuler_proposition'),
    path('propositions/<int:pk>/accepter/', views.accepter_proposition, name='accepter_proposition'),
    path('propositions/<int:pk>/refuser/', views.refuser_proposition, name='refuser_proposition'),
    # URLs pour la gestion des propositions
    path('propositions/<int:pk>/annuler/', views.annuler_proposition, name='annuler_proposition'),
    path('propositions/<int:pk>/accepter/', views.accepter_proposition, name='accepter_proposition'),
    path('propositions/<int:pk>/refuser/', views.refuser_proposition, name='refuser_proposition'),
     path('propositions/<int:pk>/modifier/', views.modifier_proposition, name='modifier_proposition'), # <-- Nouvelle URL

]



if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)