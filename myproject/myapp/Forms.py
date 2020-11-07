from django.forms import ModelForm
from django.db import transaction
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django import forms
from .models import Item,Profile, Patient, RendezVous, DossierPatient, ConsultationMedical
from django.contrib.auth.forms import UserCreationForm

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

class FormeDocteur(UserCreationForm):

    email = forms.EmailField(max_length=100)
    adresse = forms.CharField(max_length=100,  label="Votre adresse")
    date_naissance = forms.DateField()
    numero_telephone = forms.CharField(max_length=100,  label="N° de téléphone")
    affectation =  forms.ChoiceField(choices=AFFECTATION)
    fonction =  forms.ChoiceField(choices=FONCTION)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name','email','adresse','date_naissance','numero_telephone', 'fonction','affectation','fonction']
    

class FormeInscriptionPatient(UserCreationForm):
   
    adresse = forms.CharField(max_length=100,  label="Votre adresse", widget=forms.TextInput(attrs={'type' : 'text', 'class': 'form-control'}), required=True)
    date_naissance = forms.DateField(widget=forms.TextInput(attrs={'type' : 'date', 'class': 'form-control'}), required=True)
    numero_telephone = forms.CharField(max_length=100,  label="N° de téléphone",widget=forms.TextInput(attrs={'type' : 'text', 'class': 'form-control'}), required=True)
    num_assurance = forms.CharField(max_length=100,  label="N° Identification Social (SS)",widget=forms.TextInput(attrs={'type' : 'text', 'class': 'form-control'}), required=True)
    groupe_sanguin = forms.CharField(max_length=100,  label="Votre groupe sanguin",widget=forms.TextInput(attrs={'type' : 'text', 'class': 'form-control'}), required=True)
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name','email','adresse','date_naissance','numero_telephone','num_assurance', 'groupe_sanguin']

        widgets = {
            
            'username': forms.TextInput(attrs={'type' : 'text', 'class': 'form-control'}),
            'first_name' : forms.TextInput(attrs={'type' : 'text', 'class': 'form-control'}),
            'last_name' : forms.TextInput(attrs={'type' : 'text', 'class' : 'form-control'}),
            'email': forms.TextInput(attrs={'type' : 'Email', 'class': 'form-control'}),
            'date_naissance' : forms.TextInput(attrs={'type' : 'date', 'class': 'form-control'}),
            
        }

class CreateRendezVous(forms.ModelForm):
    class Meta:
        model = RendezVous
        fields=['service','date_rendez_vous','heure_rendez_vous','motif_rendez_vous']

        widgets = {
            
            'date_rendez_vous' : forms.TextInput(attrs={'type' : 'date', 'class': 'form-control'}),
            'heure_rendez_vous' : forms.TextInput(attrs={'type' : 'Number', 'class' : 'form-control'}),
            'service' : forms.Select(attrs={'type' : 'text', 'class' : 'form-control'}),
            'motif_rendez_vous': forms.TextInput(attrs={'type' : 'text', 'class': 'form-control'}),
            
        }
        

class FormeRendezVous(forms.ModelForm):
    class Meta :
        model = RendezVous
        fields=['patient','service','date_rendez_vous','heure_rendez_vous','motif_rendez_vous']

        widgets = {
            'patient': forms.Select(attrs={'type' : 'text', 'class': 'form-control'}),
            'date_rendez_vous' : forms.TextInput(attrs={'type' : 'date', 'class': 'form-control'}),
            'heure_rendez_vous' : forms.TextInput(attrs={'type' : 'Number', 'class' : 'form-control'}),
            'service' : forms.Select(attrs={'type' : 'text', 'class' : 'form-control'}),
            'motif_rendez_vous': forms.TextInput(attrs={'type' : 'text', 'class': 'form-control'}),
            
        }

class FormeDossierPatient(forms.ModelForm):
    class Meta:
        model =  DossierPatient
        fields = ['patient','antecedent_medical','medecin_traitant']

        widgets = {
            'patient' : forms.Select(attrs={'type' : 'text', 'class': 'form-control'}),
            'antecedent_medical': forms.TextInput(attrs={'type' : 'text', 'class': 'form-control'}),
            'medecin_traitant': forms.TextInput(attrs={'type' : 'text', 'class': 'form-control'}),
             
        }

class FormeConsultationPatient(forms.ModelForm):
    class Meta:
        model =  ConsultationMedical
        fields = ['patient','motif_consultation','observations']

        widgets = {
            'patient' : forms.Select(attrs={'type' : 'text', 'class': 'form-control'}),
           
            'motif_consultation': forms.TextInput(attrs={'type' : 'text', 'class': 'form-control'}),
            'observations': forms.TextInput(attrs={'type' : 'text', 'class': 'form-control'}),
             
        }



class FormePatient(forms.ModelForm):
    class Meta :
        model = Patient
        fields=['nom','prenom','adresse','date_naissance','numero_telephone','groupe_sanguin','num_assurance']

        widgets = {
            'nom' : forms.TextInput(attrs={'type' : 'text', 'class': 'form-control'}),
            'prenom': forms.TextInput(attrs={'type' : 'text', 'class': 'form-control'}),
             'adresse': forms.TextInput(attrs={'type' : 'text', 'class': 'form-control'}),
             'date_naissance': forms.TextInput(attrs={'type' : 'date', 'class': 'form-control'}),
               'numero_telephone': forms.TextInput(attrs={'type' : 'text', 'class': 'form-control'}),
                'groupe_sanguin': forms.TextInput(attrs={'type' : 'text', 'class': 'form-control'}),
                 'num_assurance': forms.TextInput(attrs={'type' : 'text', 'class': 'form-control', 'placeholder':"Numéro d'assurance"})
        }


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')



