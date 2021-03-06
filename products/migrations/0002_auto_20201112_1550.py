# Generated by Django 3.1.3 on 2020-11-12 15:50

from django.db import migrations
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name_plural': 'Categories'},
        ),
        migrations.AddField(
            model_name='product',
            name='shoe_sizes',
            field=multiselectfield.db.fields.MultiSelectField(blank=True, choices=[('5', 'Size 5'), ('6', 'Size 6'), ('7', 'Size 7'), ('8', 'Size 8'), ('9', 'Size 9'), ('10', 'Size 10'), ('11', 'Size 11'), ('12', 'Size 12')], max_length=18, null=True),
        ),
    ]
