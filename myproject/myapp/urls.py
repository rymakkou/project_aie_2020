from django.contrib import admin
from django.urls import include,path
from .views import index,charts,login,forms,tables,nanam,Inscription, ajouter, ajout_patient,afficher_page_profile, creer_rendez_vous,list_rendez_vous,afficher_rendez_vous,crer_dossier_patient,afficher_list_dossier,detail_dossier_patient,afficher_list_patients,datails_profile,crer_consultation,patientPanel,inscription_patient,patient_create_rdv




app_name='myapp'
urlpatterns = [
        path('', patientPanel, name="acceuil"),
        path('inscription_patient',inscription_patient, name="inscription_patient"),
        path('Dashboard/',index,name='index'),
        path('charts/',charts,name='charts'),
        path('login/',login,name='login'),
        path('forms/',forms,name='forms'),
        path('tables/',tables,name='tables'),
        path('nanam/',nanam,name='nanam'),
        path('Inscription/',Inscription,name='Inscription'),
        path('ajouter/',ajouter,name='ajouter'),
        path('Ajout_de_patient',ajout_patient, name="ajouter_patient"),
        path('Cree_un_rendez_vous',creer_rendez_vous, name="creer_rendez_vous"),
        path('Liste_de_tous_les_rendez_vous',list_rendez_vous, name="list_rendez_vous"),
        path('afficher_rendez_vous/<slug>', afficher_rendez_vous, name="afficher_rendez_vous"),
        path('creer_dossier_patient',crer_dossier_patient,name='crer_dossier_patient'),
        path('afficher_list_dossier',afficher_list_dossier,name="afficher_list_dossier"),
        path('detail_dossier_patient/<slug>',detail_dossier_patient,name="detail_dossier_patient"),
        path('afficher_list_patients', afficher_list_patients, name="afficher_list_patients"),
        path('datails_profile/<slug>', datails_profile, name="datails_profile"),
        path('crer_consultation/',crer_consultation,name="crer_consultation"),
        path('afficher_page_profile',afficher_page_profile,name="afficher_page_profile"),
        path('patient_create_rdv',patient_create_rdv,name="patient_create_rdv"),
       



        
]

