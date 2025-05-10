from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator
from django.utils import timezone
from django.utils.text import get_valid_filename
import uuid
from django.contrib.auth import get_user_model

from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError


# List of towns in Namibia
TOWN_CHOICES = [
    ('Windhoek', 'Windhoek'),
    ('Swakopmund', 'Swakopmund'),
    ('Oshakati', 'Oshakati'),
    ('Walvis Bay', 'Walvis Bay'),
    ('Luderitz', 'Luderitz'),
    ('Rehoboth', 'Rehoboth'),
    ('Rundu', 'Rundu'),
    ('Tsumeb', 'Tsumeb'),
    ('Katima Mulilo', 'Katima Mulilo'),
    ('Otjiwarongo', 'Otjiwarongo'),
    ('Gobabis', 'Gobabis'),
    ('Keetmanshoop', 'Keetmanshoop'),
    ('Mariental', 'Mariental'),
    ('Outapi', 'Outapi'),
    ('Grootfontein', 'Grootfontein'),
    ('Henties Bay', 'Henties Bay'),
    ('Okahandja', 'Okahandja'),
    ('Ongwediva', 'Ongwediva'),
    ('Bintheb', 'Bintheb'),
    ('Usakos', 'Usakos'),
    ('Aroab', 'Aroab'),
    ('Sossusvlei', 'Sossusvlei'),
    ('Linyanti', 'Linyanti'),
    ('Uis', 'Uis'),
    ('Pioneers Park', 'Pioneers Park'),
    ('Maltahohe', 'Maltahohe'),
    ('Aminuis', 'Aminuis'),
    ('Ndiyona', 'Ndiyona'),
    ('Oshikuku', 'Oshikuku'),
    ('Kamanjab', 'Kamanjab'),
    ('Eiseb', 'Eiseb'),
    ('Witvlei', 'Witvlei'),
    ('Ruacana', 'Ruacana'),
    ('Omatako', 'Omatako'),
    ('Sesfontein', 'Sesfontein'),
    ('Mokuru', 'Mokuru'),
    ('Opuwo', 'Opuwo'), 
]

CATEGORIES = [
    ('Sports', 'Sports'),
    ('Music', 'Music'),
    ('Conference', 'Conference'),
    ('Festival', 'Festival'),
    ('Exhibition', 'Exhibition'),
    ('Workshop', 'Workshop'),
    ('Seminar', 'Seminar'),
    ('Networking', 'Networking'),
    ('Theater', 'Theater'),
    ('Art', 'Art'),
    ('Charity', 'Charity'),
    ('Concert', 'Concert'),
    ('Fundraiser', 'Fundraiser'),
    ('Comedy', 'Comedy'),
    ('Dance', 'Dance'),
    ('Food & Drink', 'Food & Drink'),
    ('Family', 'Family'),
    ('Business', 'Business'),
    ('Technology', 'Technology'),
    ('Education', 'Education'),
    ('Health & Wellness', 'Health & Wellness'),
]

def event_image_path(instance, filename):
    """Generate path for event images"""
    return f'events/{instance.organizer.user.id}/{get_valid_filename(filename)}'

