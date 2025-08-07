from django.utils import translation

class ForceDefaultLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Let LocaleMiddleware use session/cookie if present
        if not request.COOKIES.get('django_language') and not request.session.get('django_language'):
            translation.activate('tr')
            request.LANGUAGE_CODE = 'tr'
            # ⚠️ Don't set session manually — let LocaleMiddleware handle it
            # request.session['django_language'] = 'tr'  ← REMOVE THIS LINE

        return self.get_response(request)