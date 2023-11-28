# Generated by Django 4.2.7 on 2023-11-28 18:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0011_verifydoc'),
    ]

    operations = [
        migrations.CreateModel(
            name='loanDB',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dependents', models.TextField()),
                ('education', models.TextField()),
                ('selfEmployed', models.TextField()),
                ('salary', models.TextField()),
                ('loanAmount', models.TextField()),
                ('loanTerm', models.TextField()),
                ('cibilScore', models.TextField()),
                ('resedentialValue', models.TextField()),
                ('commercialValue', models.TextField()),
                ('luxuryValue', models.TextField()),
                ('bankAssets', models.TextField()),
                ('designation', models.TextField()),
                ('verified', models.TextField()),
            ],
        ),
    ]