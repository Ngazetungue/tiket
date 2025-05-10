from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('buy-tickets/', views.buy_ticket, name='checkout'),
    path('events/', views.events, name='events'),
    path('event/<int:event_id>/', views.event_detail, name='event_detail'),
    path('payout/', views.payout, name='payout'),
    path('community/', views.community, name='community'),
    path('terms-conditions/', views.terms, name='terms'),
    path('help-center/', views.help_center, name='help_center'),
    path('privacy-policy/', views.privacy, name='privacy'),
    path('careers/', views.careers, name='careers'),
    path('contact-us/', views.contact, name='contact'),

    path('create-checkout-session/<int:event_id>/', views.create_checkout_session, name='create_checkout_session'),
    path('success/', views.success, name='success'),
    path('cancel/', views.cancel, name='cancel'),
    path('webhook/', views.stripe_webhook, name='stripe_webhook'),

]