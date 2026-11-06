from django.urls import path

from .views import AjaxGetForm, CreateAdView, CreateAd2View, CreateAd3View, CreateAd4View

app_name = 'ads'

urlpatterns = [
    path('new/<ad_url_id>/', CreateAdView.as_view(), name='url-id'),
    path('new/', CreateAdView.as_view(), name='new'),
    path('new/step/2', CreateAd2View.as_view(), name='new-2'),
    path('new/step/3', CreateAd3View.as_view(), name='new-3'),
    path('new/step/4',CreateAd4View.as_view(), name='new-4'),
    path('ajax/get/form/', AjaxGetForm.as_view(), name='ajax-get-form'),
]