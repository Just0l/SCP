# Generated by Django 4.1.4 on 2022-12-22 20:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('User', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ordered_parts',
            fields=[
                ('op_id', models.IntegerField(primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Parts',
            fields=[
                ('part_no', models.IntegerField(primary_key=True, serialize=False)),
                ('P_name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Workshop_orders',
            fields=[
                ('wo_id', models.IntegerField(primary_key=True, serialize=False)),
                ('W_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='User.workshopprofile')),
                ('op_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='SCP.ordered_parts')),
            ],
        ),
        migrations.CreateModel(
            name='Workshop_Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image_field', models.ImageField(default='no-image.jpg', height_field='imageheight', upload_to='static/images/profile/20221222-204110', width_field='imagewidth')),
                ('imagewidth', models.PositiveIntegerField(default=50, editable=False)),
                ('imageheight', models.PositiveIntegerField(default=50, editable=False)),
                ('W_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='User.workshopprofile')),
            ],
        ),
        migrations.CreateModel(
            name='Store_parts',
            fields=[
                ('sp_id', models.IntegerField(primary_key=True, serialize=False)),
                ('P_name', models.CharField(max_length=100)),
                ('desc', models.CharField(max_length=200)),
                ('car_make', models.CharField(max_length=50)),
                ('S_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='User.storeprofile')),
                ('part_no', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='SCP.parts')),
            ],
        ),
        migrations.CreateModel(
            name='Store_Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image_field', models.ImageField(default='no-image.jpg', height_field='imageheight', upload_to='static/images/profile/20221222-204110', width_field='imagewidth')),
                ('imagewidth', models.PositiveIntegerField(default=50, editable=False)),
                ('imageheight', models.PositiveIntegerField(default=50, editable=False)),
                ('S_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='User.storeprofile')),
            ],
        ),
        migrations.CreateModel(
            name='Services',
            fields=[
                ('service_id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=75)),
                ('W_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='User.workshopprofile')),
            ],
        ),
        migrations.CreateModel(
            name='Part_Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image_field', models.ImageField(default='no-image.jpg', height_field='imageheight', upload_to='static/images/profile/20221222-204110', width_field='imagewidth')),
                ('imagewidth', models.PositiveIntegerField(default=65, editable=False)),
                ('imageheight', models.PositiveIntegerField(default=65, editable=False)),
                ('P_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='SCP.parts')),
            ],
        ),
        migrations.AddField(
            model_name='ordered_parts',
            name='sp_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='SCP.store_parts'),
        ),
        migrations.CreateModel(
            name='Offers',
            fields=[
                ('offer_id', models.IntegerField(primary_key=True, serialize=False)),
                ('offer_desc', models.CharField(max_length=200)),
                ('offer_price', models.IntegerField()),
                ('W_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='User.workshopprofile')),
                ('service_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='SCP.services')),
            ],
        ),
        migrations.CreateModel(
            name='Customer_orders',
            fields=[
                ('co_id', models.IntegerField(primary_key=True, serialize=False)),
                ('C_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='User.customerprofile')),
                ('S_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='User.storeprofile')),
                ('op_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='SCP.ordered_parts')),
            ],
        ),
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Date', models.DateField()),
                ('Time', models.TimeField()),
                ('C_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='User.customerprofile')),
                ('W_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='User.workshopprofile')),
                ('service_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='SCP.services')),
            ],
        ),
    ]
