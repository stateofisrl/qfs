"""
Email utilities for user notifications.
"""

from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags


def get_admin_dashboard_url():
    """Get admin dashboard URL."""
    if settings.DEBUG:
        return "http://127.0.0.1:8001/admin/"
    else:
        # Use the actual Render domain
        return "https://qfs-investment-platform.onrender.com/admin/"


def get_dashboard_url():
    """Get user dashboard URL."""
    if settings.DEBUG:
        return "http://127.0.0.1:8001/dashboard/"
    else:
        # Use the actual Render domain
        return "https://qfs-investment-platform.onrender.com/dashboard/"


def send_verification_email(user, verification_code):
    """Send email verification code to user."""
    subject = 'Verify Your Email Address'
    
    html_message = f"""
    <html>
    <body style="font-family: Arial, sans-serif; background-color: #f5f5f5; color: #333; padding: 20px;">
        <div style="max-width: 600px; margin: 0 auto; background-color: #ffffff; border: 1px solid #e0e0e0; padding: 30px; border-radius: 8px;">
            <h2 style="color: #333; margin-bottom: 20px;">Verify Your Email Address</h2>
            <p style="color: #555; line-height: 1.6;">Hello {user.first_name},</p>
            <p style="color: #555; line-height: 1.6;">
                Thank you for signing up! To complete your registration, please verify your email address.
            </p>
            <div style="background-color: #f9f9f9; padding: 20px; border-radius: 6px; margin: 20px 0; text-align: center; border: 2px dashed #ddd;">
                <p style="color: #666; margin-bottom: 10px;">Your verification code:</p>
                <h1 style="color: #2563eb; font-size: 32px; letter-spacing: 6px; margin: 10px 0; font-family: monospace;">{verification_code}</h1>
            </div>
            <p style="color: #555; line-height: 1.6;">
                Enter this code on the verification page to activate your account.
            </p>
            <p style="color: #777; font-size: 12px; line-height: 1.6; margin-top: 20px; padding-top: 20px; border-top: 1px solid #e0e0e0;">
                This code expires in 24 hours. If you didn't request this, please ignore this email.
            </p>
        </div>
    </body>
    </html>
    """
    
    plain_message = f"""
Verify Your Email Address

Hello {user.first_name},

Thank you for signing up! To complete your registration, please verify your email address.

Your verification code: {verification_code}

Enter this code on the verification page to activate your account.

This code expires in 24 hours. If you didn't request this, please ignore this email.
    """
    
    send_mail(
        subject,
        plain_message,
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        html_message=html_message,
        fail_silently=False,
    )


def send_password_reset_email(user, reset_link):
    """Send password reset email to user."""
    subject = 'Reset Your Password - Tesla Investment Platform'
    
    html_message = f"""
    <html>
    <body style="font-family: Arial, sans-serif; background-color: #f5f5f5; color: #333; padding: 20px;">
        <div style="max-width: 600px; margin: 0 auto; background-color: #ffffff; border: 1px solid #e0e0e0; padding: 30px; border-radius: 8px;">
            <h2 style="color: #333; margin-bottom: 20px;">Password Reset Request</h2>
            <p style="color: #555; line-height: 1.6;">Hi {user.first_name},</p>
            <p style="color: #555; line-height: 1.6;">
                We received a request to reset your password for your Tesla Investment Platform account.
            </p>
            <p style="color: #555; line-height: 1.6;">
                Click the button below to reset your password:
            </p>
            <div style="text-align: center; margin: 30px 0;">
                <a href="{reset_link}" style="background-color: #2563eb; color: #fff; padding: 12px 30px; text-decoration: none; border-radius: 6px; font-weight: bold; display: inline-block;">
                    Reset Password
                </a>
            </div>
            <p style="color: #666; font-size: 12px; line-height: 1.6;">
                If you didn't request this, you can safely ignore this email.
                This link will expire in 24 hours.
            </p>
            <p style="color: #666; font-size: 12px; line-height: 1.6;">
                If the button doesn't work, copy and paste this link into your browser:<br>
                <span style="color: #666;">{reset_link}</span>
            </p>
        </div>
    </body>
    </html>
    """
    
    plain_message = strip_tags(html_message)
    
    send_mail(
        subject,
        plain_message,
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        html_message=html_message,
        fail_silently=True,
    )


