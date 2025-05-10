# from django.contrib import admin
# from django.contrib.admin import SimpleListFilter
# from django.utils.html import format_html
# from .models import (
#     Organizer, Purchaser, Event, TicketType, PromoCode,
#     Order, OrderItem, Attendee, Ticket, Payment,
#     CheckIn, Device, Payout
# )

# # Custom Filters
# class ActiveEventFilter(SimpleListFilter):
#     title = 'active status'
#     parameter_name = 'is_active'

#     def lookups(self, request, model_admin):
#         return (
#             ('active', 'Active Events'),
#             ('inactive', 'Inactive Events'),
#         )

#     def queryset(self, request, queryset):
#         if self.value() == 'active':
#             return queryset.filter(is_active=True)
#         if self.value() == 'inactive':
#             return queryset.filter(is_active=False)

# class TicketAvailabilityFilter(SimpleListFilter):
#     title = 'availability'
#     parameter_name = 'available'

#     def lookups(self, request, model_admin):
#         return (
#             ('available', 'Available Tickets'),
#             ('soldout', 'Sold Out'),
#         )

#     def queryset(self, request, queryset):
#         if self.value() == 'available':
#             return queryset.filter(quantity_available__gt=0)
#         if self.value() == 'soldout':
#             return queryset.filter(quantity_available=0)

# # Inline Admin Classes
# class OrderItemInline(admin.TabularInline):
#     model = OrderItem
#     extra = 0
#     readonly_fields = ('price', 'total')
#     fields = ('ticket_type', 'quantity', 'price', 'total')
#     can_delete = False

# class AttendeeInline(admin.TabularInline):
#     model = Attendee
#     extra = 0
#     fields = ('first_name', 'last_name', 'email', 'phone')
#     can_delete = False

# class TicketInline(admin.TabularInline):
#     model = Ticket
#     extra = 0
#     readonly_fields = ('ticket_number', 'qr_code', 'status')
#     fields = ('ticket_number', 'attendee', 'status', 'qr_code')
#     can_delete = False

# class CheckInInline(admin.TabularInline):
#     model = CheckIn
#     extra = 0
#     readonly_fields = ('check_in_time', 'is_duplicate')
#     fields = ('check_in_time', 'device', 'location', 'is_duplicate')
#     can_delete = False

# class PaymentInline(admin.StackedInline):
#     model = Payment
#     extra = 0
#     readonly_fields = ('created_at', 'updated_at')
#     fields = ('method', 'status', 'amount', 'transaction_id', 'created_at')

# # Model Admin Classes
# @admin.register(Organizer)
# class OrganizerAdmin(admin.ModelAdmin):
#     list_display = ('user', 'phone', 'bank_name', 'verified')
#     list_filter = ('verified',)
#     search_fields = ('user__username', 'user__email', 'phone')
#     raw_id_fields = ('user',)

# @admin.register(Purchaser)
# class PurchaserAdmin(admin.ModelAdmin):
#     list_display = ('full_name', 'email', 'phone', 'created_at')
#     search_fields = ('first_name', 'last_name', 'email', 'phone')
#     list_filter = ('created_at',)
#     readonly_fields = ('created_at',)

# @admin.register(Event)
# class EventAdmin(admin.ModelAdmin):
#     list_display = ('title', 'organizer', 'start_date', 'end_date', 'location', 'is_active', 'is_on_sale')
#     list_filter = (ActiveEventFilter, 'organizer', 'start_date')
#     search_fields = ('title', 'description', 'location')
#     readonly_fields = ('created_at', 'updated_at', 'is_on_sale')
#     fieldsets = (
#         (None, {
#             'fields': ('organizer', 'title', 'description', 'is_active')
#         }),
#         ('Event Details', {
#             'fields': ('location', 'venue', 'start_date', 'end_date', 'image', 'service_fee_percentage')
#         }),
#         ('Metadata', {
#             'fields': ('created_at', 'updated_at', 'is_on_sale'),
#             'classes': ('collapse',)
#         }),
#     )

