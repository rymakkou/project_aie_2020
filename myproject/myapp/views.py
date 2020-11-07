from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import Item
from .Forms import FormeDocteur
from django.contrib.auth.models import User
from django.db import transaction
from django.shortcuts import redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Profile,RendezVous, Patient, DossierPatient, ConsultationMedical
from .Forms import UserForm
from .Forms import FormePatient,FormeRendezVous, FormeDossierPatient, FormeConsultationPatient,FormeInscriptionPatient, CreateRendezVous
from django.contrib.messages import constants as messages
from datetime import datetime
from django.utils import timezone
from django.contrib.auth.decorators import login_required
  

def patientPanel(request):
    return render(request, 'PatientPanel/form.html')

def inscription_patient(request):
    form = FormeInscriptionPatient()
    if request.method=='POST':
        forme=FormeInscriptionPatient(request.POST)
        if forme.is_valid():
            user = forme.save(commit=False)
            user.is_active = True
            user.save()

            #permet d'enregistrer le profile de l'utilisateur
            user = forme.save()
            user.refresh_from_db()

            user.profile.adresse = forme.cleaned_data.get('adresse')
            user.profile.date_naissance = forme.cleaned_data.get('date_naissance')
            user.profile.numero_telephone = forme.cleaned_data.get('numero_telephone')
            user.profile.num_assurance = forme.cleaned_data.get('num_assurance')
            user.profile.groupe_sanguin = forme.cleaned_data.get('groupe_sanguin')
            
            
            user.profile.is_patient = True
        
            user.save()
            return redirect('myapp:acceuil')
        else:
            return HttpResponse('Une érreur est survenu lors de la validation des données')

    context = {
        'form' : form,
    }

    return render(request, 'PatientPanel/inscription-patient.html',context)


def afficher_page_profile(request):
    consultation = ConsultationMedical.objects.filter(patient = request.user)[:3]
    rdv = RendezVous.objects.filter(patient = request.user)[:3]

    context = {
        'consultation' : consultation,
        'rdv' : rdv,
    }
   
    return render(request, 'profile-panel.html', context)

@login_required
def patient_create_rdv(request):
    form = CreateRendezVous()

    if request.method=='POST':
        form = CreateRendezVous(request.POST)
        if form.is_valid():
            date = form.cleaned_data['date_rendez_vous']
            motif = form.cleaned_data['motif_rendez_vous']
            heure = form.cleaned_data['heure_rendez_vous']
            service = form.cleaned_data['service']

            forme = RendezVous(

                patient  = request.user,
                date_rendez_vous = date,
                motif_rendez_vous = motif,
                heure_rendez_vous = heure,
                service = service,
                etat = 'a'
            )

            forme.save()
            return redirect('myapp:afficher_page_profile')
        else:
            return HttpResponse('Une érreur est survenu lors de la validation des données')


    context = {
        'form' : form
    }
    return render(request,'PatientPanel/creation-rendez-vous.html', context)


def index(request):
    nb_pat = Patient.objects.all()
    count = RendezVous.objects.filter(etat='a', date_rendez_vous__gte = timezone.now())
    rdv_auj = RendezVous.objects.filter(date_rendez_vous = timezone.now())

    context = {
        'count' : count,
        'rdv_auj' : rdv_auj,
        'nb_pat' : nb_pat,
    }
    return render(request, 'index.html', context)

@login_required
def list_rendez_vous(request):
    list_rdv = RendezVous.objects.all()

    context = {
        'list_rdv' : list_rdv,
    }
    return render(request, 'all_rendez_vous.html', context)
    

    return render(request, 'index.html', context)
@login_required
def charts (request) :
    return render (request, 'charts.html')
def login (request) :
    return render (request, 'login.html')

@login_required
def crer_dossier_patient(request):
    forme = FormeDossierPatient()

    if request.method=='POST':
        forme=FormeDossierPatient(request.POST)
        if forme.is_valid():
            forme.save()
            return redirect('myapp:tables')
        else:
            return HttpResponse('Une érreur est survenu lors de la validation des données')

    context = {
        'forme' : forme,
    }

    return render(request, 'creer_dossier_patient.html', context)

@login_required
def afficher_list_dossier(request):
    list = DossierPatient.objects.all()

    context = {
        'list' : list,

    }

    return render(request, 'list_dossier_patient.html', context)
@login_required
def afficher_list_patients(request):
    list = Profile.objects.filter(is_patient=True)

    context = {
        'list' : list,

    }

    return render(request, 'list_patient.html', context)


