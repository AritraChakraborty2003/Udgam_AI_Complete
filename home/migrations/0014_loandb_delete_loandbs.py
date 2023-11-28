# Generated by Django 4.2.7 on 2023-11-28 18:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0013_loandbs_delete_loandb'),
    ]

    operations = [
        migrations.CreateModel(
            name='loanDB',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dependents', models.IntegerField()),
                ('selfEmployed', models.TextField()),
                ('salary', models.IntegerField()),
                ('loanAmount', models.IntegerField()),
                ('loanTerm', models.IntegerField()),
                ('cibilScore', models.IntegerField()),
                ('resedentialValue', models.IntegerField()),
                ('commercialValue', models.IntegerField()),
                ('luxuryValue', models.IntegerField()),
                ('bankAssets', models.IntegerField()),
                ('designation', models.TextField()),
                ('verified', models.TextField()),
            ],
        ),
        migrations.DeleteModel(
            name='loanDBs',
        ),
    ]