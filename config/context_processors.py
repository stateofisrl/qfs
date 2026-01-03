def user_balance(request):
    """Provide current user's balance to all templates when authenticated."""
    try:
        if request.user.is_authenticated:
            return {'balance': request.user.balance}
    except Exception:
        pass
    return {}


def site_settings(request):
    """Provide site settings (currency and language) to all templates."""
    from apps.users.models import SiteSettings
    try:
        settings = SiteSettings.get_settings()
        return {
            'site_currency': settings.currency,
            'site_language': settings.language,
            'currency_symbol': settings.currency.symbol,
            'currency_code': settings.currency.code,
            'language_code': settings.language.code,
        }
    except Exception as e:
        # Return defaults if settings don't exist
        return {
            'site_currency': None,
            'site_language': None,
            'currency_symbol': '$',
            'currency_code': 'USD',
            'language_code': 'en',
        }
