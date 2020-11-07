from django.db import models
from django.contrib import admin
from datetime import datetime, date
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.shortcuts import reverse
from django.utils.text import slugify
from django.conf import settings


# Create your models here.
category_choices=(

('I', 'Interne'),
('EX', 'Externe') ,
)

label_choices=(

    ('P','primary'),
    ('S','secondary'),
    ('D', 'danger'),
)


ETAT = (
    ('f', 'Fini'),
    ('a', 'Attente')
)

AFFECTATION = (
    ('p', 'Pédiatrie'),
    ('g', 'Médecine général'),
    ('si', 'Soins Intensifs'),
    ('u', 'Urgences'),
    ('ne', 'Neurologie'),
    ('d','Pneumlogie')
)

FONCTION = (
    ('m', 'Médecin'),
    ('ai', 'Aid soignant'),
    ('u', 'Urgentiste'),
    ('as', 'Assistante'),
    ('if', 'Inférmiere'),
)

SERVICE = (
    ('p', 'Pédiatrie'),
    ('g', 'Médecine général'),
    ('ne', 'Neurologie'),
    ('d','Pneumlogie')
)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)   

    is_patient = models.BooleanField(default=False)
    is_docteur = models.BooleanField(default=False)

    adresse = models.CharField(max_length=100, null=True, blank=True)
    date_naissance = models.DateField(null=True, blank=True)
    numero_telephone = models.CharField(max_length=11, null=True, blank=True)
    groupe_sanguin = models.CharField(max_length=3, null=True, blank=True)
    num_assurance = models.CharField(max_length=100, null=True, blank=True)

    affectation = models.CharField(max_length=2, null=True,blank=True,choices=AFFECTATION)
    fonction = models.CharField(max_length=2, null=True,blank=True,choices=FONCTION)

    slug = models.SlugField(max_length=100, null=True, blank=True)


    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created : 
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
            instance.profile.save()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.user.username)
        super(Profile, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("myapp:datails_profile", kwargs={
        'slug': self.slug
    })

    def __str__(self):
        return self.user.username

class Item(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    title=models.CharField(max_length=100,blank=True,null=True)
    price=models.FloatField(blank=True,null=True)
    discount_price=models.FloatField(blank=True,null=True)
    category=models.CharField(choices=category_choices,max_length=2)
    label=models.CharField(choices=label_choices,max_length=1)
    image=models.ImageField(null=True)
    description=models.TextField(blank=True,null=True)

class Patient(models.Model):
    nom = models.CharField(max_length=100, null=True, blank=True)
    prenom = models.CharField(max_length=100, null=True, blank=True)
    adresse = models.CharField(max_length=100, null=True, blank=True)
    date_naissance = models.DateField()
    numero_telephone = models.CharField(max_length=11, null=True, blank=True)
    groupe_sanguin = models.CharField(max_length=3, null=True, blank=True)
    num_assurance = models.CharField(max_length=100, null=True, blank=True)

    slug = models.SlugField(unique=True, null=True, blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.num_assurance)
        super(Patient, self).save(*args, **kwargs)

    def __str__(self):
        return self.nom

    def get_absolute_url(self):
        return reverse("myapp:datails_patient", kwargs={
        'slug': self.slug
    })

def increment_id_dossier_patient():
        dernier_nomber = DossierPatient.objects.all().order_by('id').last()
        if not dernier_nomber:
            return 'dos/' + '1'

        id_dossier_patient = dernier_nomber.id_dossier_patient
        item_order_nb = int(id_dossier_patient.split('dos/')[-1])
        n_item_order_nb = item_order_nb + 1
        n_item_order_id = 'dos/' + str(n_item_order_nb)
        return n_item_order_id

class DossierPatient(models.Model):
    id_dossier_patient = models.CharField(max_length=1000, default=increment_id_dossier_patient, null=True, blank=True)
    patient = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    antecedent_medical = models.CharField(max_length=600, null=True, blank=True)
    medecin_traitant = models.CharField(max_length=50, null=True, blank=True)
    slug = models.SlugField(unique=True, null=True, blank=True)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.patient.last_name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.id_dossier_patient)
        super(DossierPatient, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("myapp:detail_dossier_patient", kwargs={
        'slug': self.slug
    })





def increment_id_consultation_patient():
        dernier_nomber = ConsultationMedical.objects.all().order_by('id').last()
        if not dernier_nomber:
            return 'consul/' + '1'

        id_consultation_patient = dernier_nomber.id_consultation_patient
        item_order_nb = int(id_consultation_patient.split('consul/')[-1])
        n_item_order_nb = item_order_nb + 1
        n_item_order_id = 'consul/' + str(n_item_order_nb)
        return n_item_order_id

class ConsultationMedical(models.Model):
    id_consultation_patient = models.CharField(max_length=1000, default=increment_id_consultation_patient, null=True, blank=True)
    patient =  models.ForeignKey(User, on_delete=models.CASCADE)
    date_consultation = models.DateField(auto_now_add=True)
    motif_consultation = models.CharField(max_length=400, null=True, blank=True)
    observations = models.CharField(max_length=1000, null=True, blank=True)

    slug = models.SlugField(unique=True, null=True, blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.id_consultation_patient)
        super(ConsultationMedical, self).save(*args, **kwargs) 

    def __str__(self):
        return self.patient.last_name


def increment_id_rendez_vous():
        dernier_nomber = RendezVous.objects.all().order_by('id').last()
        if not dernier_nomber:
            return 'rdv/' + '1'

        id_rendez_vous = dernier_nomber.id_rendez_vous
        item_order_nb = int(id_rendez_vous.split('rdv/')[-1])
        n_item_order_nb = item_order_nb + 1
        n_item_order_id = 'rdv/' + str(n_item_order_nb)
        return n_item_order_id

class RendezVous(models.Model):
    id_rendez_vous = models.CharField(max_length=1000, default=increment_id_rendez_vous, null=True, blank=True)
    patient = models.ForeignKey(User, on_delete= models.CASCADE, null=True)
    service = models.CharField(max_length=2, choices=SERVICE,null=True, blank=True)
    date_rendez_vous = models.DateField(null=True)
    heure_rendez_vous = models.IntegerField(null=True, blank=True)
    motif_rendez_vous = models.CharField(max_length=200, null=True, blank=True)
    etat = models.CharField(choices=ETAT, max_length=2, null=True, blank=True)
    slug = models.SlugField(unique=True, null=True, blank=True)

    

    def __str__(self):
        return self.patient.last_name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.id_rendez_vous)
        super(RendezVous, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("myapp:afficher_rendez_vous", kwargs={
        'slug': self.slug
    })




    
            


   
