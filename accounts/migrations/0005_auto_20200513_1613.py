# Generated by Django 3.0.5 on 2020-05-13 10:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_auto_20200505_0009'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='note',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='tag',
            field=models.ManyToManyField(to='accounts.Tag'),
        ),
    ]