class Organizer(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    phone = models.CharField(max_length=15)
    bank_name = models.CharField(max_length=50)
    account_number = models.CharField(max_length=20)
    branch_code = models.CharField(max_length=10)
    verified = models.BooleanField(default=False)
    commission_rate = models.DecimalField(max_digits=5, decimal_places=2, default=10.0)  # Default 10% commission

    def __str__(self):
        return f"{self.user.get_full_name()}"

class Purchaser(models.Model):
    """Person who purchases tickets (could be buying for others)"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['phone']),
        ]
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    def __str__(self):
        return self.full_name


class Event(models.Model):

    organizer = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        limit_choices_to={'user_type': 'organiser'},
        related_name='events_organized'
    )
    title = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=200, choices=TOWN_CHOICES)
    venue = models.CharField(max_length=200, blank=True)
    category = models.CharField(max_length=50, choices=CATEGORIES)
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField(default=timezone.now)
    image = models.ImageField(upload_to='event_images/', blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    service_fee_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=5.0)

    capacity = models.PositiveIntegerField(
        default=100,  # Set your default capacity
        help_text="Maximum number of tickets available for this event"
    )
    tickets_sold = models.PositiveIntegerField(
        default=0,
        help_text="Number of tickets sold so far"
    )
    revenue = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00,
        help_text="Total revenue generated from ticket sales"
    )
    #

    # Ticket-related fields
    ticket_name = models.CharField(max_length=100, default='General Admission')
    ticket_description = models.TextField(blank=True)
    ticket_price = models.DecimalField(max_digits=10, decimal_places=2)
    ticket_quantity = models.PositiveIntegerField(
        validators=[MinValueValidator(1)],
        default=0 
    )
    ticket_quantity_sold = models.PositiveIntegerField(
        default=0  
    )
    sales_start = models.DateTimeField(default=timezone.now)
    sales_end = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-start_date']
        indexes = [
            models.Index(fields=['start_date']),
            models.Index(fields=['location']),
            models.Index(fields=['category']),
        ]
        verbose_name = "Event"
        verbose_name_plural = "Events"

    def __str__(self):
        return f"{self.title} ({self.start_date.strftime('%b %d, %Y')})"

    def clean(self):
        if self.start_date >= self.end_date:
            raise ValidationError("End date must be after start date.")
        if self.sales_start >= self.sales_end:
            raise ValidationError("Sales end date must be after sales start date.")
        if self.sales_end > self.start_date:
            raise ValidationError("Ticket sales must end before the event starts.")


    @property
    def ticket_quantity_available(self):
        """Calculate available tickets, handling None values"""
        if self.ticket_quantity is None or self.ticket_quantity_sold is None:
            return 0
        return max(0, self.ticket_quantity - self.ticket_quantity_sold)

    @property
    def is_ticket_on_sale(self):
        """Check if tickets are currently on sale"""
        now = timezone.now()
        if not self.is_active:
            return False
        if self.sales_start is None or self.sales_end is None:
            return False
        if self.ticket_quantity_available is None or self.ticket_quantity_available <= 0:
            return False
        return self.sales_start <= now <= self.sales_end

    @property
    def is_sold_out(self):
        """Check if event is sold out"""
        if self.ticket_quantity_available is None:
            return True
        return self.ticket_quantity_available <= 0

class PromoCode(models.Model):
    DISCOUNT_TYPES = (
        ('percentage', 'Percentage'),
        ('fixed', 'Fixed Amount'),
    )
    
    code = models.CharField(max_length=20, unique=True)
    discount_type = models.CharField(max_length=10, choices=DISCOUNT_TYPES)
    discount_value = models.DecimalField(max_digits=10, decimal_places=2)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    max_uses = models.PositiveIntegerField()
    times_used = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, blank=True, null=True)
    min_order_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    def __str__(self):
        return self.code
    
    def is_valid(self, order_amount=None):
        now = timezone.now()
        if not self.is_active:
            return False
        if now < self.valid_from or now > self.valid_to:
            return False
        if self.times_used >= self.max_uses:
            return False
        if order_amount and self.min_order_amount and order_amount < self.min_order_amount:
            return False
        return True

class Order(models.Model):
    PAYMENT_METHODS = (
        ('mtc', 'MTC Money'),
        ('telecom', 'Telecom Pay'),
        ('card', 'Credit/Debit Card'),
        ('bank', 'Bank Transfer'),
    )
    
    STATUS_CHOICES = (
        ('pending', 'Pending Payment'),
        ('paid', 'Paid'),
        ('cancelled', 'Cancelled'),
        ('refunded', 'Refunded'),
    )
    
    purchaser = models.ForeignKey(Purchaser, on_delete=models.CASCADE, related_name='orders')
    event = models.ForeignKey(Event, on_delete=models.PROTECT)
    order_number = models.CharField(max_length=20, unique=True, editable=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    service_fee = models.DecimalField(max_digits=10, decimal_places=2)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=50, choices=PAYMENT_METHODS, blank=True)
    payment_reference = models.CharField(max_length=100, blank=True)
    promo_code = models.ForeignKey(PromoCode, on_delete=models.SET_NULL, null=True, blank=True)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['order_number']),
            models.Index(fields=['status']),
        ]
    
    def __str__(self):
        return f"Order #{self.order_number}"
    
    def save(self, *args, **kwargs):
        if not self.order_number:
            # Generate order number: NAMTIX-XXXXXX
            self.order_number = f"NAMTIX-{uuid.uuid4().hex[:6].upper()}"
        super().save(*args, **kwargs)
    
    @property
    def is_paid(self):
        return self.status == 'paid'

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    event = models.ForeignKey(Event, on_delete=models.PROTECT) 
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    price = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return f"{self.quantity}x tickets for {self.event.title} in Order #{self.order.order_number}"

class Attendee(models.Model):
    """Actual person attending the event (may differ from purchaser)"""
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='attendees')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    special_requirements = models.TextField(blank=True)
    
    class Meta:
        ordering = ['last_name', 'first_name']
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    def __str__(self):
        return self.full_name

class EventTicket(models.Model):
    TICKET_STATUS_CHOICES = [
        ('valid', 'Valid'),
        ('used', 'Used'),
        ('cancelled', 'Cancelled'),
    ]
    
    order_item = models.ForeignKey(OrderItem, on_delete=models.CASCADE, related_name='tickets')
    attendee = models.ForeignKey(Attendee, on_delete=models.CASCADE, related_name='tickets')
    ticket_number = models.CharField(max_length=20, unique=True)
    qr_code = models.CharField(max_length=100, unique=True)
    status = models.CharField(max_length=10, choices=TICKET_STATUS_CHOICES, default='valid')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['ticket_number']),
            models.Index(fields=['qr_code']),
            models.Index(fields=['status']),
        ]
    
    def __str__(self):
        return f"{self.ticket_number} for {self.attendee.full_name}"
    
    def save(self, *args, **kwargs):
        if not self.ticket_number:
            # Generate ticket number: T-XXXXXX
            self.ticket_number = f"T-{uuid.uuid4().hex[:6].upper()}"
        if not self.qr_code:
            # Generate QR code data
            self.qr_code = f"NAMTIX-{self.ticket_number}-{uuid.uuid4().hex[:8]}"
        super().save(*args, **kwargs)

class Payment(models.Model):
    PAYMENT_STATUS = (
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    )
    
    order = models.OneToOneField(Order, on_delete=models.PROTECT, related_name='payment')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    method = models.CharField(max_length=20, choices=Order.PAYMENT_METHODS)
    status = models.CharField(max_length=20, choices=PAYMENT_STATUS, default='pending')
    transaction_id = models.CharField(max_length=100, blank=True)
    payment_details = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.get_method_display()} Payment for Order #{self.order.order_number}"

class CheckIn(models.Model):
    ticket = models.ForeignKey(EventTicket, on_delete=models.CASCADE, related_name='check_ins')
    check_in_time = models.DateTimeField(default=timezone.now)
    device = models.ForeignKey('Device', on_delete=models.SET_NULL, null=True, blank=True)
    location = models.CharField(max_length=100, blank=True)
    is_duplicate = models.BooleanField(default=False)
    notes = models.TextField(blank=True)
    
    class Meta:
        ordering = ['-check_in_time']
        unique_together = [['ticket', 'is_duplicate']]
    
    def save(self, *args, **kwargs):
        # Detect duplicates
        if not self.is_duplicate and CheckIn.objects.filter(ticket=self.ticket, is_duplicate=False).exists():
            self.is_duplicate = True
        
        # Update ticket status if valid check-in
        if not self.is_duplicate and self.ticket.status == 'valid':
            self.ticket.status = 'used'
            self.ticket.save()
        
        super().save(*args, **kwargs)
    
    def __str__(self):
        status = "DUPLICATE" if self.is_duplicate else "CHECKED IN"
        return f"{self.ticket} {status} at {self.check_in_time.strftime('%Y-%m-%d %H:%M')}"

class Device(models.Model):
    name = models.CharField(max_length=100)
    device_id = models.CharField(max_length=100, unique=True)
    last_active = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.name} ({self.device_id})"

class Payout(models.Model):
    organizer = models.ForeignKey(Organizer, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.SET_NULL, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('paid', 'Paid'),
        ('failed', 'Failed')
    ], default='pending')
    reference = models.CharField(max_length=100)
    initiated_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-initiated_at']
    
    def __str__(self):
        return f"Payout #{self.reference} - {self.amount} NAD"