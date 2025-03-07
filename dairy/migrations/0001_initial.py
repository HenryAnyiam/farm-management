# Generated by Django 4.2.13 on 2024-11-30 21:31

import datetime
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Barn',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
                ('capacity', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1)])),
            ],
            options={
                'verbose_name': 'Barn',
                'verbose_name_plural': 'Barns',
            },
        ),
        migrations.CreateModel(
            name='Cow',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=35)),
                ('date_of_birth', models.DateField()),
                ('gender', models.CharField(choices=[('Male', 'Male'), ('Female', 'Female')], max_length=6)),
                ('availability_status', models.CharField(choices=[('Alive', 'Alive'), ('Sold', 'Sold'), ('Dead', 'Dead')], default='Alive', max_length=5)),
                ('current_pregnancy_status', models.CharField(choices=[('Open', 'Open'), ('Pregnant', 'Pregnant'), ('Calved', 'Calved'), ('Unavailable', 'Unavailable')], default='Unavailable', max_length=12)),
                ('category', models.CharField(choices=[('Calf', 'Calf'), ('Weaner', 'Weaner'), ('Heifer', 'Heifer'), ('Bull', 'Bull'), ('Milking Cow', 'Milking Cow')], default='Calf', max_length=11)),
                ('current_production_status', models.CharField(choices=[('Open', 'Open'), ('Pregnant not Lactating', 'Pregnant Not Lactating'), ('Pregnant and Lactating', 'Pregnant And Lactating'), ('Dry', 'Dry'), ('Culled', 'Culled'), ('Quarantined', 'Quarantined'), ('Bull', 'Bull'), ('Young Bull', 'Young Bull'), ('Young Heifer', 'Young Heifer'), ('Mature Bull', 'Mature Bull'), ('Calf', 'Calf'), ('Weaner', 'Weaner')], default='Calf', max_length=22)),
                ('date_introduced_in_farm', models.DateField(auto_now_add=True)),
                ('is_bought', models.BooleanField(default=False)),
                ('date_of_death', models.DateField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='CowBreed',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[('Friesian', 'Friesian'), ('Ayrshire', 'Ayrshire'), ('Sahiwal', 'Sahiwal'), ('Jersey', 'Jersey'), ('Crossbreed', 'Crossbreed'), ('Guernsey', 'Guernsey')], max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Disease',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('occurrence_date', models.DateField()),
                ('is_recovered', models.BooleanField(default=False)),
                ('recovered_date', models.DateField(blank=True, null=True)),
                ('notes', models.TextField(blank=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Disease 💊',
                'verbose_name_plural': 'Diseases 💊',
            },
        ),
        migrations.CreateModel(
            name='DiseaseCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[('Nutrition', 'Nutrition'), ('Infectious', 'Infectious'), ('Physiological', 'Physiological'), ('Genetic', 'Genetic')], max_length=50, unique=True)),
            ],
            options={
                'verbose_name': 'Disease category',
                'verbose_name_plural': 'Disease categories',
            },
        ),
        migrations.CreateModel(
            name='Inseminator',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=20)),
                ('last_name', models.CharField(max_length=20)),
                ('phone_number', phonenumber_field.modelfields.PhoneNumberField(max_length=13, region=None, unique=True)),
                ('sex', models.CharField(choices=[('Male', 'Male'), ('Female', 'Female')], max_length=6)),
                ('company', models.CharField(blank=True, max_length=50, null=True)),
                ('license_number', models.CharField(max_length=25, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Lactation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField()),
                ('end_date', models.DateField(null=True)),
                ('lactation_number', models.PositiveSmallIntegerField(default=1)),
                ('cow', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lactations', to='dairy.cow')),
            ],
            options={
                'get_latest_by': '-start_date',
            },
        ),
        migrations.CreateModel(
            name='Pathogen',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[('Virus', 'Virus'), ('Bacteria', 'Bacteria'), ('Fungi', 'Fungi')], max_length=50, unique=True)),
            ],
            options={
                'verbose_name': 'Pathogen',
                'verbose_name_plural': 'Pathogens',
            },
        ),
        migrations.CreateModel(
            name='Symptoms',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('type', models.CharField(choices=[('Respiratory', 'Respiratory'), ('Digestive', 'Digestive'), ('Reproductive', 'Reproductive'), ('Musculoskeletal', 'Musculoskeletal'), ('Metabolic', 'Metabolic'), ('Other', 'Other')], max_length=20)),
                ('description', models.TextField()),
                ('date_observed', models.DateField(error_messages={'max_value': 'The date of observation cannot be in the future!.'}, validators=[django.core.validators.MaxValueValidator(datetime.date(2024, 12, 1))])),
                ('severity', models.CharField(choices=[('Mild', 'Mild'), ('Moderate', 'Moderate'), ('Severe', 'Severe')], max_length=20)),
                ('location', models.CharField(choices=[('head', 'Head'), ('Neck', 'Neck'), ('Chest', 'Chest'), ('Abdomen', 'Abdomen'), ('Back', 'Back'), ('Legs', 'Legs'), ('Tail', 'Tail'), ('Whole body', 'Whole body'), ('Other', 'Other')], max_length=20)),
            ],
            options={
                'verbose_name': 'Symptom 🤒',
                'verbose_name_plural': 'Symptoms 🤒',
            },
        ),
        migrations.CreateModel(
            name='WeightRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_now_add=True)),
                ('weight_in_kgs', models.DecimalField(decimal_places=2, max_digits=6)),
                ('cow', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dairy.cow')),
            ],
        ),
        migrations.CreateModel(
            name='Treatment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_of_treatment', models.DateTimeField(auto_now_add=True)),
                ('duration', models.IntegerField(blank=True, null=True)),
                ('notes', models.TextField(blank=True)),
                ('treatment_method', models.TextField(max_length=200)),
                ('treatment_status', models.CharField(choices=[('Scheduled', 'Scheduled'), ('In progress', 'In Progress'), ('Completed', 'Completed'), ('Cancelled', 'Cancelled'), ('Postponed', 'Postponed')], default='Scheduled', max_length=15)),
                ('cost', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('cow', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='dairy.cow')),
                ('disease', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dairy.disease')),
            ],
            options={
                'verbose_name': 'Treatment 💎',
                'verbose_name_plural': 'Treatments 💎',
            },
        ),
        migrations.CreateModel(
            name='Semen',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('producer', models.CharField(choices=[('Kenya Agricultural and Livestock Research Organization', 'Kalro'), ('Kenya Agricultural and Livestock Research Institute', 'Kagric')], max_length=64)),
                ('semen_batch', models.CharField(max_length=64)),
                ('date_of_production', models.DateField(error_messages={'max_value': 'Invalid date entry, Dates of production must not be in future'}, validators=[django.core.validators.MaxValueValidator(datetime.date(2024, 12, 1))])),
                ('date_of_expiry', models.DateField(error_messages={'min_value': 'Invalid date entry, Date of expiry must be in future'}, validators=[django.core.validators.MinValueValidator(datetime.date(2024, 12, 1))])),
                ('notes', models.TextField(blank=True)),
                ('inseminator', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='dairy.inseminator')),
            ],
        ),
        migrations.CreateModel(
            name='QuarantineRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reason', models.CharField(choices=[('Sick Cow', 'Sick Cow'), ('Bought Cow', 'Bought Cow'), ('New Cow', 'New Cow')], max_length=20)),
                ('start_date', models.DateField(auto_now_add=True)),
                ('end_date', models.DateField(null=True)),
                ('notes', models.TextField(max_length=100, null=True)),
                ('cow', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='quarantine_record', to='dairy.cow')),
            ],
            options={
                'get_latest_by': '-start_date',
            },
        ),
        migrations.CreateModel(
            name='Pregnancy',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField()),
                ('date_of_calving', models.DateField(blank=True, null=True)),
                ('pregnancy_status', models.CharField(choices=[('Confirmed', 'Confirmed'), ('Unconfirmed', 'Unconfirmed'), ('Failed', 'Failed')], default='Unconfirmed', max_length=11)),
                ('pregnancy_notes', models.TextField(blank=True)),
                ('calving_notes', models.TextField(blank=True)),
                ('pregnancy_scan_date', models.DateField(blank=True, null=True)),
                ('pregnancy_failed_date', models.DateField(blank=True, null=True)),
                ('pregnancy_outcome', models.CharField(blank=True, choices=[('Live', 'Live'), ('Stillborn', 'Stillborn'), ('Miscarriage', 'Miscarriage')], max_length=11, null=True)),
                ('cow', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='pregnancies', to='dairy.cow')),
            ],
        ),
        migrations.CreateModel(
            name='Milk',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('milking_date', models.DateTimeField(auto_now_add=True)),
                ('amount_in_kgs', models.DecimalField(decimal_places=2, default=0.0, max_digits=4, verbose_name='Amount (kgs)')),
                ('cow', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='milk_records', to='dairy.cow')),
                ('lactation', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, to='dairy.lactation')),
            ],
            options={
                'get_latest_by': '-milking_date',
            },
        ),
        migrations.AddField(
            model_name='lactation',
            name='pregnancy',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='dairy.pregnancy'),
        ),
        migrations.CreateModel(
            name='Insemination',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_of_insemination', models.DateTimeField(auto_now_add=True)),
                ('success', models.BooleanField(default=False)),
                ('notes', models.TextField(blank=True)),
                ('cow', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='inseminations', to='dairy.cow')),
                ('inseminator', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='inseminations_done', to='dairy.inseminator')),
                ('pregnancy', models.OneToOneField(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.PROTECT, to='dairy.pregnancy')),
                ('semen', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='dairy.semen')),
            ],
            options={
                'ordering': ['-date_of_insemination'],
            },
        ),
        migrations.CreateModel(
            name='Heat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('observation_time', models.DateTimeField()),
                ('cow', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='heat_records', to='dairy.cow')),
            ],
        ),
        migrations.AddField(
            model_name='disease',
            name='categories',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='diseases', to='dairy.diseasecategory'),
        ),
        migrations.AddField(
            model_name='disease',
            name='cows',
            field=models.ManyToManyField(related_name='diseases', to='dairy.cow'),
        ),
        migrations.AddField(
            model_name='disease',
            name='pathogen',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='dairy.pathogen'),
        ),
        migrations.AddField(
            model_name='disease',
            name='symptoms',
            field=models.ManyToManyField(related_name='diseases', to='dairy.symptoms'),
        ),
        migrations.AddField(
            model_name='disease',
            name='treatments',
            field=models.ManyToManyField(blank=True, related_name='diseases', to='dairy.treatment'),
        ),
        migrations.CreateModel(
            name='CullingRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reason', models.CharField(choices=[('Injuries', 'Injuries'), ('Chronic Health Issues', 'Chronic Health'), ('Cost Of Care', 'Cost Of Care'), ('Unprofitable', 'Unprofitable'), ('Low Market Demand', 'Low Market Demand'), ('Age', 'Age'), ('Consistent_Low Production', 'Consistent Low Production'), ('Low Quality', 'Consistent Poor Quality'), ('Inefficient Feed Conversion', 'Inefficient Feed Conversion'), ('Inherited Diseases', 'Inherited Diseases'), ('Inbreeding', 'Inbreeding'), ('Unwanted Traits', 'Unwanted Traits'), ('Climate Change', 'Climate Change'), ('Natural Disaster', 'Natural Disaster'), ('Overpopulation', 'Overpopulation'), ('Government Regulations', 'Government Regulations'), ('Animal Welfare Standards', 'Animal Welfare Standards'), ('Environmental Protection Laws', 'Environment Protection Laws')], max_length=35)),
                ('date', models.DateField(auto_now_add=True)),
                ('notes', models.TextField(max_length=100, null=True)),
                ('cow', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='culling_record', to='dairy.cow')),
            ],
        ),
        migrations.CreateModel(
            name='CowPen',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pen_type', models.CharField(choices=[('Movable', 'Movable'), ('Fixed', 'Fixed')], max_length=15)),
                ('category', models.CharField(choices=[('Calf Pen', 'Calf Pen'), ('Sick Pen', 'Sick Pen'), ('Breeding Pen', 'Breeding Pen'), ('Quarantine Pen', 'Quarantine Pen'), ('Bull Pen', 'Bull Pen'), ('Heifer Pen', 'Heifer Pen'), ('Dry Pen', 'Dry Pen'), ('General Pen', 'General Pen')], max_length=15)),
                ('capacity', models.PositiveIntegerField(default=1, validators=[django.core.validators.MinValueValidator(1)])),
                ('barn', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pens', to='dairy.barn')),
            ],
        ),
        migrations.CreateModel(
            name='CowInPenMovement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('cow', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dairy.cow')),
                ('new_pen', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cows_new_pen', to='dairy.cowpen')),
                ('previous_pen', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='cows_previous_pen', to='dairy.cowpen')),
            ],
        ),
        migrations.CreateModel(
            name='CowInBarnMovement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('cow', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dairy.cow')),
                ('new_barn', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='received_cows', to='dairy.barn')),
                ('previous_barn', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='moved_cows', to='dairy.barn')),
            ],
        ),
        migrations.AddField(
            model_name='cow',
            name='breed',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='cows', to='dairy.cowbreed'),
        ),
        migrations.AddField(
            model_name='cow',
            name='dam',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='calves', to='dairy.cow'),
        ),
        migrations.AddField(
            model_name='cow',
            name='sire',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='offspring', to='dairy.cow'),
        ),
        migrations.CreateModel(
            name='Vaccination',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vaccine_name', models.CharField(max_length=100)),
                ('date_given', models.DateField(auto_now_add=True)),
                ('dose_amount', models.DecimalField(decimal_places=2, max_digits=7, validators=[django.core.validators.MinValueValidator(0)])),
                ('dose_unit', models.CharField(choices=[('ml', 'ml'), ('cc', 'cc'), ('mg', 'mg'), ('g', 'g')], default='ml', max_length=3)),
                ('cow', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dairy.cow')),
            ],
            options={
                'ordering': ['-date_given'],
                'unique_together': {('cow', 'vaccine_name')},
            },
        ),
    ]
