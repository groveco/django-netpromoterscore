from django.conf import settings

PROMOTERSCORE_PERMISSION_VIEW = getattr(settings, 'PROMOTERSCORE_PERMISSION_VIEW', lambda u: u.is_staff)