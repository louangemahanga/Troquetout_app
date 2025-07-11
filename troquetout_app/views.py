# troquetout_app/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate, get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from django.core.mail import send_mail
from django.views.decorators.http import require_POST
from django.views.generic import View
from django.http import JsonResponse # Pour des réponses JSON si besoin, ou simplement redirect
from django.db import transaction 

# Importez tous vos modèles en une seule ligne propre
from .models import Annonce, Categorie, ContactMessage, NewsletterSubscriber, AnnonceLikeDislike, Commentaire, Proposition, Profile
from django.views.decorators.http import require_http_methods #

# Importez tous vos formulaires. Assurez-vous que tous ces formulaires sont définis dans forms.py
from .forms import (
    AnnonceForm,
    InscriptionForm,
    SearchForm,
    ContactForm,
    NewsletterSubscriptionForm,
    CommentaireForm,
    UserProfileEditForm,
    PropositionForm # Assurez-vous que PropositionForm est importé
)

# Obtenez le modèle User
User = get_user_model()


# --- Vues Fonctionnelles ---

def index(request):
    annonces = Annonce.objects.all().order_by('-date_publication')[:8]
    newsletter_form = NewsletterSubscriptionForm()
    
    context = {
        'annonces': annonces,
        'newsletter_form': newsletter_form,
    }
    return render(request, 'troquetout_app/index.html', context)


def liste_annonces(request):
    annonces = Annonce.objects.all().order_by('-date_publication')
    return render(request, 'troquetout_app/liste_annonces.html', {'annonces': annonces})


def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            ContactMessage.objects.create(
                nom=form.cleaned_data['nom'],
                email=form.cleaned_data['email'],
                sujet=form.cleaned_data['sujet'],
                message=form.cleaned_data['message']
            )
            messages.success(request, 'Votre message a été envoyé avec succès !')
            return redirect('contact')
    else:
        form = ContactForm()

    context = {
        'form': form
    }
    return render(request, 'troquetout_app/contact.html', context)


