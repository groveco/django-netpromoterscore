from django.conf import settings

PROMOTERSCORE_USER_RANGES_DEFAULT = {
    'promoters': [9, 10],
    'passive': [7, 8],
    'detractors': [1, 2, 3, 4, 5, 6],
    'skipped': [-1]
}

PROMOTERSCORE_PERMISSION_VIEW = getattr(settings, 'PROMOTERSCORE_PERMISSION_VIEW', lambda u: u.is_staff)
PROMOTERSCORE_USER_RANGES = getattr(settings, 'PROMOTERSCORE_USER_RANGES', PROMOTERSCORE_USER_RANGES_DEFAULT)