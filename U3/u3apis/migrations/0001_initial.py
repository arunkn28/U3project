# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-08-15 06:47
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0008_alter_user_username_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(max_length=50, unique=True, verbose_name='User Name')),
                ('phone_number', models.CharField(blank=True, max_length=15, verbose_name='Phone Number')),
                ('email', models.EmailField(blank=True, max_length=50, verbose_name='Email Id')),
                ('adi', models.CharField(blank=True, max_length=20, verbose_name='ADI')),
                ('login_source', models.CharField(blank=True, max_length=20, verbose_name='Login Source')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'db_table': 's_t_userdetails',
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('sort', models.IntegerField()),
            ],
            options={
                'db_table': 's_t_cat',
            },
        ),
        migrations.CreateModel(
            name='FeedBackLabel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=10, verbose_name='Feedback Label')),
            ],
            options={
                'db_table': 's_t_feedback',
            },
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('sort', models.IntegerField()),
                ('description', models.CharField(max_length=100)),
                ('type', models.CharField(max_length=10)),
                ('price', models.DecimalField(decimal_places=2, max_digits=7)),
                ('availabilty', models.BooleanField(default=False)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='u3apis.Category')),
            ],
            options={
                'db_table': 's_t_item',
            },
        ),
        migrations.CreateModel(
            name='MobileOTPTemp',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_number', models.CharField(blank=True, max_length=15, verbose_name='Phone Number')),
                ('otp', models.IntegerField(blank=True)),
            ],
            options={
                'db_table': 's_t_temp',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_quantity', models.IntegerField()),
                ('item_price', models.DecimalField(decimal_places=2, max_digits=7)),
                ('username', models.CharField(max_length=50)),
                ('delivered', models.BooleanField(default=False)),
                ('prepared', models.BooleanField(default=False)),
                ('order_time', models.DateTimeField(blank=True)),
                ('delivery_time', models.DateTimeField(blank=True)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='u3apis.Item')),
            ],
            options={
                'db_table': 's_t_placedorder',
            },
        ),
        migrations.CreateModel(
            name='QRCode',
            fields=[
                ('qr_code', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('active', models.BooleanField(default=False)),
                ('order_code', models.IntegerField()),
                ('waiter', models.BooleanField(default=False)),
                ('freeze_bill', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 's_t_qrcode',
            },
        ),
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.IntegerField()),
                ('label_code', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='u3apis.FeedBackLabel')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 's_t_rating',
            },
        ),
        migrations.CreateModel(
            name='ResDetails',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('res_name', models.CharField(blank=True, max_length=50, verbose_name='Phone Number')),
                ('res_address', models.CharField(blank=True, max_length=100, verbose_name='Residentail Address')),
            ],
            options={
                'db_table': 's_t_resDetails',
            },
        ),
        migrations.CreateModel(
            name='Table',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('area_name', models.CharField(max_length=25)),
                ('num_of_tables', models.IntegerField()),
                ('res_code', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='u3apis.ResDetails')),
            ],
            options={
                'db_table': 's_t_table',
            },
        ),
        migrations.CreateModel(
            name='TableCode',
            fields=[
                ('table_code', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('res_code', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='u3apis.ResDetails')),
            ],
            options={
                'db_table': 's_t_tablecode',
            },
        ),
        migrations.CreateModel(
            name='Variable',
            fields=[
                ('var_name', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('var_value', models.IntegerField()),
            ],
            options={
                'db_table': 's_t_variable',
            },
        ),
        migrations.AddField(
            model_name='qrcode',
            name='res_code',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='u3apis.ResDetails'),
        ),
        migrations.AddField(
            model_name='qrcode',
            name='table_code',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='u3apis.TableCode'),
        ),
        migrations.AddField(
            model_name='order',
            name='res_code',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='u3apis.ResDetails'),
        ),
        migrations.AddField(
            model_name='order',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='item',
            name='res_code',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='u3apis.ResDetails'),
        ),
        migrations.AddField(
            model_name='category',
            name='res_code',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='u3apis.ResDetails'),
        ),
    ]
