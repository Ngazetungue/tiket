from django.shortcuts import render, redirect, get_object_or_404
from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from organisers.models import Event

from django.shortcuts import render, get_object_or_404
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY

def home(request):
    events = Event.objects.all()[:3]
    return render(request, 'home/home.html', {'events':events})

def about(request):
    return render(request, 'home/about.html')

def buy_ticket(request):
    return render(request, 'home/checkout-page.html')

def events(request):
    events = Event.objects.all()
    category = request.GET.get('category')
    
    if category and category != 'all':
        events = events.filter(category=category)
    
    return render(request, 'home/events.html', {
        'events': events,
        'selected_category': category or 'all'
    })

def event_detail(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    return render(request, 'home/checkout-page.html', {
        'event': event,
        'STRIPE_PUBLIC_KEY': settings.STRIPE_PUBLIC_KEY
    })

def create_checkout_session(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    
    try:
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': event.title,
                        'description': event.description,
                        'images': [
                            "https://images.unsplash.com/photo-1501281668745-f7f57925c3b4?ixlib=rb-1.2.1&auto=format&fit=crop&w=600&q=80"
                        ],
                        'metadata': {
                            'event_id': str(event.id),
                            'venue': event.venue,
                        }
                    },
                    'unit_amount': int(event.ticket_price * 100),
                },
                'quantity': 1,
            }],
            mode='payment',
            customer_creation='always', 
            success_url=request.build_absolute_uri('/success/') + '?session_id={CHECKOUT_SESSION_ID}',
            cancel_url=request.build_absolute_uri('/cancel/'),
        )
        return JsonResponse({'id': checkout_session.id})
    except Exception as e:
        return JsonResponse({'error': str(e)})


def success(request):
    session_id = request.GET.get('session_id')
    
    if session_id:
        try:
            session = stripe.checkout.Session.retrieve(session_id)
        
            if session.customer_details is None:
                customer_name = "Test Customer (Dashboard)"
                customer_email = "test@example.com"
            else:
                customer_name = session.customer_details.name
                customer_email = session.customer_details.email
        
            event_id = session.metadata.get('event_id')
            if event_id:
                event = get_object_or_404(Event, id=event_id)
            else:
                event = {
                    'title': 'Windhoek Jazz Festival (Test)',
                    'venue': 'National Theatre (Test)',
                    'start_date': "May 15, 2024",
                    'start_time': "18:00",
                    'description': "Test event description.",
                    'image': {'url': 'https://via.placeholder.com/600x400'}
                }
            
            context = {
                'event': event,
                'customer_name': customer_name,
                'customer_email': customer_email,
                'ticket_reference': f"TEST-{session.id[:8].upper()}",
                'ticket_type': "General Admission",
            }
            return render(request, 'home/success.html', context)
            
        except Exception as e:
            logger.error(f"Error: {str(e)}")
            return render(request, 'home/success.html')
    
    return render(request, 'home/success.html')

def cancel(request):
    return render(request, 'home/cancel.html')

@csrf_exempt
def stripe_webhook(request):
    pass

def payout(request):
    return render(request, 'home/payout.html')

def community(request):
    return render(request, 'home/community.html')

def terms(request):
    return render(request, 'home/terms-conditions.html')

def help_center(request):
    return render(request, 'home/help-center.html')

def privacy(request):
    return render(request, 'home/privacy-policy.html')

def careers(request):
    return render(request, 'home/careers.html')

def contact(request):
    return render(request, 'home/contact-us.html')