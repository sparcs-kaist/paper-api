# Generated by Django 2.0.7 on 2018-07-31 16:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('answers', '0004_auto_20180728_1550'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='participate',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answers', to='answers.Participate'),
        ),
        migrations.AlterField(
            model_name='answer',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answers', to='papers.Question'),
        ),
        migrations.AlterField(
            model_name='select',
            name='answer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='selects', to='answers.Answer'),
        ),
    ]
