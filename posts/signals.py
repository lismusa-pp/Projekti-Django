from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Post
from .social_posting import post_to_facebook, post_to_linkedin

@receiver(post_save, sender=Post)
def auto_post_to_social(sender, instance, created, **kwargs):
    if created:
        post_to_facebook(instance)
        post_to_linkedin(instance)