def send_deposit_notification(deposit):
    """Send email notification when deposit is approved."""
    user = deposit.user
    subject = f'Deposit {"Approved" if deposit.status == "approved" else "Rejected"} - Tesla Investment Platform'
    
    # Use currency_amount (USD) for display, fallback to amount if not set
    amount_display = f"${deposit.currency_amount:,.2f}" if deposit.currency_amount else f"{deposit.amount} {deposit.cryptocurrency}"
    
    html_message = f"""
    <html>
    <body style="font-family: Arial, sans-serif; background-color: #f5f5f5; color: #333; padding: 20px;">
        <div style="max-width: 600px; margin: 0 auto; background-color: #ffffff; border: 1px solid #e0e0e0; padding: 30px; border-radius: 8px;">
            <h2 style="color: #333; margin-bottom: 20px;">Deposit {deposit.get_status_display()}</h2>
            <p style="color: #555; line-height: 1.6;">Hi {user.first_name},</p>
            <p style="color: #555; line-height: 1.6;">
                Your deposit of <strong style="color: #333;">{amount_display}</strong> has been <strong>{deposit.get_status_display().lower()}</strong>.
            </p>
            <div style="background-color: #f9f9f9; padding: 20px; border-radius: 6px; margin: 20px 0;">
                <p style="color: #666; margin: 5px 0;">Deposit Amount: <strong style="color: #333;">{amount_display}</strong></p>
                <p style="color: #666; margin: 5px 0;">Cryptocurrency Received: <strong style="color: #333;">{deposit.amount:.8f} {deposit.cryptocurrency}</strong></p>
                <p style="color: #666; margin: 5px 0;">Status: <strong style="color: {'#4ade80' if deposit.status == 'approved' else '#f87171'};">{deposit.get_status_display()}</strong></p>
                <p style="color: #666; margin: 5px 0;">Date: <strong style="color: #333;">{deposit.created_at.strftime('%B %d, %Y at %I:%M %p')}</strong></p>
            </div>
            {"<p style='color: #4ade80; line-height: 1.6;'>✓ Your account balance has been credited.</p>" if deposit.status == 'approved' else "<p style='color: #f87171; line-height: 1.6;'>✗ Please contact support if you have questions.</p>"}
            <div style="text-align: center; margin: 30px 0;">
                <a href="{settings.ALLOWED_HOSTS[0] if settings.ALLOWED_HOSTS and settings.ALLOWED_HOSTS[0] != '*' else 'http://127.0.0.1:8001'}/dashboard/" style="background-color: #2563eb; color: #fff; padding: 12px 30px; text-decoration: none; border-radius: 6px; font-weight: bold; display: inline-block;">
                    View Dashboard
                </a>
            </div>
        </div>
    </body>
    </html>
    """
    
    plain_message = strip_tags(html_message)
    
    send_mail(
        subject,
        plain_message,
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        html_message=html_message,
        fail_silently=True,
    )


def send_withdrawal_notification(withdrawal):
    """Send email notification when withdrawal is processed."""
    user = withdrawal.user
    subject = f'Withdrawal {withdrawal.get_status_display()} - Tesla Investment Platform'
    
    # Use amount (already in USD) for display
    amount_display = f"${withdrawal.amount:,.2f}"
    
    html_message = f"""
    <html>
    <body style="font-family: Arial, sans-serif; background-color: #f5f5f5; color: #333; padding: 20px;">
        <div style="max-width: 600px; margin: 0 auto; background-color: #ffffff; border: 1px solid #e0e0e0; padding: 30px; border-radius: 8px;">
            <h2 style="color: #333; margin-bottom: 20px;">Withdrawal {withdrawal.get_status_display()}</h2>
            <p style="color: #555; line-height: 1.6;">Hi {user.first_name},</p>
            <p style="color: #555; line-height: 1.6;">
                Your withdrawal request of <strong style="color: #333;">{amount_display}</strong> has been <strong>{withdrawal.get_status_display().lower()}</strong>.
            </p>
            <div style="background-color: #f9f9f9; padding: 20px; border-radius: 6px; margin: 20px 0;">
                <p style="color: #666; margin: 5px 0;">Amount: <strong style="color: #333;">{amount_display}</strong></p>
                <p style="color: #666; margin: 5px 0;">Cryptocurrency: <strong style="color: #333;">{withdrawal.cryptocurrency}</strong></p>
                <p style="color: #666; margin: 5px 0;">Status: <strong style="color: {'#4ade80' if withdrawal.status == 'completed' else '#f87171' if withdrawal.status == 'rejected' else '#fbbf24'};">{withdrawal.get_status_display()}</strong></p>
                <p style="color: #666; margin: 5px 0;">Date: <strong style="color: #333;">{withdrawal.created_at.strftime('%B %d, %Y at %I:%M %p')}</strong></p>
            </div>
            {"<p style='color: #4ade80; line-height: 1.6;'>✓ Your funds have been sent to your account.</p>" if withdrawal.status == 'completed' else "<p style='color: #f87171; line-height: 1.6;'>✗ Your balance has been refunded. Contact support for details.</p>" if withdrawal.status == 'rejected' else "<p style='color: #d97706; line-height: 1.6;'>⏳ Your withdrawal is being processed.</p>"}
            <div style="text-align: center; margin: 30px 0;">
                <a href="{settings.ALLOWED_HOSTS[0] if settings.ALLOWED_HOSTS and settings.ALLOWED_HOSTS[0] != '*' else 'http://127.0.0.1:8001'}/withdrawals/" style="background-color: #2563eb; color: #fff; padding: 12px 30px; text-decoration: none; border-radius: 6px; font-weight: bold; display: inline-block;">
                    View Withdrawals
                </a>
            </div>
        </div>
    </body>
    </html>
    """
    
    plain_message = strip_tags(html_message)
    
    send_mail(
        subject,
        plain_message,
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        html_message=html_message,
        fail_silently=True,
    )


