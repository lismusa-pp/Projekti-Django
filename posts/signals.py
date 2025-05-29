from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Post
from .social_posting import post_to_facebook, post_to_linkedin

@receiver(post_save, sender=Post)
def auto_post_to_social(sender, instance, created, **kwargs):
    if created:
        post_to_facebook(instance)
        post_to_linkedin(instance)

import requests
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Post
from django.conf import settings

@receiver(post_save, sender=Post)
def post_to_social_media(sender, instance, created, **kwargs):
    if created:
        # Send to Facebook
        fb_url = f"https://graph.facebook.com/{settings.FACEBOOK_PAGE_ID}/photos"
        fb_data = {
            "url": instance.image.url if instance.image else "",
            "caption": f"{instance.title}\n\n{instance.body}",
            "access_token": settings.FACEBOOK_PAGE_ACCESS_TOKEN
        }
        try:
            requests.post(fb_url, data=fb_data)
        except Exception as e:
            print("Facebook Error:", e)

        # Send to LinkedIn
        linkedin_url = "https://api.linkedin.com/v2/ugcPosts"
        linkedin_headers = {
            "Authorization": f"Bearer {settings.LINKEDIN_ACCESS_TOKEN}",
            "X-Restli-Protocol-Version": "2.0.0",
            "Content-Type": "application/json"
        }
        linkedin_payload = {
            "author": f"urn:li:organization:{settings.LINKEDIN_ORGANIZATION_ID}",
            "lifecycleState": "PUBLISHED",
            "specificContent": {
                "com.linkedin.ugc.ShareContent": {
                    "shareCommentary": {
                        "text": f"{instance.title}\n\n{instance.body}"
                    },
                    "shareMediaCategory": "NONE"
                }
            },
            "visibility": {
                "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
            }
        }
        try:
            requests.post(linkedin_url, headers=linkedin_headers, json=linkedin_payload)
        except Exception as e:
            print("LinkedIn Error:", e)
