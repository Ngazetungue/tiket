from django.contrib import admin
from django.contrib.admin import SimpleListFilter
from django.utils import timezone
from django.db.models import Sum
from django.contrib import messages
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
from .forms import (
    OrganizerForm,
    EventForm,
    PromoCodeForm,
    OrderForm,
    AttendeeForm,
    EventTicketForm,
    PaymentForm,
    PayoutForm
)

# ====================== FILTERS ======================
class ActiveEventFilter(SimpleListFilter):
    title = 'Active Events'
    parameter_name = 'is_active'

    def lookups(self, request, model_admin):
        return (
            ('active', 'Active'),
            ('inactive', 'Inactive'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'active':
            return queryset.filter(is_active=True)
        if self.value() == 'inactive':
            return queryset.filter(is_active=False)

class OnSaleFilter(SimpleListFilter):
    title = 'On Sale'
    parameter_name = 'on_sale'

    def lookups(self, request, model_admin):
        return (
            ('on_sale', 'Currently on sale'),
            ('not_on_sale', 'Not on sale'),
        )

    def queryset(self, request, queryset):
        now = timezone.now()
        if self.value() == 'on_sale':
            return queryset.filter(
                is_active=True,
                sales_start__lte=now,
                sales_end__gte=now,
                ticket_quantity_available__gt=0
            )
        if self.value() == 'not_on_sale':
            return queryset.exclude(
                is_active=True,
                sales_start__lte=now,
                sales_end__gte=now,
                ticket_quantity_available__gt=0
            )

# ====================== INLINES ======================
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1
    readonly_fields = ('price', 'total')
    fields = ('event', 'quantity', 'price', 'total')

class AttendeeInline(admin.TabularInline):
    model = Attendee
    extra = 1
    fields = ('first_name', 'last_name', 'email', 'phone', 'special_requirements')

class EventTicketInline(admin.TabularInline):
    model = EventTicket
    extra = 0
    readonly_fields = ('ticket_number', 'qr_code', 'status')
    fields = ('ticket_number', 'attendee', 'qr_code', 'status')

class CheckInInline(admin.TabularInline):
    model = CheckIn
    extra = 0
    readonly_fields = ('check_in_time', 'is_duplicate')
    fields = ('check_in_time', 'device', 'location', 'is_duplicate', 'notes')

# ====================== MODEL ADMINS ======================
@admin.register(Organizer)
class OrganizerAdmin(admin.ModelAdmin):
    form = OrganizerForm
    list_display = ('user', 'phone', 'verified', 'commission_rate')
    list_filter = ('verified',)
    search_fields = ('user__first_name', 'user__last_name', 'phone')
    readonly_fields = ('verified',)
    fieldsets = (
        ('User Information', {
            'fields': ('user', 'phone')
        }),
        ('Bank Details', {
            'fields': ('bank_name', 'account_number', 'branch_code')
        }),
        ('Verification', {
            'fields': ('verified', 'commission_rate')
        }),
    )

@admin.register(Purchaser)
class PurchaserAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'phone', 'created_at')
    search_fields = ('first_name', 'last_name', 'email', 'phone')
    list_filter = ('created_at',)
    readonly_fields = ('created_at',)
    fieldsets = (
        ('Personal Information', {
            'fields': ('user', 'first_name', 'last_name', 'email', 'phone')
        }),
        ('Metadata', {
            'fields': ('created_at',)
        }),
    )

admin.site.register(Event)

@admin.register(PromoCode)
class PromoCodeAdmin(admin.ModelAdmin):
    form = PromoCodeForm
    list_display = (
        'code',
        'discount_type',
        'discount_value',
        'valid_from',
        'valid_to',
        'is_active',
        'times_used',
        'max_uses'
    )
    list_filter = ('discount_type', 'is_active', 'event')
    search_fields = ('code', 'event__title')
    readonly_fields = ('times_used',)
    fieldsets = (
        ('Code Information', {
            'fields': ('code', 'is_active', 'event')
        }),
        ('Discount Details', {
            'fields': ('discount_type', 'discount_value', 'min_order_amount')
        }),
        ('Usage Limits', {
            'fields': ('max_uses', 'times_used')
        }),
        ('Validity Period', {
            'fields': ('valid_from', 'valid_to')
        }),
    )

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    form = OrderForm
    inlines = [OrderItemInline, AttendeeInline]
    list_display = (
        'order_number',
        'purchaser',
        'event',
        'status',
        'total_amount',
        'created_at',
        'is_paid'
    )
    list_filter = ('status', 'created_at', 'payment_method')
    search_fields = (
        'order_number',
        'purchaser__first_name',
        'purchaser__last_name',
        'event__title'
    )
    readonly_fields = (
        'order_number',
        'created_at',
        'updated_at',
        'subtotal',
        'service_fee',
        'total_amount'
    )
    fieldsets = (
        ('Order Information', {
            'fields': (
                'order_number',
                'purchaser',
                'event',
                'status',
                'promo_code',
                'discount_amount'
            )
        }),
        ('Payment Details', {
            'fields': (
                'payment_method',
                'payment_reference',
                'subtotal',
                'service_fee',
                'total_amount'
            )
        }),
        ('Dates', {
            'fields': (
                'created_at',
                'updated_at'
            )
        }),
    )

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'event', 'quantity', 'price', 'total')
    list_filter = ('event',)
    search_fields = ('order__order_number', 'event__title')
    readonly_fields = ('price', 'total')
    fieldsets = (
        ('Item Information', {
            'fields': ('order', 'event', 'quantity')
        }),
        ('Pricing', {
            'fields': ('price', 'total')
        }),
    )

