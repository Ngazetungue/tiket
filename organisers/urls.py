from django.urls import path
from . import views

app_name = 'organisers'

urlpatterns = [
    # ====================== DASHBOARD URLs ======================
    path('dashboard/', views.dashboard, name='dashboard'),

    # ====================== ORGANIZER URLs ======================
    path('organizers/', views.organizer_list, name='organizer_list'),
    path('organizers/create/', views.organizer_create, name='organizer_create'),
    path('organizers/<int:pk>/', views.organizer_detail, name='organizer_detail'),
    path('organizers/<int:pk>/update/', views.organizer_update, name='organizer_update'),
    path('organizers/<int:pk>/delete/', views.organizer_delete, name='organizer_delete'),

    # ====================== PURCHASER URLs ======================
    path('purchasers/', views.purchaser_list, name='purchaser_list'),
    path('purchasers/create/', views.purchaser_create, name='purchaser_create'),
    path('purchasers/<int:pk>/', views.purchaser_detail, name='purchaser_detail'),
    path('purchasers/<int:pk>/update/', views.purchaser_update, name='purchaser_update'),
    path('purchasers/<int:pk>/delete/', views.purchaser_delete, name='purchaser_delete'),

    # ====================== EVENT URLs ======================
    path('events/', views.event_list, name='event_list'),
    path('events/create/', views.event_create, name='event_create'),
    path('events/<int:pk>/', views.event_detail, name='event_detail'),
    path('events/<int:pk>', views.event_update, name='event_update'),
    path('events/<int:pk>', views.event_delete, name='event_delete'),

    # ====================== PROMO CODE URLs ======================
    path('promo-codes/', views.promo_code_list, name='promo_code_list'),
    path('promo-codes/create/', views.promo_code_create, name='promo_code_create'),
    path('promo-codes/<int:pk>/', views.promo_code_detail, name='promo_code_detail'),
    path('promo-codes/<int:pk>/update/', views.promo_code_update, name='promo_code_update'),
    path('promo-codes/<int:pk>/delete/', views.promo_code_delete, name='promo_code_delete'),

    # ====================== ORDER URLs ======================
    path('orders/', views.order_list, name='order_list'),
    path('orders/create/', views.order_create, name='order_create'),
    path('orders/<int:pk>/', views.order_detail, name='order_detail'),
    path('orders/<int:pk>/update/', views.order_update, name='order_update'),
    path('orders/<int:pk>/delete/', views.order_delete, name='order_delete'),

    # ====================== ORDER ITEM URLs ======================
    path('orders/<int:order_pk>/items/create/', views.order_item_create, name='order_item_create'),
    path('order-items/<int:pk>/update/', views.order_item_update, name='order_item_update'),
    path('order-items/<int:pk>/delete/', views.order_item_delete, name='order_item_delete'),

    # ====================== ATTENDEE URLs ======================
    path('orders/<int:order_pk>/attendees/create/', views.attendee_create, name='attendee_create'),
    path('attendees/<int:pk>/update/', views.attendee_update, name='attendee_update'),
    path('attendees/<int:pk>/delete/', views.attendee_delete, name='attendee_delete'),

    # ====================== EVENT TICKET URLs ======================
    path('tickets/', views.event_ticket_list, name='event_ticket_list'),
    path('tickets/<int:pk>/', views.event_ticket_detail, name='event_ticket_detail'),
    path('tickets/<int:pk>/delete/', views.event_ticket_delete, name='event_ticket_delete'),

    # ====================== PAYMENT URLs ======================
    path('orders/<int:order_pk>/payments/create/', views.payment_create, name='payment_create'),
    path('payments/<int:pk>/update/', views.payment_update, name='payment_update'),
    path('payments/<int:pk>/delete/', views.payment_delete, name='payment_delete'),

    # ====================== CHECK-IN URLs ======================
    path('tickets/<int:ticket_pk>/check-ins/create/', views.check_in_create, name='check_in_create'),
    path('check-ins/<int:pk>/delete/', views.check_in_delete, name='check_in_delete'),

    # ====================== DEVICE URLs ======================
    path('devices/', views.device_list, name='device_list'),
    path('devices/create/', views.device_create, name='device_create'),
    path('devices/<int:pk>/update/', views.device_update, name='device_update'),
    path('devices/<int:pk>/delete/', views.device_delete, name='device_delete'),

    # ====================== PAYOUT URLs ======================
    path('payouts/', views.payout_list, name='payout_list'),
    path('payouts/create/', views.payout_create, name='payout_create'),
    path('payouts/<int:pk>/', views.payout_detail, name='payout_detail'),
    path('payouts/<int:pk>/delete/', views.payout_delete, name='payout_delete'),
]