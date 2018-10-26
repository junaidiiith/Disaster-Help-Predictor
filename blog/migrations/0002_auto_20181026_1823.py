# Generated by Django 2.0 on 2018-10-26 18:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='vote',
            field=models.IntegerField(choices=[(1, 'Caution/Advice'), (2, 'Damage'), (3, 'Disease'), (4, 'Information'), (5, 'Need Help'), (6, 'Other'), (7, 'People Affected'), (8, 'Support')]),
        ),
    ]
