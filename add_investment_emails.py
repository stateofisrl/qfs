#!/usr/bin/env python
"""Script to add investment email functions."""

investment_functions = '''

def send_investment_notification(investment):
    """Send email notification when investment is created."""
    user = investment.user
    subject = f'Investment Confirmation - ${investment.amount:,.2f} - Tesla Investment Platform'
    
    html_message = f"""
    <html>
    <body style="font-family: Arial, sans-serif; background-color: #000; color: #fff; padding: 20px;">
        <div style="max-width: 600px; margin: 0 auto; background-color: #1a1a1a; border: 1px solid #333; padding: 30px; border-radius: 8px;">
            <h2 style="color: #fff; margin-bottom: 20px;">✓ Investment Confirmed</h2>
            <p style="color: #ccc; line-height: 1.6;">Hi {user.first_name},</p>
            <p style="color: #ccc; line-height: 1.6;">
                Your investment has been successfully created. You will earn returns based on your investment plan.
            </p>
            <div style="background-color: #222; padding: 20px; border-radius: 6px; margin: 20px 0;">
                <p style="color: #999; margin: 5px 0;">Investment Amount: <strong style="color: #4ade80;">${investment.amount:,.2f}</strong></p>
                <p style="color: #999; margin: 5px 0;">Plan: <strong style="color: #fff;">{investment.plan.name}</strong></p>
                <p style="color: #999; margin: 5px 0;">Expected Return: <strong style="color: #4ade80;">${investment.expected_return:,.2f}</strong></p>
                <p style="color: #999; margin: 5px 0;">ROI: <strong style="color: #fff;">{investment.plan.roi}%</strong></p>
                <p style="color: #999; margin: 5px 0;">Duration: <strong style="color: #fff;">{investment.plan.duration_days} days</strong></p>
                <p style="color: #999; margin: 5px 0;">Start Date: <strong style="color: #fff;">{investment.created_at.strftime('%B %d, %Y')}</strong></p>
                <p style="color: #999; margin: 5px 0;">End Date: <strong style="color: #fff;">{(investment.created_at + investment.plan.duration_timedelta).strftime('%B %d, %Y')}</strong></p>
            </div>
            <p style="color: #4ade80; line-height: 1.6;">✓ Your investment is actively earning returns.</p>
            <div style="text-align: center; margin: 30px 0;">
                <a href="http://127.0.0.1:8001/investments/" style="background-color: #fff; color: #000; padding: 12px 30px; text-decoration: none; border-radius: 6px; font-weight: bold; display: inline-block;">
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
    <body style="font-family: Arial, sans-serif; background-color: #000; color: #fff; padding: 20px;">
        <div style="max-width: 600px; margin: 0 auto; background-color: #1a1a1a; border: 1px solid #333; padding: 30px; border-radius: 8px;">
            <h2 style="color: #4ade80; margin-bottom: 20px;">🎉 Investment Completed & Earnings Credited</h2>
            <p style="color: #ccc; line-height: 1.6;">Hi {user.first_name},</p>
            <p style="color: #ccc; line-height: 1.6;">
                Your investment has completed and your earnings have been credited to your account!
            </p>
            <div style="background-color: #222; padding: 20px; border-radius: 6px; margin: 20px 0;">
                <p style="color: #999; margin: 5px 0;">Original Investment: <strong style="color: #fff;">${investment.amount:,.2f}</strong></p>
                <p style="color: #999; margin: 5px 0;">Earnings (ROI): <strong style="color: #4ade80;">${investment.earned:,.2f}</strong></p>
                <p style="color: #999; margin: 5px 0;">Total Returned: <strong style="color: #4ade80;">${(investment.amount + investment.earned):,.2f}</strong></p>
                <p style="color: #999; margin: 5px 0;">Plan: <strong style="color: #fff;">{investment.plan.name}</strong></p>
                <p style="color: #999; margin: 5px 0;">Completed Date: <strong style="color: #fff;">{investment.updated_at.strftime('%B %d, %Y')}</strong></p>
            </div>
            <p style="color: #4ade80; line-height: 1.6;">✓ Your account balance has been updated with your original investment plus earnings.</p>
            <div style="text-align: center; margin: 30px 0;">
                <a href="http://127.0.0.1:8001/dashboard/" style="background-color: #fff; color: #000; padding: 12px 30px; text-decoration: none; border-radius: 6px; font-weight: bold; display: inline-block;">
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
'''

# Append to emails.py
with open('apps/users/emails.py', 'a') as f:
    f.write(investment_functions)

print("Investment email functions added successfully!")
