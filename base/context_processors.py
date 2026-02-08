from django.conf import settings


def turnstile(request):
    """
    Makes the Turnstile Site Key available in every template.
    """
    return {
        'TURNSTILE_SITE_KEY': getattr(settings, 'TURNSTILE_SITE_KEY', '')
    }
