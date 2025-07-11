# troquetout_app/models.py
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings

class Categorie(models.Model):
    nom = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name_plural = "Catégories"

    def __str__(self):
        return self.nom

class Annonce(models.Model):
    auteur = models.ForeignKey(User, on_delete=models.CASCADE, related_name='annonces')
    titre = models.CharField(max_length=200)
    description = models.TextField()
    categorie = models.ForeignKey(
        Categorie,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='annonces_par_categorie'
    )
    image = models.ImageField(upload_to='annonces_photos/', null=True, blank=True)
    valeur_estimee = models.CharField(max_length=100, null=True, blank=True, help_text="Ex: 50€ ou 'Négociable'")
    date_publication = models.DateTimeField(auto_now_add=True)
    TYPE_ANNONCE_CHOICES = [
        ('echange', 'Échange'),
        ('vente', 'Vente'),
        ('don', 'Don'),
        ('offrir', 'Offrir'),
    ]
    type_annonce = models.CharField(
        max_length=10,
        choices=TYPE_ANNONCE_CHOICES,
        default='echange',
        help_text="Indique si c'est une offre d'échange, de vente, de don ou une proposition."
    )
    localisation = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="Ville, code postal ou région de l'objet."
    )
    contact_telephone = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        help_text="Numéro de téléphone pour les contacts (optionnel)."
    )
    contact_email = models.EmailField(
        blank=True,
        null=True,
        help_text="Adresse email de contact différente de votre compte (optionnel)."
    )
    adresse = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="L'adresse précise pour l'échange (optionnel)."
    )
    STATUT_CHOICES = [
        ('OUVERT', 'Ouvert'),
        ('ECHANGE', 'Échangé'),
        ('FERME', 'Fermé'),
    ]
    statut = models.CharField(
        max_length=10,
        choices=STATUT_CHOICES,
        default='OUVERT',
    )
    
    def __str__(self):
        return self.titre

    class Meta:
        ordering = ['-date_publication']


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=100, blank=True)
    profile_image = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

    def __str__(self):
        return f"Profil de {self.user.username}"

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'profile'):
        instance.profile.save()


class ContactMessage(models.Model):
    nom = models.CharField(max_length=100)
    email = models.EmailField()
    sujet = models.CharField(max_length=200)
    message = models.TextField()
    date_soumission = models.DateTimeField(auto_now_add=True)
    lu = models.BooleanField(default=False)

    class Meta:
        ordering = ['-date_soumission']
        verbose_name = "Message de Contact"
        verbose_name_plural = "Messages de Contact"

    def __str__(self):
        return f"Message de {self.nom} - {self.sujet} ({self.date_soumission.strftime('%Y-%m-%d %H:%M')})"
    
class NewsletterSubscriber(models.Model):
    email = models.EmailField(unique=True, max_length=255)
    subscribed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "Abonné Newsletter"
        verbose_name_plural = "Abonnés Newsletter"
        ordering = ['-subscribed_at']
        
class AnnonceLikeDislike(models.Model):
    annonce = models.ForeignKey(Annonce, on_delete=models.CASCADE, related_name='likes_dislikes')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_like = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('annonce', 'user')

    def __str__(self):
        return f"{self.user.username} {'aime' if self.is_like else 'n\'aime pas'} {self.annonce.titre}"

class Commentaire(models.Model):
    annonce = models.ForeignKey(Annonce, on_delete=models.CASCADE, related_name='commentaires')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    texte = models.TextField()
    date_creation = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['date_creation']

    def __str__(self):
        return f"Commentaire de {self.user.username} sur {self.annonce.titre}"

class Proposition(models.Model):
    propose_par = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='propositions_faites', verbose_name="Proposée par")
    annonce_proposee = models.ForeignKey(Annonce, on_delete=models.CASCADE, related_name='propositions_recues_pour_cet_article', verbose_name="Annonce proposée")
    annonce_cible = models.ForeignKey(Annonce, on_delete=models.CASCADE, related_name='propositions_recues_par_cet_article_cible', verbose_name="Annonce ciblée")
    
    message = models.TextField(blank=True, null=True, verbose_name="Message de la proposition")
    date_proposition = models.DateTimeField(auto_now_add=True, verbose_name="Date de la proposition")
    
    STATUT_CHOICES = [
        ('en_attente', 'En attente'),
        ('acceptee', 'Acceptée'),
        ('refusee', 'Refusée'),
        ('annulee', 'Annulée'),
    ]
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='en_attente', verbose_name="Statut")

    class Meta:
        verbose_name = "Proposition de troc"
        verbose_name_plural = "Propositions de Troc"
        ordering = ['-date_proposition']
        unique_together = [['annonce_cible', 'annonce_proposee', 'propose_par']]

    def __str__(self):
        return f"Proposition de {self.propose_par.username} pour '{self.annonce_cible.titre}' avec '{self.annonce_proposee.titre}' ({self.get_statut_display()})"