@login_required
def datails_profile(request, slug):
    detail = get_object_or_404(Profile, slug = slug)

    test = DossierPatient.objects.all().count()   
    if (test == 0):
        has_dossier  = DossierPatient.objects.filter(patient__profile__slug = slug)
    else:
        has_dossier = DossierPatient.objects.get(patient__profile__slug = slug)
 
    has_consul = ConsultationMedical.objects.filter(patient__profile__slug = slug)

    has_rdv = RendezVous.objects.filter(patient__profile__slug = slug)

    context = {
        'detail' : detail,
        'has_dossier' : has_dossier,
        'has_consul' : has_consul,
        'has_rdv' : has_rdv,
    }

    return render(request, 'details_patient.html', context)

@login_required
def detail_dossier_patient(request, slug):
    detail = get_object_or_404(DossierPatient, slug=slug)

    context = {
        'detail' : detail 
    }

    return render(request, 'details_dossier_patient.html', context)

@login_required
def creer_rendez_vous(request):
    forme = FormeRendezVous()

    if request.method=='POST':
        forme=FormeRendezVous(request.POST)
        if forme.is_valid():
            date = forme.cleaned_data['date_rendez_vous']
            nom = forme.cleaned_data['patient']
            motif = forme.cleaned_data['motif_rendez_vous']
            heure = forme.cleaned_data['heure_rendez_vous']
            service = forme.cleaned_data['service']

            forme = RendezVous(
                patient  = nom,
                date_rendez_vous = date,
                motif_rendez_vous = motif,
                heure_rendez_vous = heure,
                service = service,
                etat = 'a'
            )

            forme.save()
            return redirect('myapp:tables')
        else:
            return HttpResponse('Une érreur est survenu lors de la validation des données')

    context = {
        'forme' : forme
    }
    return render(request,'Creer_rendez_vous.html', context)
@login_required
def ajout_patient(request):
    forme = FormeInscriptionPatient()  

    if request.method=='POST':
        forme=FormeInscriptionPatient(request.POST)
        if forme.is_valid():
            user = forme.save(commit=False)
            user.is_active = True
            user.save()

            #permet d'enregistrer le profile de l'utilisateur
            user = forme.save()
            user.refresh_from_db()

            user.profile.adresse = forme.cleaned_data.get('adresse')
            user.profile.date_naissance = forme.cleaned_data.get('date_naissance')
            user.profile.numero_telephone = forme.cleaned_data.get('numero_telephone')
            user.profile.num_assurance = forme.cleaned_data.get('num_assurance')
            user.profile.groupe_sanguin = forme.cleaned_data.get('groupe_sanguin')
            
            user.profile.is_patient = True
        
            user.save()
            return redirect('myapp:tables')
        else:
            return HttpResponse('Une érreur est survenu lors de la validation des données')
    context = {
        'forme' : forme,
    }
    return render(request, 'Ajouter_patient.html', context)

def crer_consultation(request):
    forme = FormeConsultationPatient()
    if request.method=='POST':
        forme=FormeConsultationPatient(request.POST)
        if forme.is_valid():
            forme.save()
            return redirect('myapp:tables')
        else:
            return HttpResponse('Une érreur est survenu lors de la validation des données')


    context = {
        'forme' : forme,
    }

    return render(request, 'creer_consultation.html', context)


@login_required
def forms (request) :
    forme = FormeDocteur()
   
    if request.method=='POST':
        forme=FormeDocteur(request.POST)
        if forme.is_valid():
            
            user = forme.save(commit=False)
            user.is_active = True
            user.save()

            #permet d'enregistrer le profile de l'utilisateur
            user = forme.save()
            user.refresh_from_db()

            user.profile.adresse = forme.cleaned_data.get('adresse')
            user.profile.date_naissance = forme.cleaned_data.get('date_naissance')
            user.profile.numero_telephone = forme.cleaned_data.get('numero_telephone')
            user.profile.affectation = forme.cleaned_data.get('affectation')
            user.profile.fonction = forme.cleaned_data.get('fonction')
            
            user.profile.is_docteur = True
        
            user.save()
            return redirect('myapp:tables')
        else:
            return HttpResponse('Une érreur est survenu lors de la validation des données')

    context = {
        'forme' : forme

    }
    return render (request, 'forms.html', context)

@login_required
def tables (request) :
    return render (request, 'tables.html')
def nanam (request) :
    return render (request, 'nanam.html')

@login_required
def afficher_rendez_vous(request, slug):
    rdv = get_object_or_404(RendezVous, slug=slug)

    context = {
        'rdv' : rdv,
    }
    return render(request, 'details_rendez_vous.html', context)

@login_required
def Inscription (request) :
    forme = FormeDocteur()
    user = User.objects.filter(user=request.user)
    context : {
        'Form' : forme,
        'user' : user,
        }
    return render (request, 'Inscription.html',context)


@login_required
@transaction.atomic
def update_profile(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request,'Your profile was successfully updated!')
            return redirect('settings:profile')
        else:
            messages.error(request,'Please correct the error below.')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
    return render(request, 'profiles/profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })




def ajouter(request) :
       

    return redirect('myapp:index')
