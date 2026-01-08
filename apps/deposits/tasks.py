"""
Celery tasks for deposits app.
"""

from celery import shared_task
from django.core.management import call_command


@shared_task
def auto_verify_deposits():
    """
    Periodic task to automatically verify pending deposits.
    Runs every 5 minutes via Celery Beat.
    """
    try:
        print("🔍 [Celery Task] Starting automatic deposit verification...")
        
        # Call the management command
        call_command('verify_deposits', '--hours', '24', '--tolerance', '0.01')
        
        print("✅ [Celery Task] Deposit verification completed successfully.")
        return {
            'status': 'success',
            'message': 'Deposit verification completed'
        }
        
    except Exception as e:
        error_msg = f"❌ [Celery Task] Error verifying deposits: {str(e)}"
        print(error_msg)
        return {
            'status': 'error',
            'message': str(e)
        }
