from django.db import models

from django_countries.fields import CountryField

class ConfigurationManager(models.Manager):
    def get(self, ad_pk=None):
        if ad_pk is not None:
            qs = Configuration.objects.filter(ad_pk=ad_pk)
            if qs.count() == 1:
                configuration_obj = qs.first()
            else:
                raise ValueError('Error multiple or None Configuration profiles')
            return configuration_obj
        else:
            raise ValueError('Every Configuration profile of an Ad has an ad_id or ad_pk')

MARKETING_OBJECTIVE_CHOICES = (
    ('LIKES', 'Likes'),
    ('COMMENTS', 'Comments'),
    ('LIKES&COMMENTS', 'Likes & Comments'),
)

class Configuration(models.Model):
    ad_pk               = models.CharField(max_length=16, null=True, blank=True)
    marketing_objective = models.CharField(max_length=16, choices=MARKETING_OBJECTIVE_CHOICES)
    name                = models.CharField(max_length=250)
    website             = models.URLField(null=True, blank=True)
    country             = CountryField(blank_label='Select your country', null=True, blank=True)
    access_token        = models.CharField(max_length=50, null=True, blank=True)
    updated             = models.DateTimeField(auto_now=True)
    timestamp           = models.DateTimeField(auto_now_add=True)
    submitted           = models.BooleanField(default=False)

    objects             = ConfigurationManager()

    def __str__(self):
        return self.ad_pk


class AudienceManager(models.Manager):
    def get(self, ad_pk=None):
        if ad_pk is not None:
            qs = Audience.objects.filter(ad_pk=ad_pk)
            if qs.count() == 1:
                audience_obj = qs.first()
            else:
                raise ValueError('Error multiple or None Configuration profiles')
            return audience_obj
        else:
            raise ValueError('Every Audience profile of an Ad has an ad_id or ad_pk')

AUDIENCE_COMMUNITY_CHOICES = (
    ('ADULTS', 'Adults'),
    ('TEENS', 'Teenagers'),
    ('CHILDREN', 'Children'),
)

class Audience(models.Model):
    ad_pk           = models.CharField(max_length=16, null=True, blank=True)
    community       = models.CharField(max_length=9, choices=AUDIENCE_COMMUNITY_CHOICES)
    updated         = models.DateTimeField(auto_now=True)
    timestamp       = models.DateTimeField(auto_now_add=True)
    submitted       = models.BooleanField(default=False)

    objects         = AudienceManager()

    def __str__(self):
        return self.ad_pk

class BillingManager(models.Manager):
    def get(self, ad_pk=None):
        if ad_pk is not None:
            qs = Billing.objects.filter(ad_pk=ad_pk)
            if qs.count() == 1:
                billing_obj = qs.first()
            else:
                raise ValueError('Error multiple or None Billing profiles')
            return billing_obj
        else:
            raise ValueError('Every Billing profile of an Ad has an ad_id or ad_pk')

class Billing(models.Model):
    ad_pk          = models.CharField(max_length=16, null=True, blank=True)
    daily_budget   = models.DecimalField(max_digits=5, decimal_places=2, default=5.00)
    updated        = models.DateTimeField(auto_now=True)
    timestamp      = models.DateTimeField(auto_now_add=True)
    submitted      = models.BooleanField(default=False)

    objects         = BillingManager()

    def __str__(self):
        return self.ad_pk