def send_admin_deposit_notification(deposit):
    """Send email notification to admin when new deposit is created."""
    from django.core.mail import EmailMultiAlternatives
    import os
    
    if not settings.ADMIN_EMAIL:
        print("[EMAIL] No ADMIN_EMAIL configured, skipping admin notification")
        return
    
    user = deposit.user
    # Use currency_amount (USD) for display
    amount_display = f"${deposit.currency_amount:,.2f}" if deposit.currency_amount else f"{deposit.amount} {deposit.cryptocurrency}"
    subject = f'New Deposit Request - {amount_display} from {user.get_full_name()}'
    admin_url = get_admin_dashboard_url()
    
    # Build the full URL for the screenshot
    screenshot_url = ""
    if deposit.proof_image:
        base_url = "https://qfs-investment-platform.onrender.com" if not settings.DEBUG else "http://127.0.0.1:8001"
        screenshot_url = f"{base_url}{deposit.proof_image.url}"
    
    print(f"[EMAIL] Preparing admin deposit notification:")
    print(f"  From: {settings.DEFAULT_FROM_EMAIL}")
    print(f"  To: {settings.ADMIN_EMAIL}")
    print(f"  Subject: {subject}")
    print(f"  Screenshot URL: {screenshot_url}")
    
    html_message = f"""
    <html>
    <body style="font-family: Arial, sans-serif; background-color: #f5f5f5; color: #333; padding: 20px;">
        <div style="max-width: 600px; margin: 0 auto; background-color: #ffffff; border: 1px solid #e0e0e0; padding: 30px; border-radius: 8px;">
            <h2 style="color: #d97706; margin-bottom: 20px;">⚠️ New Deposit Pending Approval</h2>
            <p style="color: #555; line-height: 1.6;">
                A new deposit request requires your attention.
            </p>
            <div style="background-color: #f9f9f9; padding: 20px; border-radius: 6px; margin: 20px 0;">
                <p style="color: #666; margin: 5px 0;">User: <strong style="color: #333;">{user.get_full_name()} ({user.email})</strong></p>
                <p style="color: #666; margin: 5px 0;">Deposit Amount: <strong style="color: #4ade80;">{amount_display}</strong></p>
                <p style="color: #666; margin: 5px 0;">Cryptocurrency Received: <strong style="color: #333;">{deposit.amount:.8f} {deposit.cryptocurrency}</strong></p>
                <p style="color: #666; margin: 5px 0;">Proof Type: <strong style="color: #333;">{deposit.get_proof_type_display()}</strong></p>
                {"<p style='color: #666; margin: 5px 0;'>Transaction ID: <strong style='color: #333;'>" + deposit.proof_content + "</strong></p>" if deposit.proof_type == 'transaction_id' and deposit.proof_content else ""}
                {"<p style='color: #666; margin: 5px 0;'>Note: <strong style='color: #333;'>" + deposit.proof_content + "</strong></p>" if deposit.proof_type == 'note' and deposit.proof_content else ""}
                <p style="color: #666; margin: 5px 0;">Status: <strong style="color: #d97706;">Pending</strong></p>
                <p style="color: #666; margin: 5px 0;">Date: <strong style="color: #333;">{deposit.created_at.strftime('%B %d, %Y at %I:%M %p')}</strong></p>
            </div>
            {"<div style='margin: 20px 0; padding: 20px; background-color: #f9f9f9; border-radius: 6px;'><p style='color: #666; margin-bottom: 10px;'><strong>Payment Screenshot:</strong></p><img src='" + screenshot_url + "' style='max-width: 100%; height: auto; border-radius: 4px; border: 1px solid #ddd;' alt='Deposit Proof' /></div>" if deposit.proof_image else ""}
            <div style="text-align: center; margin: 30px 0;">
                <a href="{admin_url}deposits/deposit/{deposit.pk}/change/" style="background-color: #d97706; color: #000; padding: 12px 30px; text-decoration: none; border-radius: 6px; font-weight: bold; display: inline-block;">
                    Review Deposit
                </a>
            </div>
        </div>
    </body>
    </html>
    """
    
    plain_message = strip_tags(html_message)
    
    send_mail(
        subject,
        plain_message,
        settings.DEFAULT_FROM_EMAIL,
        [settings.ADMIN_EMAIL],
        html_message=html_message,
        fail_silently=True,
    )


