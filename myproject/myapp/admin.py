from django.contrib import admin

# Register your models here.
from .models import Item, Profile, Patient, RendezVous, DossierPatient,ConsultationMedical

admin.site.register(Profile)
admin.site.register(Patient)
admin.site.register(RendezVous)
admin.site.register(Item)
admin.site.register(DossierPatient)
admin.site.register(ConsultationMedical)
