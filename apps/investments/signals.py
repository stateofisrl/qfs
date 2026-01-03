"""
Investments signals.
"""

from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.utils import timezone
from .models import UserInvestment


@receiver(pre_save, sender=UserInvestment)
def handle_investment_status_change(sender, instance, **kwargs):
    """
    Handle investment status changes.
    - If cancelled: refund the invested amount back to user balance
    - If completed: credit the ROI earnings to user balance and update earned field
    """
    if instance.pk:  # Only for existing investments (updates)
        try:
            old_instance = UserInvestment.objects.get(pk=instance.pk)
            
            # CRITICAL: Only refund if status is ACTUALLY CHANGING to cancelled
            # This prevents duplicate refunds on subsequent saves
            if (old_instance.status != instance.status and
                old_instance.status == 'active' and 
                instance.status == 'cancelled'):
                # Refund the invested amount back to user
                instance.user.balance += instance.amount
                # Deduct from total_invested
                instance.user.total_invested -= instance.amount
                instance.user.save()
            
            # CRITICAL: Only credit earnings if status is ACTUALLY CHANGING to completed
            # This prevents duplicate credits on subsequent saves
            if (old_instance.status != instance.status and
                old_instance.status == 'active' and 
                instance.status == 'completed' and
                old_instance.earned == 0):  # Extra safety: only if not already credited
                # Credit the ROI earnings (expected_return) to user balance
                instance.user.balance += instance.expected_return
                # Also return the original investment amount
                instance.user.balance += instance.amount
                # Update earned field to show the ROI amount earned
                instance.earned = instance.expected_return
                # Add to total_earnings (cumulative ROI earnings)
                instance.user.total_earnings += instance.expected_return
                # Deduct from total_invested (investment is complete)
                instance.user.total_invested -= instance.amount
                instance.user.save()
                
        except UserInvestment.DoesNotExist:
            pass


@receiver(post_save, sender=UserInvestment)
def send_investment_created_email(sender, instance, created, **kwargs):
    """Send email when investment is created."""
    if created:
        try:
            from apps.users.emails import send_investment_notification
            print(f"[SIGNAL] Sending investment confirmation email for investment #{instance.pk} - ${instance.amount}")
            send_investment_notification(instance)
            print(f"[SIGNAL] Investment email sent successfully for investment #{instance.pk}")
        except Exception as e:
            print(f"[ERROR] Failed to send investment email: {e}")
            import traceback
            traceback.print_exc()


@receiver(post_save, sender=UserInvestment)
def handle_investment_completion_email(sender, instance, **kwargs):
    """Send email when investment is completed and earnings are credited."""
    if instance.status == 'completed' and instance.earned > 0:
        try:
            # Only send email once per completion
            if not hasattr(instance, '_email_sent'):
                from apps.users.emails import send_investment_completed_notification
                print(f"[SIGNAL] Sending investment completed email for investment #{instance.pk}")
                send_investment_completed_notification(instance)
                print(f"[SIGNAL] Completion email sent successfully for investment #{instance.pk}")
                instance._email_sent = True
        except Exception as e:
            print(f"[ERROR] Failed to send investment completion email: {e}")
            import traceback
            traceback.print_exc()

