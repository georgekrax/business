from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.views.generic import View, TemplateView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.gis.geoip2 import GeoIP2
import json, requests
from .models import Ad
from profiles.models import Configuration, Audience, Billing
from profiles.forms import ConfigurationForm, AudienceForm, BillingForm

class AjaxGetForm(View):
    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            ad_id = request.session.get('ad_id')
            ad_obj = Ad.objects.get(ad_id=ad_id)
            configuration_obj = Configuration.objects.get(ad_pk=ad_id)
            audience_obj = Audience.objects.get(ad_pk=ad_id)
            billing_obj = Billing.objects.get(ad_pk=ad_id)
            ad_ended = False

            if configuration_obj.submitted and audience_obj.submitted and billing_obj.submitted:
                ad_obj.status = 'ONGOING'
                ad_ended = True
                ad_obj.save()

            data = {
                "adEnded": ad_ended,
                "configurationObjSubmitted": configuration_obj.submitted,
                "audienceObjSubmitted": audience_obj.submitted,
                "billingObjSubmitted": billing_obj.submitted,
            }
            return JsonResponse(data)
        else:
            return redirect('home')

class CreateAdView(LoginRequiredMixin, TemplateView):
    template_name = 'ads/create.html'

    def get(self, request, ad_url_id=None, *args, **kwargs):
        ad_obj, ad_created = Ad.objects.new_or_get(request)
        if ad_url_id != ad_obj.ad_id:
            return redirect('ads:url-id', ad_url_id=ad_obj.ad_id)
        configuration_obj = Configuration.objects.get(ad_pk=ad_obj.ad_id)
        audience_obj = Audience.objects.get(ad_pk=ad_obj.ad_id)
        billing_obj = Billing.objects.get(ad_pk=ad_obj.ad_id)

        configuration_form = ConfigurationForm(instance=configuration_obj)
        audience_form = AudienceForm(instance=audience_obj)
        billing_form = BillingForm(instance=billing_obj)

        if configuration_obj.submitted and audience_obj.submitted and billing_obj.submitted:
            ad_obj.status = 'ONGOING'
            ad_obj.save()

        context = {
            "ad_obj": ad_obj,
            "configuration_obj": configuration_obj,
            "configuration_form": configuration_form,
            "audience_obj": audience_obj,
            "audience_form": audience_form,
            "billing_obj": billing_obj,
            "billing_form": billing_form
        }
        return render(request, self.template_name, context)

class CreateAd2View(LoginRequiredMixin, TemplateView):
    def get(self, request, *args, **kwargs):
        return redirect('ads:new')

    def post(self, request, *args, **kwargs):   
        ad_id = request.session.get('ad_id')
        configuration_obj = Configuration.objects.get(ad_pk=ad_id)
        form = ConfigurationForm(request.POST)
        if form.is_valid():
            marketing_objective = form.cleaned_data['marketing_objective']
            name = form.cleaned_data['name']
            website = form.cleaned_data['website']
            country = form.cleaned_data['country']
            configuration_obj.marketing_objective = marketing_objective
            configuration_obj.name = name
            configuration_obj.website = website
            configuration_obj.country = country
            configuration_obj.submitted = True
            configuration_obj.save()
            if request.is_ajax():
                data = {
                    "configurationObjSubmitted": configuration_obj.submitted
                }
                return JsonResponse(data)
            return redirect('ads:new')
        else:
            return HttpResponse('Error 1')


class CreateAd3View(LoginRequiredMixin, TemplateView):
    def get(self, request, *args, **kwargs):
        return redirect('ads:new')

    def post(self, request, *args, **kwargs):
        ad_id = request.session.get('ad_id')
        audience_obj = Audience.objects.get(ad_pk=ad_id)
        form = AudienceForm(request.POST)
        if form.is_valid():
            community = form.cleaned_data['community']
            audience_obj.community = community
            audience_obj.submitted = True
            audience_obj.save()
            if request.is_ajax():
                json_data = {
                    "audienceObjSubmitted": audience_obj.submitted,
                }
                return JsonResponse(json_data)
            return redirect('ads:new')
        else:
            return HttpResponse('Error 2')


class CreateAd4View(LoginRequiredMixin, TemplateView):
    def get(self, request, *args, **kwargs):
        return redirect('ads:new')

    def post(self, request, *args, **kwargs):
        ad_id = request.session.get('ad_id')
        billing_obj = Billing.objects.get(ad_pk=ad_id)
        form = BillingForm(request.POST)
        if form.is_valid():
            daily_budget = form.cleaned_data['daily_budget']
            billing_obj.daily_budget = daily_budget
            billing_obj.submitted = True
            billing_obj.save()
            if request.is_ajax():
                json_data = {
                    "billingObjSubmitted": billing_obj.submitted,
                    "msg": "Your ad is created successfully!"
                }
                return JsonResponse(json_data)
            return redirect('ads:new')
        else:
            return HttpResponse('Error 3')