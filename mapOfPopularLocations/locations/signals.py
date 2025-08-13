from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import Review, ReviewSubscription

@receiver(post_save, sender=Review)
def send_review_email(sender, instance, created, **kwargs):
    if created:
        location = instance.location
        subscribers = ReviewSubscription.objects.filter(location=location, active=True)
        for sub in subscribers:
            send_mail(
                subject=f"New review for {location.title}",
                message=f"Review: {instance.text}",
                from_email=None,
                recipient_list=[sub.user.email],
            )
