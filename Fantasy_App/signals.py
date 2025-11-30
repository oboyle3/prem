from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import GolfersInDatabase, UserProfile, Wallet, Currency, UserTrackedGolfers

@receiver(post_save, sender=User)
def create_user_related_models(sender, instance, created, **kwargs):
    if created:
        print("PATRICKPATRICK PATRICK")
        # Create a UserProfile
        UserProfile.objects.create(user=instance)

        # Create a Wallet with default balance 0
        Wallet.objects.create(user=instance, balance=10000)
        currency = Currency.objects.first()
        lineup = UserTrackedGolfers.objects.create(user=instance)
        lineup.slot1 = GolfersInDatabase.objects.filter(rating__gte=9).first()
        lineup.slot2 = GolfersInDatabase.objects.filter(rating__gte=7, rating__lte=8).first()
        lineup.slot3 = GolfersInDatabase.objects.filter(rating__gte=5, rating__lte=6).first()
        lineup.slot4 = GolfersInDatabase.objects.filter(rating__gte=3, rating__lte=4).first()
        lineup.slot5 = GolfersInDatabase.objects.filter(rating__gte=1, rating__lte=2).first()

        # STEP 3: save
        lineup.save()
        if currency:
            currency.total_supply -= 10000
            currency.save()
        print("Created profile + wallet for:", instance.username)
