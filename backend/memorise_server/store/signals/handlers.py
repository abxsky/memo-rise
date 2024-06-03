from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from store.models import Customer

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_customer_for_new_user(sender, instance, created, **kwargs):
    if created:
        try:
            if not Customer.objects.filter(user=instance).exists():
                Customer.objects.create(user=instance)
        except Exception as e:
            print(f"Erreur pour la creéation de l'utilisateur {instance}: {e}")