def send_admin_withdrawal_notification(withdrawal):
    """Send email notification to admin when new withdrawal is created."""
    if not settings.ADMIN_EMAIL:
        print("[EMAIL] No ADMIN_EMAIL configured, skipping admin notification")
        return
    
    user = withdrawal.user
    subject = f'New Withdrawal Request - ${withdrawal.amount} from {user.get_full_name()}'
    admin_url = get_admin_dashboard_url()
    
    print(f"[EMAIL] Preparing admin withdrawal notification:")
    print(f"  From: {settings.DEFAULT_FROM_EMAIL}")
    print(f"  To: {settings.ADMIN_EMAIL}")
    print(f"  Subject: {subject}")
    
    html_message = f"""
    <html>
    <body style="font-family: Arial, sans-serif; background-color: #f5f5f5; color: #333; padding: 20px;">
        <div style="max-width: 600px; margin: 0 auto; background-color: #ffffff; border: 1px solid #e0e0e0; padding: 30px; border-radius: 8px;">
            <h2 style="color: #d97706; margin-bottom: 20px;">⚠️ New Withdrawal Pending Approval</h2>
            <p style="color: #555; line-height: 1.6;">
                A new withdrawal request requires your attention.
            </p>
            <div style="background-color: #f9f9f9; padding: 20px; border-radius: 6px; margin: 20px 0;">
                <p style="color: #666; margin: 5px 0;">User: <strong style="color: #333;">{user.get_full_name()} ({user.email})</strong></p>
                <p style="color: #666; margin: 5px 0;">Amount: <strong style="color: #f87171;">${withdrawal.amount}</strong></p>
                <p style="color: #666; margin: 5px 0;">Cryptocurrency: <strong style="color: #333;">{withdrawal.cryptocurrency}</strong></p>
                <p style="color: #666; margin: 5px 0;">Wallet Address: <strong style="color: #333;">{withdrawal.wallet_address}</strong></p>
                <p style="color: #666; margin: 5px 0;">User Balance: <strong style="color: #4ade80;">${user.balance}</strong></p>
                <p style="color: #666; margin: 5px 0;">Status: <strong style="color: #d97706;">Pending</strong></p>
                <p style="color: #666; margin: 5px 0;">Date: <strong style="color: #333;">{withdrawal.created_at.strftime('%B %d, %Y at %I:%M %p')}</strong></p>
            </div>
            <div style="text-align: center; margin: 30px 0;">
                <a href="{admin_url}withdrawals/withdrawal/{withdrawal.pk}/change/" style="background-color: #d97706; color: #000; padding: 12px 30px; text-decoration: none; border-radius: 6px; font-weight: bold; display: inline-block;">
                    Review Withdrawal
                </a>
            </div>
        </div>
    </body>
    </html>
    """
    
    plain_message = strip_tags(html_message)
    
    send_mail(
        subject,
        plain_message,
        settings.DEFAULT_FROM_EMAIL,
        [settings.ADMIN_EMAIL],
        html_message=html_message,
        fail_silently=True,
    )


