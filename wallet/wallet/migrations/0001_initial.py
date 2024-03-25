# Generated by Django 4.2.11 on 2024-03-25 10:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Currency',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('country', models.CharField(max_length=80)),
                ('currency', models.CharField(max_length=50)),
                ('code', models.CharField(max_length=3)),
                ('number', models.PositiveSmallIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=6)),
                ('created', models.DateTimeField(default=django.utils.timezone.localtime)),
                ('currency', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='wallet.currency')),
            ],
            options={
                'ordering': ['created'],
            },
        ),
        migrations.CreateModel(
            name='WalletHolder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Wallet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid', models.UUIDField(default=uuid.uuid4, unique=True)),
                ('balance', models.DecimalField(decimal_places=2, max_digits=6)),
                ('currency', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='wallet.currency')),
                ('holder', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='wallet.walletholder')),
                ('transactions', models.ManyToManyField(through='wallet.Transaction', to='wallet.wallet')),
            ],
        ),
        migrations.AddField(
            model_name='transaction',
            name='receiver',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='transaction_receiver', to='wallet.wallet'),
        ),
        migrations.AddField(
            model_name='transaction',
            name='sender',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='transaction_sender', to='wallet.wallet'),
        ),
    ]