def register(request):
    if request.method == 'POST':
        form = InscriptionForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Inscription réussie ! Bienvenue sur TroqueTout.")
            return redirect('home')
        else:
            messages.error(request, "Erreur lors de l'inscription. Veuillez corriger les erreurs.")
    else:
        form = InscriptionForm()
    return render(request, 'troquetout_app/signup.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Bienvenue, {username} !")
                return redirect('home')
            else:
                messages.error(request, "Nom d'utilisateur ou mot de passe invalide.")
        else:
            messages.error(request, "Nom d'utilisateur ou mot de passe invalide.")
    else:
        form = AuthenticationForm()
    return render(request, 'troquetout_app/login.html', {'form': form})


@login_required
def logout_view(request):
    logout(request)
    messages.info(request, "Vous avez été déconnecté avec succès.")
    return redirect('logout_success')


@login_required
def detail_annonce(request, pk):
    annonce = get_object_or_404(Annonce, pk=pk)
    
    likes_count = annonce.likes_dislikes.filter(is_like=True).count()
    dislikes_count = annonce.likes_dislikes.filter(is_like=False).count()
    
    user_interaction = None
    if request.user.is_authenticated:
        try:
            user_interaction = AnnonceLikeDislike.objects.get(annonce=annonce, user=request.user)
        except AnnonceLikeDislike.DoesNotExist:
            pass

    commentaires = annonce.commentaires.all()
    
    if request.method == 'POST':
        commentaire_form = CommentaireForm(request.POST)
        if commentaire_form.is_valid():
            if request.user.is_authenticated:
                nouveau_commentaire = commentaire_form.save(commit=False)
                nouveau_commentaire.annonce = annonce
                nouveau_commentaire.user = request.user
                nouveau_commentaire.save()
                messages.success(request, 'Votre commentaire a été ajouté avec succès !')
                return redirect('detail_annonce', pk=annonce.pk)
            else:
                messages.error(request, 'Vous devez être connecté pour commenter.')
                return redirect('login')
    else:
        commentaire_form = CommentaireForm()

    context = {
        'annonce': annonce,
        'likes_count': likes_count,
        'dislikes_count': dislikes_count,
        'user_interaction': user_interaction,
        'commentaires': commentaires,
        'commentaire_form': commentaire_form,
    }
    return render(request, 'troquetout_app/detail_annonce.html', context)


@login_required
@require_POST
def like_dislike_annonce(request, pk):
    annonce = get_object_or_404(Annonce, pk=pk)
    action = request.POST.get('action')

    existing_interaction = AnnonceLikeDislike.objects.filter(annonce=annonce, user=request.user).first()

    if action == 'like':
        if existing_interaction and existing_interaction.is_like:
            existing_interaction.delete()
            messages.info(request, "Votre 'J'aime' a été retiré.")
        elif existing_interaction and not existing_interaction.is_like:
            existing_interaction.is_like = True
            existing_interaction.save()
            messages.success(request, "Vous aimez cette annonce !")
        else:
            AnnonceLikeDislike.objects.create(annonce=annonce, user=request.user, is_like=True)
            messages.success(request, "Vous aimez cette annonce !")
    
    elif action == 'dislike':
        if existing_interaction and not existing_interaction.is_like:
            existing_interaction.delete()
            messages.info(request, "Votre 'Je n'aime pas' a été retiré.")
        elif existing_interaction and existing_interaction.is_like:
            existing_interaction.is_like = False
            existing_interaction.save()
            messages.success(request, "Vous n'aimez pas cette annonce.")
        else:
            AnnonceLikeDislike.objects.create(annonce=annonce, user=request.user, is_like=False)
            messages.success(request, "Vous n'aimez pas cette annonce.")
    else:
        messages.error(request, "Action invalide.")

    return redirect('detail_annonce', pk=pk)


@login_required
def creer_proposition(request, pk):
    annonce_cible = get_object_or_404(Annonce, pk=pk)

    # Vérifier que l'utilisateur ne propose pas sa propre annonce
    if annonce_cible.auteur == request.user: # Changé 'utilisateur' en 'auteur' pour correspondre à votre modèle Annonce
        messages.error(request, "Vous ne pouvez pas faire de proposition sur votre propre annonce.")
        return redirect('detail_annonce', pk=annonce_cible.pk)

    if request.method == 'POST':
        form = PropositionForm(request.POST)
        # Filtrer le queryset pour n'afficher que les annonces de l'utilisateur connecté
        # Changé 'utilisateur' en 'auteur' ici aussi
        form.fields['annonce_proposee'].queryset = Annonce.objects.filter(auteur=request.user)

        if form.is_valid():
            proposition = form.save(commit=False)
            proposition.propose_par = request.user
            proposition.annonce_cible = annonce_cible
            proposition.statut = 'en_attente' # Définir le statut initial
            proposition.save()

            messages.success(request, "Votre proposition de troc a été envoyée avec succès !")
            return redirect('mes_propositions') # Rediriger l'utilisateur vers ses propositions
        else:
            messages.error(request, "Veuillez corriger les erreurs dans le formulaire.")
    else:
        form = PropositionForm()
        # Filtrer le queryset pour n'afficher que les annonces de l'utilisateur connecté
        # Changé 'utilisateur' en 'auteur' ici aussi
        form.fields['annonce_proposee'].queryset = Annonce.objects.filter(auteur=request.user) # Supprimé 'disponible=True' car ce n'est pas un champ dans votre modèle Annonce. Ajoutez-le si vous en créez un.

    context = {
        'annonce_cible': annonce_cible,
        'form': form,
    }
    return render(request, 'troquetout_app/creer_proposition.html', context)


# --- Vues Basées sur les Classes (Class-Based Views) ---

class AnnonceCreateView(LoginRequiredMixin, CreateView):
    model = Annonce
    form_class = AnnonceForm
    template_name = 'troquetout_app/creer_annonce.html'
    success_url = reverse_lazy('liste_annonces')

    def form_valid(self, form):
        form.instance.auteur = self.request.user
        messages.success(self.request, "Votre annonce a été créée avec succès !")
        return super().form_valid(form)


class AnnonceUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Annonce
    form_class = AnnonceForm
    template_name = 'troquetout_app/modifier_annonce.html'
    context_object_name = 'annonce'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        return obj

    def test_func(self):
        user_is_owner = self.get_object().auteur == self.request.user
        return user_is_owner

    def get_success_url(self):
        url = reverse_lazy('detail_annonce', kwargs={'pk': self.object.pk})
        return url


def search_annonces(request):
    all_categories = Categorie.objects.all().order_by('nom')
    form = SearchForm(request.GET, categories=all_categories)
    annonces = Annonce.objects.all().order_by('-date_publication')

    if form.is_valid():
        query = form.cleaned_data.get('query')
        category = form.cleaned_data.get('category')

        if query:
            annonces = annonces.filter(
                Q(titre__icontains=query) | Q(description__icontains=query)
            ).distinct()

        if category:
            annonces = annonces.filter(categorie=category)
    
    context = {
        'form': form,
        'annonces': annonces,
    }
    return render(request, 'troquetout_app/search_results.html', context)


@require_POST
def subscribe_newsletter(request):
    form = NewsletterSubscriptionForm(request.POST)
    if form.is_valid():
        try:
            form.save()
            messages.success(request, 'Merci de vous être abonné à notre newsletter !')
            return redirect('subscription_success')
        except Exception as e:
            if 'unique constraint' in str(e).lower():
                messages.warning(request, 'Cette adresse email est déjà abonnée.')
            else:
                messages.error(request, 'Une erreur est survenue lors de votre abonnement. Veuillez réessayer.')
            return redirect('home')
    else:
        messages.error(request, 'Veuillez entrer une adresse email valide pour vous abonner.')
        return redirect('home')

def subscription_success(request):
    return render(request, 'troquetout_app/subscription_success.html')


class AnnonceDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Annonce
    template_name = 'troquetout_app/annonce_confirm_delete.html'
    success_url = reverse_lazy('liste_annonces')

    def test_func(self):
        return self.get_object().auteur == self.request.user
    
class LogoutSuccessView(TemplateView):
    template_name = 'troquetout_app/logout_success.html'

class UserProfileView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'troquetout_app/profile.html'
    context_object_name = 'user_profile'

    def get_object(self):
        pk = self.kwargs.get('pk')
        if pk:
            user_obj = get_object_or_404(User, pk=pk)
            return user_obj
        else:
            return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['user_announcements'] = Annonce.objects.filter(auteur=self.get_object()).order_by('-date_publication')
        
        try:
            context['profile_data'] = self.get_object().profile
        except User.profile.RelatedObjectDoesNotExist:
            context['profile_data'] = None
            
        return context

class UserProfileUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Profile
    form_class = UserProfileEditForm
    template_name = 'troquetout_app/modifier_profil.html'
    
    def get_object(self, queryset=None):
        return self.request.user.profile

    def get_success_url(self):
        return reverse_lazy('my_profile')

    def test_func(self):
        return self.request.user == self.get_object().user

    def form_valid(self, form):
        messages.success(self.request, "Votre profil a été mis à jour avec succès !")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Une erreur est survenue lors de la mise à jour de votre profil. Veuillez vérifier les informations saisies.")
        return super().form_invalid(form)


class FAQHelpView(TemplateView):
    template_name = 'troquetout_app/faq_aide.html'
    
class LicenseView(TemplateView):
    template_name = 'troquetout_app/license.html'

class PrivacyPolicyView(TemplateView):
    template_name = 'troquetout_app/privacy_policy.html'

class TermsOfServiceView(TemplateView):
    template_name = 'troquetout_app/terms_of_service.html'
    
class MesAnnoncesView(LoginRequiredMixin, ListView):
    model = Annonce
    template_name = 'troquetout_app/mes_annonces.html'
    context_object_name = 'annonces'

    def get_queryset(self):
        return Annonce.objects.filter(auteur=self.request.user).order_by('-date_publication')


class MesPropositionsView(LoginRequiredMixin, ListView):
    model = Proposition # <-- Changé de PropositionTroc
    template_name = 'troquetout_app/mes_propositions.html'
    context_object_name = 'propositions'

    def get_queryset(self):
        user = self.request.user
        return Proposition.objects.filter( # <-- Changé de PropositionTroc
            Q(propose_par=user) | Q(annonce_cible__auteur=user)
        ).select_related('propose_par', 'annonce_proposee', 'annonce_cible').distinct()
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
@login_required
@require_POST # S'assurer que cette vue n'est appelée que via une requête POST
def annuler_proposition(request, pk):
    proposition = get_object_or_404(Proposition, pk=pk)

    # L'utilisateur ne peut annuler que ses propres propositions en attente
    if proposition.propose_par == request.user and proposition.statut == 'en_attente':
        proposition.statut = 'annulee'
        proposition.save()
        messages.success(request, "La proposition a été annulée avec succès.")
    else:
        messages.error(request, "Vous n'êtes pas autorisé à annuler cette proposition ou elle n'est plus en attente.")
    
    return redirect('mes_propositions') # Rediriger l'utilisateur vers la liste de ses propositions

@login_required
@require_POST # Généralement, les actions de statut sont POST
def accepter_proposition(request, pk):
    proposition = get_object_or_404(Proposition, pk=pk)

    # L'utilisateur peut accepter la proposition s'il est l'auteur de l'annonce ciblée
    # et si le statut est 'en_attente'
    if proposition.annonce_cible.auteur == request.user and proposition.statut == 'en_attente':
        with transaction.atomic(): # Utiliser une transaction pour des mises à jour atomiques
            proposition.statut = 'acceptee'
            proposition.save()

            # Mettre à jour les statuts des annonces impliquées si nécessaire
            # Par exemple, si une proposition est acceptée, les annonces ne sont plus disponibles
            proposition.annonce_cible.statut = 'ECHANGE' # Ou 'FERME'
            proposition.annonce_cible.save()
            proposition.annonce_proposee.statut = 'ECHANGE' # Ou 'FERME'
            proposition.annonce_proposee.save()

            # Refuser automatiquement les autres propositions pour l'annonce ciblée
            # ou pour l'annonce proposée si elles sont en attente
            Proposition.objects.filter(
                Q(annonce_cible=proposition.annonce_cible) | Q(annonce_proposee=proposition.annonce_proposee)
            ).exclude(pk=proposition.pk).filter(statut='en_attente').update(statut='refusee')

            messages.success(request, "La proposition a été acceptée avec succès ! Les annonces sont marquées comme échangées.")
    else:
        messages.error(request, "Vous n'êtes pas autorisé à accepter cette proposition ou elle n'est plus en attente.")

    return redirect('mes_propositions')


@login_required
@require_POST # Généralement, les actions de statut sont POST
def refuser_proposition(request, pk):
    proposition = get_object_or_404(Proposition, pk=pk)

    # L'utilisateur peut refuser la proposition s'il est l'auteur de l'annonce ciblée
    # et si le statut est 'en_attente'
    if proposition.annonce_cible.auteur == request.user and proposition.statut == 'en_attente':
        proposition.statut = 'refusee'
        proposition.save()
        messages.info(request, "La proposition a été refusée.")
    else:
        messages.error(request, "Vous n'êtes pas autorisé à refuser cette proposition ou elle n'est plus en attente.")

    return redirect('mes_propositions')



@login_required
@require_http_methods(["GET", "POST"]) # Permettre les requêtes GET pour afficher le formulaire et POST pour soumettre
def modifier_proposition(request, pk):
    proposition = get_object_or_404(Proposition, pk=pk)

    # Assurez-vous que l'utilisateur est le proposeur et que la proposition est en attente
    if proposition.propose_par != request.user or proposition.statut != 'en_attente':
        messages.error(request, "Vous ne pouvez pas modifier cette proposition.")
        return redirect('mes_propositions')

    if request.method == 'POST':
        form = PropositionForm(request.POST, instance=proposition)
        # Re-filtrez le queryset pour l'annonce proposée pour l'utilisateur actuel
        form.fields['annonce_proposee'].queryset = Annonce.objects.filter(auteur=request.user).exclude(pk=proposition.annonce_cible.pk)
        if form.is_valid():
            form.save()
            messages.success(request, "Votre proposition a été modifiée avec succès !")
            return redirect('mes_propositions')
    else:
        form = PropositionForm(instance=proposition)
        # Re-filtrez le queryset pour l'annonce proposée pour l'utilisateur actuel
        form.fields['annonce_proposee'].queryset = Annonce.objects.filter(auteur=request.user).exclude(pk=proposition.annonce_cible.pk)

    context = {
        'form': form,
        'proposition': proposition,
        'annonce_cible': proposition.annonce_cible, # Utile pour afficher le titre de l'annonce ciblée
    }
    return render(request, 'troquetout_app/modifier_proposition.html', context) # Nous créerons ce template à l'étape 3