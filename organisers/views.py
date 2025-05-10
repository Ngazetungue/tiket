
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.core.paginator import Paginator
from .models import (
    Organizer, Purchaser, Event, PromoCode,
    Order, OrderItem, Attendee, EventTicket,
    Payment, CheckIn, Device, Payout
)
from .forms import (
    OrganizerForm, PurchaserForm, EventForm,
    PromoCodeForm, OrderForm, OrderItemForm,
    AttendeeForm, EventTicketForm, PaymentForm,
    CheckInForm, DeviceForm, PayoutForm
)

from users.models import CustomUser, Profile

from django.utils import timezone

# ====================== HOMEPAGE VIEWS ======================
def event_list(request):
    events = Event.objects.all()
    return render(request,'home/home.html',{'events':events})

# ====================== DASHBOARD VIEWS ======================
@login_required
def dashboard(request):
    user = request.user

    if user.user_type == 'staff':
        template = 'organisers/staff-dashboard.html'
    elif user.user_type == 'organiser':
        template = 'organisers/organiser-dashboard.html'
    else:
        user.user_type == 'admin'
        template = 'organisers/admin-dashboard.html'
    
    return render(request, template)

# ====================== ORGANIZER VIEWS ======================
@login_required
@permission_required('organisers.view_organizer', raise_exception=True)
def organizer_list(request):
    organizers = Organizer.objects.all().order_by('-verified', 'user__last_name')
    paginator = Paginator(organizers, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'organizers/list.html', {'page_obj': page_obj})

@login_required
@permission_required('organisers.add_organizer', raise_exception=True)
def organizer_create(request):
    if request.method == 'POST':
        form = OrganizerForm(request.POST)
        if form.is_valid():
            organizer = form.save()
            messages.success(request, f'Organizer {organizer.user.get_full_name()} created successfully!')
            return redirect('organizer_detail', pk=organizer.pk)
    else:
        form = OrganizerForm()
    return render(request, 'organizers/form.html', {'form': form, 'action': 'Create'})

@login_required
@permission_required('organisers.change_organizer', raise_exception=True)
def organizer_update(request, pk):
    organizer = get_object_or_404(Organizer, pk=pk)
    if request.method == 'POST':
        form = OrganizerForm(request.POST, instance=organizer)
        if form.is_valid():
            form.save()
            messages.success(request, 'Organizer updated successfully!')
            return redirect('organizer_detail', pk=organizer.pk)
    else:
        form = OrganizerForm(instance=organizer)
    return render(request, 'organizers/form.html', {'form': form, 'action': 'Update'})

@login_required
@permission_required('organisers.view_organizer', raise_exception=True)
def organizer_detail(request, pk):
    organizer = get_object_or_404(Organizer, pk=pk)
    events = Event.objects.filter(organizer=organizer)
    return render(request, 'organizers/detail.html', {
        'organizer': organizer,
        'events': events
    })

# ====================== PURCHASER VIEWS ======================
@login_required
def purchaser_list(request):
    purchasers = Purchaser.objects.all().order_by('-created_at')
    paginator = Paginator(purchasers, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'purchasers/list.html', {'page_obj': page_obj})

@login_required
def purchaser_create(request):
    if request.method == 'POST':
        form = PurchaserForm(request.POST)
        if form.is_valid():
            purchaser = form.save()
            messages.success(request, f'Purchaser {purchaser.full_name} created successfully!')
            return redirect('purchaser_detail', pk=purchaser.pk)
    else:
        form = PurchaserForm()
    return render(request, 'purchasers/form.html', {'form': form, 'action': 'Create'})

@login_required
def purchaser_update(request, pk):
    purchaser = get_object_or_404(Purchaser, pk=pk)
    if request.method == 'POST':
        form = PurchaserForm(request.POST, instance=purchaser)
        if form.is_valid():
            form.save()
            messages.success(request, 'Purchaser updated successfully!')
            return redirect('purchaser_detail', pk=purchaser.pk)
    else:
        form = PurchaserForm(instance=purchaser)
    return render(request, 'purchasers/form.html', {'form': form, 'action': 'Update'})

