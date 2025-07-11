# troquetout_app/admin.py
from django.contrib import admin
from .models import Annonce, Categorie # Importe vos modèles Annonce ET Categorie
from .models import ContactMessage

admin.site.register(Annonce)    # Enregistre le modèle Annonce
admin.site.register(Categorie)  # <-- AJOUTE CETTE LIGNE POUR ENREGISTRER LE MODÈLE CATEGORIE



@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('nom', 'email', 'sujet', 'date_soumission', 'lu')
    list_filter = ('lu', 'date_soumission')
    search_fields = ('nom', 'email', 'sujet', 'message')
    readonly_fields = ('date_soumission',) # La date est auto-générée
    actions = ['mark_as_read', 'mark_as_unread'] # Actions personnalisées

    def mark_as_read(self, request, queryset):
        queryset.update(lu=True)
        self.message_user(request, "Les messages sélectionnés ont été marqués comme lus.")
    mark_as_read.short_description = "Marquer comme lu"

    def mark_as_unread(self, request, queryset):
        queryset.update(lu=False)
        self.message_user(request, "Les messages sélectionnés ont été marqués comme non lus.")
    mark_as_unread.short_description = "Marquer comme non lu"