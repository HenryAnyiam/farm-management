# Generated by Django 4.2.13 on 2024-12-16 03:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_alter_user_role'),
        ('poultry', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='eggcollection',
            name='organization',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='egg_collections', to='users.organization'),
        ),
        migrations.AddField(
            model_name='flock',
            name='organization',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='flocks', to='users.organization'),
        ),
        migrations.AddField(
            model_name='flockbreed',
            name='organization',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='breeds', to='users.organization'),
        ),
        migrations.AddField(
            model_name='flockbreedinformation',
            name='organization',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='breed_information', to='users.organization'),
        ),
        migrations.AddField(
            model_name='flockhistory',
            name='organization',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='flock_histories', to='users.organization'),
        ),
        migrations.AddField(
            model_name='flockinspectionrecord',
            name='organization',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='inspections', to='users.organization'),
        ),
        migrations.AddField(
            model_name='flockmovement',
            name='organization',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='flock_movements', to='users.organization'),
        ),
        migrations.AddField(
            model_name='flocksource',
            name='organization',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sources', to='users.organization'),
        ),
        migrations.AddField(
            model_name='housingstructure',
            name='organization',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='structures', to='users.organization'),
        ),
    ]