@login_required
def purchaser_detail(request, pk):
    purchaser = get_object_or_404(Purchaser, pk=pk)
    orders = Order.objects.filter(purchaser=purchaser)
    return render(request, 'purchasers/detail.html', {
        'purchaser': purchaser,
        'orders': orders
    })

# ====================== EVENT VIEWS ======================

@login_required(login_url='/accounts/login/')
def event_list(request):
    if not request.user.is_authenticated:
        return redirect('login') 

    events = Event.objects.filter(
        organizer=request.user,
        is_active=True
    ).order_by('start_date')
    
    for event in events:
        try:
            sales_percentage = (event.tickets_sold / event.capacity) * 100 if event.capacity > 0 else 0
        except (AttributeError, ZeroDivisionError):
            sales_percentage = 0
        
        if sales_percentage >= 100:
            event.badge_color = 'bg-green-100 text-green-800'
            event.sales_status = 'Sold Out'
        elif sales_percentage >= 70:
            event.badge_color = 'bg-blue-100 text-blue-800'
            event.sales_status = 'Selling Fast'
        else:
            event.badge_color = 'bg-yellow-100 text-yellow-800'
            event.sales_status = 'Available'
            
        event.revenue_display = f"NAD {event.revenue:,.2f}"
    
    return render(request, "organisers/event-list.html", {"events": events})

@login_required
def event_create(request):
    try:
        organizer = Profile.objects.get(user=request.user)
    except Organizer.DoesNotExist:
        return redirect('some_error_page')

    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            event = form.save(commit=False)
            event.organizer = request.user 
            event.save()
            return redirect('organisers:event_list') 
    else:
        initial_data = {
            'start_date': timezone.now() + timezone.timedelta(days=7),
            'end_date': timezone.now() + timezone.timedelta(days=7, hours=2),
            'sales_start': timezone.now(),
            'sales_end': timezone.now() + timezone.timedelta(days=6),
        }
        form = EventForm(initial=initial_data)

    return render(request, 'organisers/create-event.html', {
        'form': form,
        'organizer': organizer,
    })

@login_required
def event_update(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES, instance=event)
        if form.is_valid():
            form.save()
            messages.success(request, 'Event updated successfully!')
            return redirect('organisers:event_detail', pk=event.pk)
    else:
        form = EventForm(instance=event)
    return render(request, 'organisers/event-update.html', {'form': form, 'action': 'Update'})

def event_detail(request, pk):
    event = get_object_or_404(Event, pk=pk)
    return render(request, 'organisers/event-detail.html', {
        'event': event,
    })