# @admin.register(TicketType)
# class TicketTypeAdmin(admin.ModelAdmin):
#     list_display = ('name', 'event', 'price', 'quantity_available', 'is_available', 'sales_end')
#     list_filter = (TicketAvailabilityFilter, 'event', 'is_active')
#     search_fields = ('name', 'event__title')
#     readonly_fields = ('quantity_sold', 'quantity_available', 'is_available')
#     fieldsets = (
#         (None, {
#             'fields': ('event', 'name', 'description', 'is_active')
#         }),
#         ('Pricing & Inventory', {
#             'fields': ('price', 'quantity', 'quantity_sold', 'quantity_available')
#         }),
#         ('Sales Period', {
#             'fields': ('sales_start', 'sales_end', 'is_available')
#         }),
#         ('Order Limits', {
#             'fields': ('min_per_order', 'max_per_order'),
#             'classes': ('collapse',)
#         }),
#     )

# @admin.register(PromoCode)
# class PromoCodeAdmin(admin.ModelAdmin):
#     list_display = ('code', 'discount_type', 'discount_value', 'is_active', 'valid_from', 'valid_to', 'times_used')
#     list_filter = ('discount_type', 'is_active')
#     search_fields = ('code',)
#     filter_horizontal = ('ticket_types',)
#     readonly_fields = ('times_used',)

# @admin.register(Order)
# class OrderAdmin(admin.ModelAdmin):
#     list_display = ('order_number', 'purchaser', 'event', 'total_amount', 'status', 'created_at')
#     list_filter = ('status', 'event', 'created_at', 'payment_method')
#     search_fields = ('order_number', 'purchaser__email', 'purchaser__phone')
#     readonly_fields = ('order_number', 'created_at', 'updated_at', 'subtotal', 'service_fee', 'total_amount')
#     inlines = [OrderItemInline, AttendeeInline, PaymentInline]
#     fieldsets = (
#         (None, {
#             'fields': ('order_number', 'purchaser', 'event', 'status')
#         }),
#         ('Payment', {
#             'fields': ('payment_method', 'payment_reference', 'promo_code', 'discount_amount')
#         }),
#         ('Amounts', {
#             'fields': ('subtotal', 'service_fee', 'total_amount')
#         }),
#         ('Metadata', {
#             'fields': ('created_at', 'updated_at'),
#             'classes': ('collapse',)
#         }),
#     )

# @admin.register(Ticket)
# class TicketAdmin(admin.ModelAdmin):
#     list_display = ('ticket_number', 'attendee', 'order_item', 'status', 'created_at')
#     list_filter = ('status', 'order_item__order__event')
#     search_fields = ('ticket_number', 'attendee__first_name', 'attendee__last_name', 'qr_code')
#     readonly_fields = ('ticket_number', 'qr_code', 'created_at')
#     inlines = [CheckInInline]

#     def qr_code_display(self, obj):
#         return format_html('<a href="{}" target="_blank">View QR</a>', obj.qr_code_url)
#     qr_code_display.short_description = 'QR Code'

# @admin.register(Payment)
# class PaymentAdmin(admin.ModelAdmin):
#     list_display = ('order', 'method', 'amount', 'status', 'created_at')
#     list_filter = ('status', 'method', 'created_at')
#     search_fields = ('order__order_number', 'transaction_id')
#     readonly_fields = ('created_at', 'updated_at')

# @admin.register(CheckIn)
# class CheckInAdmin(admin.ModelAdmin):
#     list_display = ('ticket', 'check_in_time', 'is_duplicate', 'location')
#     list_filter = ('is_duplicate', 'device', 'check_in_time')
#     search_fields = ('ticket__ticket_number', 'ticket__attendee__first_name')

# @admin.register(Device)
# class DeviceAdmin(admin.ModelAdmin):
#     list_display = ('name', 'device_id', 'last_active', 'is_active')
#     list_filter = ('is_active',)
#     search_fields = ('name', 'device_id')

# @admin.register(Payout)
# class PayoutAdmin(admin.ModelAdmin):
#     list_display = ('organizer', 'event', 'amount', 'status', 'initiated_at')
#     list_filter = ('status', 'organizer', 'initiated_at')
#     search_fields = ('reference', 'organizer__user__username')
#     readonly_fields = ('initiated_at', 'completed_at')