def send_admin_support_notification(ticket):
    """Send email notification to admin when new support ticket is created."""
    if not settings.ADMIN_EMAIL:
        return
    
    user = ticket.user
    subject = f'New Support Ticket #{ticket.pk} - {ticket.subject}'
    admin_url = get_admin_dashboard_url()
    
    html_message = f"""
    <html>
    <body style="font-family: Arial, sans-serif; background-color: #f5f5f5; color: #333; padding: 20px;">
        <div style="max-width: 600px; margin: 0 auto; background-color: #ffffff; border: 1px solid #e0e0e0; padding: 30px; border-radius: 8px;">
            <h2 style="color: #d97706; margin-bottom: 20px;">📩 New Support Ticket</h2>
            <p style="color: #555; line-height: 1.6;">
                A new support ticket has been created and needs your response.
            </p>
            <div style="background-color: #f9f9f9; padding: 20px; border-radius: 6px; margin: 20px 0;">
                <p style="color: #666; margin: 5px 0;">Ticket: <strong style="color: #333;">#{ticket.pk}</strong></p>
                <p style="color: #666; margin: 5px 0;">User: <strong style="color: #333;">{user.get_full_name()} ({user.email})</strong></p>
                <p style="color: #666; margin: 5px 0;">Subject: <strong style="color: #333;">{ticket.subject}</strong></p>
                <p style="color: #666; margin: 5px 0;">Category: <strong style="color: #333;">{ticket.get_category_display()}</strong></p>
                <p style="color: #666; margin: 5px 0;">Priority: <strong style="color: {'#f87171' if ticket.priority == 'high' else '#fbbf24' if ticket.priority == 'medium' else '#4ade80'};">{ticket.get_priority_display()}</strong></p>
                <p style="color: #666; margin: 5px 0;">Date: <strong style="color: #333;">{ticket.created_at.strftime('%B %d, %Y at %I:%M %p')}</strong></p>
            </div>
            <div style="background-color: #f0f0f0; padding: 15px; border-radius: 6px; margin: 20px 0;">
                <p style="color: #666; margin: 0; font-size: 14px;">Message:</p>
                <p style="color: #555; margin: 10px 0; line-height: 1.6;">{ticket.message[:200]}{"..." if len(ticket.message) > 200 else ""}</p>
            </div>
            <div style="text-align: center; margin: 30px 0;">
                <a href="{admin_url}support/supportticket/{ticket.pk}/change/" style="background-color: #d97706; color: #000; padding: 12px 30px; text-decoration: none; border-radius: 6px; font-weight: bold; display: inline-block;">
                    Reply to Ticket
                </a>
            </div>
        </div>
    </body>
    </html>
    """
    
    plain_message = strip_tags(html_message)
    
    send_mail(
        subject,
        plain_message,
        settings.DEFAULT_FROM_EMAIL,
        [settings.ADMIN_EMAIL],
        html_message=html_message,
        fail_silently=True,
    )