@login_required
def event_delete(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.method == 'POST':
        event.delete()
        messages.success(request, 'Event deleted successfully!')
        return redirect('organisers:event_list')
    return render(request, 'organisers/event-delete.html', {
        'object': event,})

# ====================== PROMO CODE VIEWS ======================
@login_required
def promo_code_list(request):
    promo_codes = PromoCode.objects.all().order_by('-valid_to')
    paginator = Paginator(promo_codes, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'organizers/list.html', {'page_obj': page_obj})

@login_required
def promo_code_create(request):
    if request.method == 'POST':
        form = PromoCodeForm(request.POST)
        if form.is_valid():
            promo_code = form.save()
            messages.success(request, f'Promo code "{promo_code.code}" created successfully!')
            return redirect('promo_code_detail', pk=promo_code.pk)
    else:
        form = PromoCodeForm()
    return render(request, 'organizers/form.html', {'form': form, 'action': 'Create'})

@login_required
def promo_code_update(request, pk):
    promo_code = get_object_or_404(PromoCode, pk=pk)
    if request.method == 'POST':
        form = PromoCodeForm(request.POST, instance=promo_code)
        if form.is_valid():
            form.save()
            messages.success(request, 'Promo code updated successfully!')
            return redirect('promo_code_detail', pk=promo_code.pk)
    else:
        form = PromoCodeForm(instance=promo_code)
    return render(request, 'organizers/form.html', {'form': form, 'action': 'Update'})

@login_required
def promo_code_detail(request, pk):
    promo_code = get_object_or_404(PromoCode, pk=pk)
    return render(request, 'organizers/detail.html', {'promo_code': promo_code})

# ====================== ORDER VIEWS ======================
@login_required
def order_list(request):
    orders = Order.objects.all().order_by('-created_at')
    
    # Filter for organizers to see only their events' orders
    if hasattr(request.user, 'organizer'):
        orders = orders.filter(event__organizer=request.user.organizer)
    
    paginator = Paginator(orders, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'orders/list.html', {'page_obj': page_obj})

@login_required
def order_create(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            if hasattr(request.user, 'purchaser'):
                order.purchaser = request.user.purchaser
            order.save()
            messages.success(request, f'Order #{order.order_number} created successfully!')
            return redirect('order_detail', pk=order.pk)
    else:
        form = OrderForm()
    return render(request, 'orders/form.html', {'form': form, 'action': 'Create'})

@login_required
def order_update(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            messages.success(request, 'Order updated successfully!')
            return redirect('order_detail', pk=order.pk)
    else:
        form = OrderForm(instance=order)
    return render(request, 'orders/form.html', {'form': form, 'action': 'Update'})

@login_required
def order_detail(request, pk):
    order = get_object_or_404(Order, pk=pk)
    return render(request, 'orders/detail.html', {'order': order})

# ====================== ORDER ITEM VIEWS ======================
@login_required
def order_item_create(request, order_pk):
    order = get_object_or_404(Order, pk=order_pk)
    if request.method == 'POST':
        form = OrderItemForm(request.POST)
        if form.is_valid():
            order_item = form.save(commit=False)
            order_item.order = order
            order_item.price = order_item.event.ticket_price
            order_item.total = order_item.price * order_item.quantity
            order_item.save()
            
            # Update order totals
            order.subtotal = sum(item.total for item in order.items.all())
            order.service_fee = order.subtotal * (order.event.service_fee_percentage / 100)
            order.total_amount = order.subtotal + order.service_fee - order.discount_amount
            order.save()
            
            messages.success(request, 'Ticket added to order successfully!')
            return redirect('order_detail', pk=order.pk)
    else:
        form = OrderItemForm(initial={'event': order.event})
    return render(request, 'order_items/form.html', {
        'form': form,
        'order': order,
        'action': 'Add'
    })

@login_required
def order_item_update(request, pk):
    order_item = get_object_or_404(OrderItem, pk=pk)
    if request.method == 'POST':
        form = OrderItemForm(request.POST, instance=order_item)
        if form.is_valid():
            order_item = form.save(commit=False)
            order_item.total = order_item.price * order_item.quantity
            order_item.save()
            
            # Update order totals
            order = order_item.order
            order.subtotal = sum(item.total for item in order.items.all())
            order.service_fee = order.subtotal * (order.event.service_fee_percentage / 100)
            order.total_amount = order.subtotal + order.service_fee - order.discount_amount
            order.save()
            
            messages.success(request, 'Order item updated successfully!')
            return redirect('order_detail', pk=order.pk)
    else:
        form = OrderItemForm(instance=order_item)
    return render(request, 'order_items/form.html', {
        'form': form,
        'order': order_item.order,
        'action': 'Update'
    })

# ====================== ATTENDEE VIEWS ======================
@login_required
def attendee_create(request, order_pk):
    order = get_object_or_404(Order, pk=order_pk)
    if request.method == 'POST':
        form = AttendeeForm(request.POST)
        if form.is_valid():
            attendee = form.save(commit=False)
            attendee.order = order
            attendee.save()
            messages.success(request, 'Attendee added successfully!')
            return redirect('order_detail', pk=order.pk)
    else:
        form = AttendeeForm()
    return render(request, 'attendees/form.html', {
        'form': form,
        'order': order,
        'action': 'Add'
    })

@login_required
def attendee_update(request, pk):
    attendee = get_object_or_404(Attendee, pk=pk)
    if request.method == 'POST':
        form = AttendeeForm(request.POST, instance=attendee)
        if form.is_valid():
            form.save()
            messages.success(request, 'Attendee updated successfully!')
            return redirect('order_detail', pk=attendee.order.pk)
    else:
        form = AttendeeForm(instance=attendee)
    return render(request, 'attendees/form.html', {
        'form': form,
        'order': attendee.order,
        'action': 'Update'
    })

# ====================== EVENT TICKET VIEWS ======================
@login_required
def event_ticket_list(request):
    tickets = EventTicket.objects.all().order_by('-created_at')
    paginator = Paginator(tickets, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'event_tickets/list.html', {'page_obj': page_obj})

@login_required
def event_ticket_detail(request, pk):
    ticket = get_object_or_404(EventTicket, pk=pk)
    check_ins = CheckIn.objects.filter(ticket=ticket)
    return render(request, 'event_tickets/detail.html', {
        'ticket': ticket,
        'check_ins': check_ins
    })

# ====================== PAYMENT VIEWS ======================
@login_required
def payment_create(request, order_pk):
    order = get_object_or_404(Order, pk=order_pk)
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.order = order
            payment.amount = order.total_amount
            payment.save()
            
            # Update order status if payment is completed
            if payment.status == 'completed':
                order.status = 'paid'
                order.save()
            
            messages.success(request, 'Payment recorded successfully!')
            return redirect('order_detail', pk=order.pk)
    else:
        form = PaymentForm(initial={
            'amount': order.total_amount,
            'status': 'pending'
        })
    return render(request, 'payments/form.html', {
        'form': form,
        'order': order,
        'action': 'Add'
    })

@login_required
def payment_update(request, pk):
    payment = get_object_or_404(Payment, pk=pk)
    if request.method == 'POST':
        form = PaymentForm(request.POST, instance=payment)
        if form.is_valid():
            payment = form.save()
            
            # Update order status if payment status changed
            order = payment.order
            if payment.status == 'completed' and order.status != 'paid':
                order.status = 'paid'
                order.save()
            elif payment.status != 'completed' and order.status == 'paid':
                order.status = 'pending'
                order.save()
            
            messages.success(request, 'Payment updated successfully!')
            return redirect('order_detail', pk=payment.order.pk)
    else:
        form = PaymentForm(instance=payment)
    return render(request, 'payments/form.html', {
        'form': form,
        'order': payment.order,
        'action': 'Update'
    })

# ====================== CHECK-IN VIEWS ======================
@login_required
def check_in_create(request, ticket_pk):
    ticket = get_object_or_404(EventTicket, pk=ticket_pk)
    if request.method == 'POST':
        form = CheckInForm(request.POST)
        if form.is_valid():
            check_in = form.save(commit=False)
            check_in.ticket = ticket
            check_in.save()
            
            # Update ticket status if not duplicate
            if not check_in.is_duplicate:
                ticket.status = 'used'
                ticket.save()
            
            messages.success(request, 'Check-in recorded successfully!')
            return redirect('event_ticket_detail', pk=ticket.pk)
    else:
        form = CheckInForm()
    return render(request, 'check_ins/form.html', {
        'form': form,
        'ticket': ticket,
        'action': 'Add'
    })

# ====================== DEVICE VIEWS ======================
@login_required
def device_list(request):
    devices = Device.objects.all().order_by('name')
    return render(request, 'devices/list.html', {'devices': devices})

@login_required
def device_create(request):
    if request.method == 'POST':
        form = DeviceForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Device added successfully!')
            return redirect('device_list')
    else:
        form = DeviceForm()
    return render(request, 'devices/form.html', {'form': form, 'action': 'Add'})

@login_required
def device_update(request, pk):
    device = get_object_or_404(Device, pk=pk)
    if request.method == 'POST':
        form = DeviceForm(request.POST, instance=device)
        if form.is_valid():
            form.save()
            messages.success(request, 'Device updated successfully!')
            return redirect('device_list')
    else:
        form = DeviceForm(instance=device)
    return render(request, 'devices/form.html', {'form': form, 'action': 'Update'})

# ====================== PAYOUT VIEWS ======================
@login_required
@permission_required('organisers.view_payout', raise_exception=True)
def payout_list(request):
    payouts = Payout.objects.all().order_by('-initiated_at')
    
    # Filter for organizers to see only their payouts
    if hasattr(request.user, 'organizer'):
        payouts = payouts.filter(organizer=request.user.organizer)
    
    paginator = Paginator(payouts, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'payouts/list.html', {'page_obj': page_obj})

@login_required
@permission_required('organisers.add_payout', raise_exception=True)
def payout_create(request):
    if request.method == 'POST':
        form = PayoutForm(request.POST)
        if form.is_valid():
            payout = form.save(commit=False)
            if hasattr(request.user, 'organizer'):
                payout.organizer = request.user.organizer
            payout.save()
            messages.success(request, f'Payout #{payout.reference} created successfully!')
            return redirect('payout_detail', pk=payout.pk)
    else:
        form = PayoutForm()
    return render(request, 'payouts/form.html', {'form': form, 'action': 'Create'})

@login_required
@permission_required('organisers.view_payout', raise_exception=True)
def payout_detail(request, pk):
    payout = get_object_or_404(Payout, pk=pk)
    return render(request, 'payouts/detail.html', {'payout': payout})


# ====================== ORGANIZER CRUD ======================
@login_required
def organizer_delete(request, pk):
    organizer = get_object_or_404(Organizer, pk=pk)
    if request.method == 'POST':
        organizer.delete()
        messages.success(request, 'Organizer deleted successfully!')
        return redirect('organizer_list')
    return render(request, 'delete_confirmation.html', {
        'object': organizer,
        'cancel_url': reverse('organizer_detail', kwargs={'pk': pk})
    })

# ====================== PURCHASER CRUD ======================
@login_required
def purchaser_delete(request, pk):
    purchaser = get_object_or_404(Purchaser, pk=pk)
    if request.method == 'POST':
        purchaser.delete()
        messages.success(request, 'Purchaser deleted successfully!')
        return redirect('purchaser_list')
    return render(request, 'delete_confirmation.html', {
        'object': purchaser,
        'cancel_url': reverse('purchaser_detail', kwargs={'pk': pk})
    })


# ====================== PROMO CODE CRUD ======================
@login_required
def promo_code_delete(request, pk):
    promo_code = get_object_or_404(PromoCode, pk=pk)
    if request.method == 'POST':
        promo_code.delete()
        messages.success(request, 'Promo code deleted successfully!')
        return redirect('promo_code_list')
    return render(request, 'delete_confirmation.html', {
        'object': promo_code,
        'cancel_url': reverse('promo_code_detail', kwargs={'pk': pk})
    })

# ====================== ORDER CRUD ======================
@login_required
def order_delete(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if request.method == 'POST':
        order.delete()
        messages.success(request, 'Order deleted successfully!')
        return redirect('order_list')
    return render(request, 'delete_confirmation.html', {
        'object': order,
        'cancel_url': reverse('order_detail', kwargs={'pk': pk})
    })

# ====================== ORDER ITEM CRUD ======================
@login_required
def order_item_delete(request, pk):
    order_item = get_object_or_404(OrderItem, pk=pk)
    order_pk = order_item.order.pk
    if request.method == 'POST':
        order_item.delete()
        
        # Update order totals
        order = order_item.order
        order.subtotal = sum(item.total for item in order.items.all())
        order.service_fee = order.subtotal * (order.event.service_fee_percentage / 100)
        order.total_amount = order.subtotal + order.service_fee - order.discount_amount
        order.save()
        
        messages.success(request, 'Order item deleted successfully!')
        return redirect('order_detail', pk=order_pk)
    return render(request, 'delete_confirmation.html', {
        'object': order_item,
        'cancel_url': reverse('order_detail', kwargs={'pk': order_pk})
    })

# ====================== ATTENDEE CRUD ======================
@login_required
def attendee_delete(request, pk):
    attendee = get_object_or_404(Attendee, pk=pk)
    order_pk = attendee.order.pk
    if request.method == 'POST':
        attendee.delete()
        messages.success(request, 'Attendee deleted successfully!')
        return redirect('order_detail', pk=order_pk)
    return render(request, 'delete_confirmation.html', {
        'object': attendee,
        'cancel_url': reverse('order_detail', kwargs={'pk': order_pk})
    })

# ====================== EVENT TICKET CRUD ======================
@login_required
def event_ticket_delete(request, pk):
    ticket = get_object_or_404(EventTicket, pk=pk)
    if request.method == 'POST':
        ticket.delete()
        messages.success(request, 'Ticket deleted successfully!')
        return redirect('event_ticket_list')
    return render(request, 'delete_confirmation.html', {
        'object': ticket,
        'cancel_url': reverse('event_ticket_detail', kwargs={'pk': pk})
    })

# ====================== PAYMENT CRUD ======================
@login_required
def payment_delete(request, pk):
    payment = get_object_or_404(Payment, pk=pk)
    order_pk = payment.order.pk
    if request.method == 'POST':
        payment.delete()
        
        # Update order status if payment was completed
        if payment.status == 'completed':
            order = payment.order
            order.status = 'pending'
            order.save()
        
        messages.success(request, 'Payment record deleted successfully!')
        return redirect('order_detail', pk=order_pk)
    return render(request, 'delete_confirmation.html', {
        'object': payment,
        'cancel_url': reverse('order_detail', kwargs={'pk': order_pk})
    })

# ====================== CHECK-IN CRUD ======================
@login_required
def check_in_delete(request, pk):
    check_in = get_object_or_404(CheckIn, pk=pk)
    ticket_pk = check_in.ticket.pk
    if request.method == 'POST':
        check_in.delete()
        
        # Reset ticket status if this was the only valid check-in
        ticket = check_in.ticket
        if not CheckIn.objects.filter(ticket=ticket, is_duplicate=False).exists():
            ticket.status = 'valid'
            ticket.save()
        
        messages.success(request, 'Check-in record deleted successfully!')
        return redirect('event_ticket_detail', pk=ticket_pk)
    return render(request, 'delete_confirmation.html', {
        'object': check_in,
        'cancel_url': reverse('event_ticket_detail', kwargs={'pk': ticket_pk})
    })

# ====================== DEVICE CRUD ======================
@login_required
def device_delete(request, pk):
    device = get_object_or_404(Device, pk=pk)
    if request.method == 'POST':
        device.delete()
        messages.success(request, 'Device deleted successfully!')
        return redirect('device_list')
    return render(request, 'delete_confirmation.html', {
        'object': device,
        'cancel_url': reverse('device_list')
    })

# ====================== PAYOUT CRUD ======================
@login_required
@permission_required('organisers.delete_payout', raise_exception=True)
def payout_delete(request, pk):
    payout = get_object_or_404(Payout, pk=pk)
    if request.method == 'POST':
        payout.delete()
        messages.success(request, 'Payout deleted successfully!')
        return redirect('payout_list')
    return render(request, 'delete_confirmation.html', {
        'object': payout,
        'cancel_url': reverse('payout_detail', kwargs={'pk': pk})
    })