@admin.register(Attendee)
class AttendeeAdmin(admin.ModelAdmin):
    form = AttendeeForm
    list_display = ('full_name', 'email', 'phone', 'order')
    search_fields = ('first_name', 'last_name', 'email', 'phone')
    list_filter = ('order__event',)
    fieldsets = (
        ('Attendee Information', {
            'fields': (
                'order',
                'first_name',
                'last_name',
                'email',
                'phone',
                'special_requirements'
            )
        }),
    )

@admin.register(EventTicket)
class EventTicketAdmin(admin.ModelAdmin):
    form = EventTicketForm
    inlines = [CheckInInline]
    list_display = (
        'ticket_number',
        'attendee',
        'order_item',
        'status',
        'created_at'
    )
    list_filter = ('status', 'order_item__event')
    search_fields = (
        'ticket_number',
        'attendee__first_name',
        'attendee__last_name',
        'qr_code'
    )
    readonly_fields = ('ticket_number', 'qr_code', 'created_at')
    fieldsets = (
        ('Ticket Information', {
            'fields': (
                'order_item',
                'attendee',
                'status'
            )
        }),
        ('System Information', {
            'fields': (
                'ticket_number',
                'qr_code',
                'created_at'
            )
        }),
    )

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    form = PaymentForm
    list_display = (
        'order',
        'amount',
        'method',
        'status',
        'created_at'
    )
    list_filter = ('status', 'method', 'created_at')
    search_fields = ('order__order_number', 'transaction_id')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Payment Information', {
            'fields': (
                'order',
                'amount',
                'method',
                'status',
                'transaction_id'
            )
        }),
        ('Additional Details', {
            'fields': ('payment_details',)
        }),
        ('Dates', {
            'fields': (
                'created_at',
                'updated_at'
            )
        }),
    )

@admin.register(CheckIn)
class CheckInAdmin(admin.ModelAdmin):
    list_display = (
        'ticket',
        'check_in_time',
        'is_duplicate',
        'device'
    )
    list_filter = ('is_duplicate', 'device')
    search_fields = (
        'ticket__ticket_number',
        'ticket__attendee__first_name',
        'ticket__attendee__last_name'
    )
    readonly_fields = ('check_in_time', 'is_duplicate')
    fieldsets = (
        ('Check-in Information', {
            'fields': (
                'ticket',
                'device',
                'location',
                'is_duplicate',
                'notes'
            )
        }),
        ('Timestamp', {
            'fields': ('check_in_time',)
        }),
    )

@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ('name', 'device_id', 'last_active', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name', 'device_id')
    readonly_fields = ('last_active',)
    fieldsets = (
        ('Device Information', {
            'fields': (
                'name',
                'device_id',
                'is_active'
            )
        }),
        ('Last Activity', {
            'fields': ('last_active',)
        }),
    )

@admin.register(Payout)
class PayoutAdmin(admin.ModelAdmin):
    form = PayoutForm
    list_display = (
        'reference',
        'organizer',
        'event',
        'amount',
        'status',
        'initiated_at'
    )
    list_filter = ('status', 'organizer')
    search_fields = ('reference', 'organizer__user__username')
    readonly_fields = ('initiated_at', 'completed_at')
    fieldsets = (
        ('Payout Information', {
            'fields': (
                'organizer',
                'event',
                'amount',
                'status',
                'reference'
            )
        }),
        ('Dates', {
            'fields': (
                'initiated_at',
                'completed_at'
            )
        }),
    )