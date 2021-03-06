# Generated by Django 3.1.1 on 2020-09-10 04:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0014_auto_20200908_2219'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='supplier',
            field=models.CharField(default='JBird Coffee', max_length=200),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='order',
            name='order_id',
            field=models.CharField(default='e8e4f2519ba54e15ab83d6a784e7c7c3', max_length=32),
        ),
        migrations.AlterField(
            model_name='product',
            name='product_image',
            field=models.ImageField(upload_to='images/'),
        ),
    ]