def send_investment_notification(investment):
    """Send email notification when investment is created."""
    user = investment.user
    subject = f'Investment Confirmation - ${investment.amount:,.2f} - Tesla Investment Platform'
    
    html_message = f"""
    <html>
    <body style="font-family: Arial, sans-serif; background-color: #f5f5f5; color: #333; padding: 20px;">
        <div style="max-width: 600px; margin: 0 auto; background-color: #ffffff; border: 1px solid #e0e0e0; padding: 30px; border-radius: 8px;">
            <h2 style="color: #333; margin-bottom: 20px;">✓ Investment Confirmed</h2>
            <p style="color: #555; line-height: 1.6;">Hi {user.first_name},</p>
            <p style="color: #555; line-height: 1.6;">
                Your investment has been successfully created. You will earn returns based on your investment plan.
            </p>
            <div style="background-color: #f9f9f9; padding: 20px; border-radius: 6px; margin: 20px 0;">
                <p style="color: #666; margin: 5px 0;">Investment Amount: <strong style="color: #4ade80;">${investment.amount:,.2f}</strong></p>
                <p style="color: #666; margin: 5px 0;">Plan: <strong style="color: #333;">{investment.plan.name}</strong></p>
                <p style="color: #666; margin: 5px 0;">Expected Return: <strong style="color: #4ade80;">${investment.expected_return:,.2f}</strong></p>
                <p style="color: #666; margin: 5px 0;">ROI: <strong style="color: #333;">{investment.plan.roi_percentage}%</strong></p>
                <p style="color: #666; margin: 5px 0;">Duration: <strong style="color: #333;">{investment.plan.duration_days} days</strong></p>
                <p style="color: #666; margin: 5px 0;">Start Date: <strong style="color: #333;">{investment.start_date.strftime('%B %d, %Y')}</strong></p>
                <p style="color: #666; margin: 5px 0;">End Date: <strong style="color: #333;">{(investment.end_date).strftime('%B %d, %Y')}</strong></p>
            </div>
            <p style="color: #4ade80; line-height: 1.6;">✓ Your investment is actively earning returns.</p>
            <div style="text-align: center; margin: 30px 0;">
                <a href="http://127.0.0.1:8001/investments/" style="background-color: #2563eb; color: #fff; padding: 12px 30px; text-decoration: none; border-radius: 6px; font-weight: bold; display: inline-block;">
                    View Investments
                </a>
            </div>
        </div>
    </body>
    </html>
    """
    
    plain_message = strip_tags(html_message)
    
    send_mail(
        subject,
        plain_message,
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        html_message=html_message,
        fail_silently=True,
    )


def send_investment_completed_notification(investment):
    """Send email notification when investment completes and earnings are credited."""
    user = investment.user
    subject = f'Investment Completed - ${investment.earned:,.2f} Earnings - Tesla Investment Platform'
    
    html_message = f"""
    <html>
    <body style="font-family: Arial, sans-serif; background-color: #f5f5f5; color: #333; padding: 20px;">
        <div style="max-width: 600px; margin: 0 auto; background-color: #ffffff; border: 1px solid #e0e0e0; padding: 30px; border-radius: 8px;">
            <h2 style="color: #4ade80; margin-bottom: 20px;">🎉 Investment Completed & Earnings Credited</h2>
            <p style="color: #555; line-height: 1.6;">Hi {user.first_name},</p>
            <p style="color: #555; line-height: 1.6;">
                Your investment has completed and your earnings have been credited to your account!
            </p>
            <div style="background-color: #f9f9f9; padding: 20px; border-radius: 6px; margin: 20px 0;">
                <p style="color: #666; margin: 5px 0;">Original Investment: <strong style="color: #333;">${investment.amount:,.2f}</strong></p>
                <p style="color: #666; margin: 5px 0;">Earnings (ROI): <strong style="color: #4ade80;">${investment.earned:,.2f}</strong></p>
                <p style="color: #666; margin: 5px 0;">Total Returned: <strong style="color: #4ade80;">${(investment.amount + investment.earned):,.2f}</strong></p>
                <p style="color: #666; margin: 5px 0;">Plan: <strong style="color: #333;">{investment.plan.name}</strong></p>
                <p style="color: #666; margin: 5px 0;">Completed Date: <strong style="color: #333;">{investment.updated_at.strftime('%B %d, %Y')}</strong></p>
            </div>
            <p style="color: #4ade80; line-height: 1.6;">✓ Your account balance has been updated with your original investment plus earnings.</p>
            <div style="text-align: center; margin: 30px 0;">
                <a href="http://127.0.0.1:8001/dashboard/" style="background-color: #2563eb; color: #fff; padding: 12px 30px; text-decoration: none; border-radius: 6px; font-weight: bold; display: inline-block;">
                    View Dashboard
                </a>
            </div>
        </div>
    </body>
    </html>
    """
    
    plain_message = strip_tags(html_message)
    
    send_mail(
        subject,
        plain_message,
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        html_message=html_message,
        fail_silently=True,
    )


