from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from .models import (
    Organizer,
    Purchaser,
    Event,
    PromoCode,
    Order,
    OrderItem,
    Attendee,
    EventTicket,
    Payment,
    CheckIn,
    Device,
    Payout
)
from django.core.validators import MinValueValidator

class OrganizerForm(forms.ModelForm):
    class Meta:
        model = Organizer
        fields = '__all__'
        widgets = {
            'user': forms.Select(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. +264811234567'
            }),
            'bank_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Bank name'
            }),
            'account_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Account number'
            }),
            'branch_code': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Branch code'
            }),
            'commission_rate': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'max': '100',
                'step': '0.01'
            }),
        }

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if not phone.startswith('+264'):
            raise ValidationError("Namibian phone numbers must start with +264")
        return phone

class PurchaserForm(forms.ModelForm):
    class Meta:
        model = Purchaser
        fields = '__all__'
        widgets = {
            'user': forms.Select(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'First name'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Last name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Email address'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Phone number'
            }),
        }

from django import forms
from django.core.exceptions import ValidationError
from .models import Event

class EventForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add Tailwind classes to all fields
        for field_name, field in self.fields.items():
            base_classes = 'block w-full rounded-md border-gray-300 shadow-sm focus:border-red-500 focus:ring-red-500 sm:text-sm'
            
            if field_name in ['description', 'ticket_description']:
                field.widget.attrs.update({
                    'class': f'{base_classes} py-2 px-3 border min-h-[100px]'
                })
            elif field_name in ['start_date', 'end_date', 'sales_start', 'sales_end']:
                field.widget.attrs.update({
                    'class': f'{base_classes} py-2 px-3 border datetime-picker'
                })
            elif field_name == 'image':
                field.widget.attrs.update({
                    'class': 'sr-only'  # Hide default file input (use custom UI)
                })
            else:
                field.widget.attrs.update({
                    'class': f'{base_classes} py-2 px-3 border'
                })

    class Meta:
        model = Event
        fields = [
            'title', 'description', 'location', 'venue', 'category',
            'start_date', 'end_date', 'image',
            'ticket_name', 'ticket_description', 'ticket_price',
            'ticket_quantity', 'sales_start', 'sales_end'
        ]
        widgets = {
            'start_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'sales_start': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'sales_end': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'description': forms.Textarea(attrs={'rows': 3}),
            'ticket_description': forms.Textarea(attrs={'rows': 2}),
        }

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        sales_start = cleaned_data.get('sales_start')
        sales_end = cleaned_data.get('sales_end')

        if start_date and end_date and start_date >= end_date:
            raise ValidationError("End date must be after start date.")

        if sales_start and sales_end and sales_start >= sales_end:
            raise ValidationError("Ticket sales end must be after sales start.")

        if sales_end and start_date and sales_end > start_date:
            raise ValidationError("Ticket sales must end before the event starts.")

        return cleaned_data

class PromoCodeForm(forms.ModelForm):
    class Meta:
        model = PromoCode
        fields = '__all__'
        widgets = {
            'code': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Promo code'
            }),
            'discount_type': forms.Select(attrs={'class': 'form-control'}),
            'discount_value': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'step': '0.01'
            }),
            'valid_from': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            }),
            'valid_to': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            }),
            'max_uses': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1'
            }),
            'min_order_amount': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'step': '0.01'
            }),
            'event': forms.Select(attrs={'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        valid_from = cleaned_data.get('valid_from')
        valid_to = cleaned_data.get('valid_to')
        
        if valid_from and valid_to and valid_from >= valid_to:
            raise ValidationError("Valid to must be after valid from date.")

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = '__all__'
        widgets = {
            'purchaser': forms.Select(attrs={'class': 'form-control'}),
            'event': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'payment_method': forms.Select(attrs={'class': 'form-control'}),
            'payment_reference': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Payment reference'
            }),
            'promo_code': forms.Select(attrs={'class': 'form-control'}),
            'subtotal': forms.NumberInput(attrs={
                'class': 'form-control',
                'readonly': 'readonly'
            }),
            'service_fee': forms.NumberInput(attrs={
                'class': 'form-control',
                'readonly': 'readonly'
            }),
            'total_amount': forms.NumberInput(attrs={
                'class': 'form-control',
                'readonly': 'readonly'
            }),
            'discount_amount': forms.NumberInput(attrs={
                'class': 'form-control',
                'readonly': 'readonly'
            }),
        }

class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = '__all__'
        widgets = {
            'order': forms.Select(attrs={'class': 'form-control'}),
            'event': forms.Select(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1'
            }),
            'price': forms.NumberInput(attrs={
                'class': 'form-control',
                'readonly': 'readonly'
            }),
            'total': forms.NumberInput(attrs={
                'class': 'form-control',
                'readonly': 'readonly'
            }),
        }

class AttendeeForm(forms.ModelForm):
    class Meta:
        model = Attendee
        fields = '__all__'
        widgets = {
            'order': forms.Select(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'First name'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Last name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Email address'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Phone number'
            }),
            'special_requirements': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Any special requirements'
            }),
        }

class EventTicketForm(forms.ModelForm):
    class Meta:
        model = EventTicket
        fields = '__all__'
        widgets = {
            'order_item': forms.Select(attrs={'class': 'form-control'}),
            'attendee': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'ticket_number': forms.TextInput(attrs={
                'class': 'form-control',
                'readonly': 'readonly'
            }),
            'qr_code': forms.TextInput(attrs={
                'class': 'form-control',
                'readonly': 'readonly'
            }),
        }

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = '__all__'
        widgets = {
            'order': forms.Select(attrs={'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'step': '0.01'
            }),
            'method': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'transaction_id': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Transaction ID'
            }),
        }

class CheckInForm(forms.ModelForm):
    class Meta:
        model = CheckIn
        fields = '__all__'
        widgets = {
            'ticket': forms.Select(attrs={'class': 'form-control'}),
            'device': forms.Select(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Check-in location'
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Any notes'
            }),
        }

class DeviceForm(forms.ModelForm):
    class Meta:
        model = Device
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Device name'
            }),
            'device_id': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Unique device ID'
            }),
        }

class PayoutForm(forms.ModelForm):
    class Meta:
        model = Payout
        fields = '__all__'
        widgets = {
            'organizer': forms.Select(attrs={'class': 'form-control'}),
            'event': forms.Select(attrs={'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'step': '0.01'
            }),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'reference': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Payout reference'
            }),
        }