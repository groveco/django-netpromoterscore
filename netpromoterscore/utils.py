from app_settings import PROMOTERSCORE_USER_RANGES


monthDict = {1: 'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May', 6: 'June', 7: 'July', 8: 'August',
             9: 'September', 10: 'October', 11: 'November', 12: 'December'}


def count_score(score):
    promoters, detractors, passive = score.get('promoters', 0), score.get('detractors', 0), score.get('passive', 0)
    total = promoters + detractors + passive
    if total > 0:
        return round(((promoters - detractors) / float(total)) * 100, 2)
    else:
        return 'Not enough information'


def get_range_name_by_score(score):
    for r_name, range in PROMOTERSCORE_USER_RANGES.iteritems():
        if score in range:
            return r_name
    raise Exception('Range not found')