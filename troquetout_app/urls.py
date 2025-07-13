# troquetout_app/urls.py
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Annonces
    path('annonces/', views.liste_annonces, name='liste_annonces'),
    path('annonces/creer/', views.AnnonceCreateView.as_view(), name='creer_annonce'),
    path('annonces/<int:pk>/', views.detail_annonce, name='detail_annonce'),
    path('annonces/<int:pk>/modifier/', views.AnnonceUpdateView.as_view(), name='modifier_annonce'),
    path('annonces/<int:pk>/supprimer/', views.AnnonceDeleteView.as_view(), name='supprimer_annonce'),
    path('annonces/<int:pk>/proposer/', views.creer_proposition, name='creer_proposition'),
    path('annonces/<int:pk>/like-dislike/', views.like_dislike_annonce, name='like_dislike_annonce'), # Si vous l'utilisez, elle est correcte.

    # Recherche
    path('search/', views.search_annonces, name='search_annonces'), # C'est le chemin correct pour la recherche

    # Authentification
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'), # C'est le chemin correct pour votre vue login
    path('logout/', views.logout_view, name='logout'), # C'est le chemin correct pour votre vue logout

    # Contact & Newsletter
    path('contact/', views.contact_view, name='contact'),
    path('subscribe/', views.subscribe_newsletter, name='subscribe_newsletter'),
    path('subscription-success/', views.subscription_success, name='subscription_success'),
    
    # Nouvelle URL pour la page de succès de déconnexion (si vous la gardez, sinon elle peut être supprimée)
    # path('logout-success/', views.LogoutSuccessView.as_view(), name='logout_success'), 
    # Note: Votre logout_view redirige déjà vers 'home', donc cette vue de succès n'est peut-être pas utilisée.

    # Profil Utilisateur
    path('profile/<int:pk>/', views.UserProfileView.as_view(), name='profile'),
    path('profile/', views.UserProfileView.as_view(), name='my_profile'), 
    path('profile/modifier/', views.UserProfileUpdateView.as_view(), name='modifier_profil'),
    path('profile/mes-annonces/', views.MesAnnoncesView.as_view(), name='mes_annonces'),
    path('profile/mes-propositions/', views.MesPropositionsView.as_view(), name='mes_propositions'),
    
    # Gestion des propositions
    path('propositions/<int:pk>/annuler/', views.annuler_proposition, name='annuler_proposition'),
    path('propositions/<int:pk>/accepter/', views.accepter_proposition, name='accepter_proposition'),
    path('propositions/<int:pk>/refuser/', views.refuser_proposition, name='refuser_proposition'),
    path('propositions/<int:pk>/modifier/', views.modifier_proposition, name='modifier_proposition'),

    # Pages Statiques
    path('faq-aide/', views.FAQHelpView.as_view(), name='faq_aide'),
    path('license/', views.LicenseView.as_view(), name='license'),
    path('politique-confidentialite/', views.PrivacyPolicyView.as_view(), name='privacy_policy'),
    path('conditions-utilisation/', views.TermsOfServiceView.as_view(), name='terms_of_service'),

    # Page d'accueil (doit être la dernière pour éviter de surcharger d'autres URL)
    path('', views.index, name='home'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)