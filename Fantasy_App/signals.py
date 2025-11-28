from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import UserProfile, Wallet, Currency

@receiver(post_save, sender=User)
def create_user_related_models(sender, instance, created, **kwargs):
    if created:
        print("PATRICKPATRICK PATRICK")
        # Create a UserProfile
        UserProfile.objects.create(user=instance)

        # Create a Wallet with default balance 0
        Wallet.objects.create(user=instance, balance=10000)
        currency = Currency.objects.first()
        if currency:
            currency.total_supply -= 10000
            currency.save()
        print("Created profile + wallet for:", instance.username)
