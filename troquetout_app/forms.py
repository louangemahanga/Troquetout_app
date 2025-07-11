# troquetout_app/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model
from .models import Annonce, Categorie, NewsletterSubscriber, Commentaire, ContactMessage, Profile, Proposition # Assurez-vous que Profile et Proposition sont importés !

User = get_user_model()

class AnnonceForm(forms.ModelForm):
    class Meta:
        model = Annonce
        fields = [
            'titre',
            'description',
            'categorie',
            'image',
            'valeur_estimee',
            'type_annonce',
            'localisation',
            'contact_telephone',
            'contact_email',
            'adresse',
            'statut',
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }
        labels = {
            'titre': 'Titre de l\'annonce',
            'description': 'Description de l\'objet',
            'categorie': 'Catégorie existante',
            'image': 'Image (optionnel)',
            'valeur_estimee': 'Valeur estimée (en € si vente, indicative si échange)',
            'type_annonce': 'Type d\'annonce',
            'localisation': 'Lieu de l\'objet (ville, code postal)',
            'contact_telephone': 'Téléphone de contact',
            'contact_email': 'Email de contact',
            'adresse': 'Adresse de l\'échange',
            'statut': 'Statut de l\'annonce',
        }


class InscriptionForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text='Obligatoire. Saisissez une adresse email valide.')

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('email',)


class SearchForm(forms.Form):
    query = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'shadow appearance-none border rounded w-full py-3 px-4 text-text-dark leading-tight focus:outline-none focus:shadow-outline bg-gray-700 border-gray-600 placeholder-gray-400',
            'placeholder': 'Rechercher par titre ou description...'
        })
    )
    category = forms.ModelChoiceField(
        queryset=None,
        required=False,
        empty_label="Toutes les catégories",
        widget=forms.Select(attrs={
            'class': 'w-full p-3 rounded-lg bg-gray-700 border border-gray-600 text-text-light focus:outline-none focus:ring-2 focus:ring-primary'
        })
    )

    def __init__(self, *args, **kwargs):
        categories = kwargs.pop('categories', None)
        super().__init__(*args, **kwargs)
        if categories is not None:
            self.fields['category'].queryset = categories
            

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['nom', 'email', 'sujet', 'message']
        widgets = {
            'nom': forms.TextInput(attrs={
                'class': 'w-full px-5 py-3 rounded-xl border border-gray-300 focus:outline-none focus:ring-2 focus:ring-indigo-400 text-gray-700',
                'placeholder': 'Votre nom'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'w-full px-5 py-3 rounded-xl border border-gray-300 focus:outline-none focus:ring-2 focus:ring-indigo-400 text-gray-700',
                'placeholder': 'votre.email@example.com'
            }),
            'sujet': forms.TextInput(attrs={
                'class': 'w-full px-5 py-3 rounded-xl border border-gray-300 focus:outline-none focus:ring-2 focus:ring-indigo-400 text-gray-700',
                'placeholder': 'Sujet de votre message'
            }),
            'message': forms.Textarea(attrs={
                'rows': 5,
                'class': 'w-full px-5 py-3 rounded-xl border border-gray-300 focus:outline-none focus:ring-2 focus:ring-indigo-400 text-gray-700',
                'placeholder': 'Votre message ici...'
            }),
        }


class NewsletterSubscriptionForm(forms.ModelForm):
    class Meta:
        model = NewsletterSubscriber
        fields = ['email']

class CommentaireForm(forms.ModelForm):
    class Meta:
        model = Commentaire
        fields = ['texte']
        widgets = {
            'texte': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Ajouter un commentaire...',
                'class': 'w-full p-3 border rounded-lg focus:outline-none focus:ring-2 focus:ring-primary'
            }),
        }
        labels = {
            'texte': '' # Pas de label pour le champ de texte du commentaire
        }

# --- NOUVELLE DÉFINITION / CORRECTION DE VOTRE FORMULAIRE DE PROFIL ---
# J'ai renommé votre ancienne classe UserProfileForm en UserProfileEditForm pour correspondre à votre import
# Et j'ai ajouté l'import de 'Profile' et je configure le formulaire pour utiliser le modèle 'Profile'
# C'est la MEILLEURE PRATIQUE si vous avez des champs comme bio, location, profile_image.
# Assurez-vous d'avoir bien défini le modèle Profile dans troquetout_app/models.py
class UserProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile # <-- IMPORTANT : Nous utilisons le modèle Profile ici
        # Listez ici tous les champs du modèle Profile que vous voulez rendre éditables
        fields = ['bio', 'location', 'profile_image'] # Exemple de champs spécifiques à un profil

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name == 'profile_image': # Traitement spécial pour le champ d'image
                field.widget.attrs.update({'class': 'block w-full text-sm text-gray-900 border border-gray-300 rounded-lg cursor-pointer bg-gray-50 focus:outline-none'})
            else: # Pour les autres champs texte
                field.widget.attrs.update({
                    'class': 'w-full px-4 py-3 rounded-lg border-2 border-gray-300 focus:border-primary focus:ring focus:ring-primary focus:ring-opacity-50 transition duration-200 text-gray-800 text-lg',
                })

class PropositionForm(forms.ModelForm):
    # Ce champ sera un sélecteur des annonces de l'utilisateur qui fait la proposition
    # Il sera filtré dans la vue pour n'afficher que les annonces de l'utilisateur connecté
    annonce_proposee = forms.ModelChoiceField(
        queryset=Annonce.objects.none(), # Le queryset est vide ici et sera défini dans la vue
        label="Votre annonce à proposer",
        empty_label="--- Choisissez votre annonce ---",
        widget=forms.Select(attrs={'class': 'form-select block w-full mt-1 border-gray-300 rounded-md shadow-sm focus:border-accent focus:ring focus:ring-accent focus:ring-opacity-50'})
    )

    class Meta: # <-- Indentation corrigée ici !
        model = Proposition
        fields = ['annonce_proposee', 'message']
        widgets = {
            'message': forms.Textarea(attrs={'class': 'form-textarea block w-full mt-1 border-gray-300 rounded-md shadow-sm focus:border-accent focus:ring focus:ring-accent focus:ring-opacity-50', 'rows': 4, 'placeholder': 'Ajoutez un message pour accompagner votre proposition (facultatif)'}),
        }
        labels = {
            'message': 'Votre message',
        }