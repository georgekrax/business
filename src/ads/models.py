from django.conf import settings
from django.db import models
from django.db.models.signals import pre_save, post_save, post_delete

from profiles.models import Configuration, Audience, Billing
from .utils import unique_ad_id_generator

class AdManager(models.Manager):
    def new_or_get(self, request):
        ad_id = request.session.get('ad_id', None)
        qs = self.model.objects.all().filter(ad_id=ad_id)
        if qs.count() == 1:
            new_obj = False
            ad_obj = qs.first()
        else:
            ad_obj = Ad.objects.new(request.user)
            new_obj = True
            request.session['ad_id'] = ad_obj.ad_id
        return ad_obj, new_obj

    def new(self, user=None):
        user_obj = None
        if user.is_authenticated:
                user_obj = user
        else:
            raise ValueError('User cannot be None')
        return self.model.objects.create(user=user_obj)

    def all(self):
        qs = self.get_queryset().exclude(status='ONGOING')
        return qs

AD_STATUS_CHOICES = (
    ('CREATED', 'Created'),
    ('ONGOING', 'Ongoing'),
    ('POSTED', 'Posted'),
    ('ENDED', 'Ended')
)

class Ad(models.Model):
    user                    = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ad_id                   = models.CharField(max_length=16, unique=True, null=True, blank=True)
    configuration_profile   = models.OneToOneField(Configuration, on_delete=models.CASCADE, null=True, blank=True)
    audience_profile        = models.OneToOneField(Audience, on_delete=models.CASCADE, null=True, blank=True)
    billing_profile         = models.OneToOneField(Billing, on_delete=models.CASCADE, null=True, blank=True)
    status                  = models.CharField(max_length=7, choices=AD_STATUS_CHOICES, default='CREATED')
    updated                 = models.DateTimeField(auto_now=True)
    timestamp               = models.DateTimeField(auto_now_add=True)

    objects                 = AdManager()

    def __str__(self):
        return self.ad_id

def unique_ad_id_generator_receiver(sender, instance, *args, **kwargs):
    if not instance.ad_id:
        instance.ad_id = unique_ad_id_generator(instance)

    if not instance.configuration_profile:
        configuration_profiles_qs = Configuration.objects.filter(ad_pk=instance.ad_id)
        if configuration_profiles_qs.exists():
            configuration_profiles_qs.delete()
        instance.configuration_profile = Configuration.objects.create(ad_pk=instance.ad_id)
        
    if not instance.audience_profile:
        audience_profiles_qs = Audience.objects.filter(ad_pk=instance.ad_id)
        if audience_profiles_qs.exists():
            audience_profiles_qs.delete()
        instance.audience_profile = Audience.objects.create(ad_pk=instance.ad_id)

    if not instance.billing_profile:
        billing_profile_qs = Billing.objects.filter(ad_pk=instance.ad_id)
        if billing_profile_qs.exists():
            billing_profile_qs.delete()
        instance.billing_profile = Billing.objects.create(ad_pk=instance.ad_id)
    
pre_save.connect(unique_ad_id_generator_receiver, sender=Ad)

def post_delete_ad_receiver(sender, instance, *args, **kwargs):
    configuration_profile_qs = Configuration.objects.filter(ad_pk=instance.ad_id)
    audience_profile_qs = Audience.objects.filter(ad_pk=instance.ad_id)
    billing_profile_qs = Billing.objects.filter(ad_pk=instance.ad_id)
    audience_profile_qs.delete()
    configuration_profile_qs.delete()
    billing_profile_qs.delete()

post_delete.connect(post_delete_ad_receiver, sender=Ad)
