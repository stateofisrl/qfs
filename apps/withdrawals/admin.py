"""
Withdrawals admin configuration.
"""

from django.contrib import admin
from django.utils import timezone
from .models import Withdrawal


@admin.register(Withdrawal)
class WithdrawalAdmin(admin.ModelAdmin):
    list_display = ['user', 'amount', 'get_cryptocurrency_display', 'status', 'created_at']
    list_filter = ['status', 'cryptocurrency', 'created_at']
    search_fields = ['user__email', 'cryptocurrency', 'wallet_address']
    actions = ['mark_as_processing', 'mark_as_completed', 'mark_as_rejected']
    ordering = ['-created_at']
    
    def get_cryptocurrency_display(self, obj):
        """Display cryptocurrency with full name."""
        return f"{obj.get_cryptocurrency_display()} ({obj.cryptocurrency})"
    get_cryptocurrency_display.short_description = 'Cryptocurrency'
    get_cryptocurrency_display.admin_order_field = 'cryptocurrency'
    
    def get_readonly_fields(self, request, obj=None):
        """Make fields readonly only when editing existing withdrawal."""
        if obj:  # Editing an existing object
            return ['user', 'amount', 'cryptocurrency', 'wallet_address', 'created_at']
        return []  # Adding new object - allow editing all fields
    
    def get_fieldsets(self, request, obj=None):
        """Return different fieldsets for add vs change forms."""
        if obj:  # Editing existing withdrawal
            return (
                ('Withdrawal Request', {
                    'fields': ('user', 'amount', 'cryptocurrency', 'wallet_address', 'created_at')
                }),
                ('Processing', {
                    'fields': ('status', 'transaction_hash', 'processed_by', 'processed_at')
                }),
                ('Admin Notes', {
                    'fields': ('admin_notes',)
                }),
            )
        else:  # Adding new withdrawal
            return (
                ('Withdrawal Request', {
                    'fields': ('user', 'amount', 'cryptocurrency', 'wallet_address')
                }),
                ('Processing', {
                    'fields': ('status', 'transaction_hash', 'admin_notes')
                }),
            )
    
    def save_model(self, request, obj, form, change):
        """Override save to handle balance refund on rejection."""
        if change:  # Only for updates
            try:
                old_obj = Withdrawal.objects.get(pk=obj.pk)
                # Check if status changed to rejected - refund the balance
                if old_obj.status != 'rejected' and obj.status == 'rejected':
                    user = obj.user
                    user.balance += obj.amount
                    user.save()
                    self.message_user(request, f'Balance refunded: ${obj.amount} to {user.email}')
            except Withdrawal.DoesNotExist:
                pass
        
        # Set processed_by if status is completed or rejected
        if obj.status in ['completed', 'rejected'] and not obj.processed_by:
            obj.processed_by = request.user
            obj.processed_at = timezone.now()
        
        super().save_model(request, obj, form, change)
    
    def mark_as_processing(self, request, queryset):
        """Mark withdrawals as processing."""
        count = queryset.filter(status='pending').update(status='processing')
        self.message_user(request, f'{count} withdrawal(s) marked as processing.')
    mark_as_processing.short_description = 'Mark as processing'
    
    def mark_as_completed(self, request, queryset):
        """Mark withdrawals as completed."""
        count = 0
        for withdrawal in queryset.filter(status__in=['pending', 'processing']):
            withdrawal.status = 'completed'
            withdrawal.processed_at = timezone.now()
            withdrawal.processed_by = request.user
            withdrawal.save()
            count += 1
        
        self.message_user(request, f'{count} withdrawal(s) marked as completed.')
    mark_as_completed.short_description = 'Mark as completed'
    
    def mark_as_rejected(self, request, queryset):
        """Mark withdrawals as rejected (balance refund handled in save_model)."""
        count = 0
        for withdrawal in queryset.filter(status__in=['pending', 'processing']):
            withdrawal.status = 'rejected'
            withdrawal.processed_at = timezone.now()
            withdrawal.processed_by = request.user
            withdrawal.save()  # This will trigger save_model which handles the refund
            count += 1
        
        self.message_user(request, f'{count} withdrawal(s) marked as rejected and balance refunded.')
    mark_as_rejected.short_description = 'Mark as rejected'
