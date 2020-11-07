# Generated by Django 3.1.2 on 2020-11-03 20:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import myapp.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(blank=True, max_length=100, null=True)),
                ('prenom', models.CharField(blank=True, max_length=100, null=True)),
                ('adresse', models.CharField(blank=True, max_length=100, null=True)),
                ('date_naissance', models.DateField()),
                ('numero_telephone', models.CharField(blank=True, max_length=11, null=True)),
                ('groupe_sanguin', models.CharField(blank=True, max_length=3, null=True)),
                ('num_assurance', models.CharField(blank=True, max_length=100, null=True)),
                ('slug', models.SlugField(blank=True, null=True, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='RendezVous',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_rendez_vous', models.CharField(blank=True, default=myapp.models.increment_id_rendez_vous, max_length=1000, null=True)),
                ('date_rendez_vous', models.DateField(null=True)),
                ('heure_rendez_vous', models.IntegerField(blank=True, null=True)),
                ('motif_rendez_vous', models.CharField(blank=True, max_length=200, null=True)),
                ('etat', models.CharField(blank=True, choices=[('f', 'Fini'), ('a', 'Attente')], max_length=2, null=True)),
                ('slug', models.SlugField(blank=True, null=True, unique=True)),
                ('patient', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='myapp.patient')),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_patient', models.BooleanField(default=False)),
                ('is_docteur', models.BooleanField(default=False)),
                ('adresse', models.CharField(blank=True, max_length=100, null=True)),
                ('date_naissance', models.DateField(blank=True, null=True)),
                ('numero_telephone', models.CharField(blank=True, max_length=11, null=True)),
                ('groupe_sanguin', models.CharField(blank=True, max_length=3, null=True)),
                ('num_assurance', models.CharField(blank=True, max_length=100, null=True)),
                ('affectation', models.CharField(blank=True, choices=[('p', 'Pédiatrie'), ('g', 'Médecine général'), ('si', 'Soins Intensifs'), ('u', 'Urgences'), ('ne', 'Neurologie'), ('d', 'Pneumlogie')], max_length=2, null=True)),
                ('fonction', models.CharField(blank=True, choices=[('m', 'Médecin'), ('ai', 'Aid soignant'), ('u', 'Urgentiste'), ('as', 'Assistante'), ('if', 'Inférmiere')], max_length=2, null=True)),
                ('slug', models.SlugField(blank=True, max_length=100, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=100, null=True)),
                ('price', models.FloatField(blank=True, null=True)),
                ('discount_price', models.FloatField(blank=True, null=True)),
                ('category', models.CharField(choices=[('I', 'Interne'), ('EX', 'Externe')], max_length=2)),
                ('label', models.CharField(choices=[('P', 'primary'), ('S', 'secondary'), ('D', 'danger')], max_length=1)),
                ('image', models.ImageField(null=True, upload_to='')),
                ('description', models.TextField(blank=True, null=True)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='DossierPatient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_dossier_patient', models.CharField(blank=True, default=myapp.models.increment_id_dossier_patient, max_length=1000, null=True)),
                ('antecedent_medical', models.CharField(blank=True, max_length=600, null=True)),
                ('medecin_traitant', models.CharField(blank=True, max_length=50, null=True)),
                ('slug', models.SlugField(blank=True, null=True, unique=True)),
                ('created_at', models.DateField(auto_now_add=True)),
                ('patient', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='myapp.patient')),
            ],
        ),
        migrations.CreateModel(
            name='ConsultationMedical',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_consultation_patient', models.CharField(blank=True, default=myapp.models.increment_id_consultation_patient, max_length=1000, null=True)),
                ('date_consultation', models.DateField(auto_now_add=True)),
                ('motif_consultation', models.CharField(blank=True, max_length=400, null=True)),
                ('observations', models.CharField(blank=True, max_length=1000, null=True)),
                ('slug', models.SlugField(blank=True, null=True, unique=True)),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.patient')),
            ],
        ),
    ]