def send_investment_notification(investment):
    """Send email notification when investment is created."""
    user = investment.user
    subject = f'Investment Confirmation - ${investment.amount:,.2f} - Tesla Investment Platform'
    
    html_message = f"""
    <html>
    <body style="font-family: Arial, sans-serif; background-color: #f5f5f5; color: #333; padding: 20px;">
        <div style="max-width: 600px; margin: 0 auto; background-color: #ffffff; border: 1px solid #e0e0e0; padding: 30px; border-radius: 8px;">
            <h2 style="color: #333; margin-bottom: 20px;">✓ Investment Confirmed</h2>
            <p style="color: #555; line-height: 1.6;">Hi {user.first_name},</p>
            <p style="color: #555; line-height: 1.6;">
                Your investment has been successfully created. You will earn returns based on your investment plan.
            </p>
            <div style="background-color: #f9f9f9; padding: 20px; border-radius: 6px; margin: 20px 0;">
                <p style="color: #666; margin: 5px 0;">Investment Amount: <strong style="color: #4ade80;">${investment.amount:,.2f}</strong></p>
                <p style="color: #666; margin: 5px 0;">Plan: <strong style="color: #333;">{investment.plan.name}</strong></p>
                <p style="color: #666; margin: 5px 0;">Expected Return: <strong style="color: #4ade80;">${investment.expected_return:,.2f}</strong></p>
                <p style="color: #666; margin: 5px 0;">ROI: <strong style="color: #333;">{investment.plan.roi_percentage}%</strong></p>
                <p style="color: #666; margin: 5px 0;">Duration: <strong style="color: #333;">{investment.plan.duration_days} days</strong></p>
                <p style="color: #666; margin: 5px 0;">Start Date: <strong style="color: #333;">{investment.start_date.strftime('%B %d, %Y')}</strong></p>
                <p style="color: #666; margin: 5px 0;">End Date: <strong style="color: #333;">{(investment.end_date).strftime('%B %d, %Y')}</strong></p>
            </div>
            <p style="color: #4ade80; line-height: 1.6;">✓ Your investment is actively earning returns.</p>
            <div style="text-align: center; margin: 30px 0;">
                <a href="http://127.0.0.1:8001/investments/" style="background-color: #2563eb; color: #fff; padding: 12px 30px; text-decoration: none; border-radius: 6px; font-weight: bold; display: inline-block;">
                    View Investments
                </a>
            </div>
        </div>
    </body>
    </html>
    """
    
    plain_message = strip_tags(html_message)
    
    send_mail(
        subject,
        plain_message,
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        html_message=html_message,
        fail_silently=True,
    )


def send_investment_completed_notification(investment):
    """Send email notification when investment completes and earnings are credited."""
    user = investment.user
    subject = f'Investment Completed - ${investment.earned:,.2f} Earnings - Tesla Investment Platform'
    
    html_message = f"""
    <html>
    <body style="font-family: Arial, sans-serif; background-color: #f5f5f5; color: #333; padding: 20px;">
        <div style="max-width: 600px; margin: 0 auto; background-color: #ffffff; border: 1px solid #e0e0e0; padding: 30px; border-radius: 8px;">
            <h2 style="color: #4ade80; margin-bottom: 20px;">🎉 Investment Completed & Earnings Credited</h2>
            <p style="color: #555; line-height: 1.6;">Hi {user.first_name},</p>
            <p style="color: #555; line-height: 1.6;">
                Your investment has completed and your earnings have been credited to your account!
            </p>
            <div style="background-color: #f9f9f9; padding: 20px; border-radius: 6px; margin: 20px 0;">
                <p style="color: #666; margin: 5px 0;">Original Investment: <strong style="color: #333;">${investment.amount:,.2f}</strong></p>
                <p style="color: #666; margin: 5px 0;">Earnings (ROI): <strong style="color: #4ade80;">${investment.earned:,.2f}</strong></p>
                <p style="color: #666; margin: 5px 0;">Total Returned: <strong style="color: #4ade80;">${(investment.amount + investment.earned):,.2f}</strong></p>
                <p style="color: #666; margin: 5px 0;">Plan: <strong style="color: #333;">{investment.plan.name}</strong></p>
                <p style="color: #666; margin: 5px 0;">Completed Date: <strong style="color: #333;">{investment.updated_at.strftime('%B %d, %Y')}</strong></p>
            </div>
            <p style="color: #4ade80; line-height: 1.6;">✓ Your account balance has been updated with your original investment plus earnings.</p>
            <div style="text-align: center; margin: 30px 0;">
                <a href="http://127.0.0.1:8001/dashboard/" style="background-color: #2563eb; color: #fff; padding: 12px 30px; text-decoration: none; border-radius: 6px; font-weight: bold; display: inline-block;">
                    View Dashboard
                </a>
            </div>
        </div>
    </body>
    </html>
    """
    
    plain_message = strip_tags(html_message)
    
    send_mail(
        subject,
        plain_message,
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        html_message=html_message,
        fail_silently=True,
    )





