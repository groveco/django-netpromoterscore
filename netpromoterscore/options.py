from urllib import urlencode


class Option:
    title = None
    parameter_name = None
    available_choices = None
    default_value = None


    def __init__(self, params):
        self.params = params
        self.chosen_value = self.default_value
        if self.parameter_name in params:
            self.chosen_value = params[self.parameter_name]

    def get_choices(self):
        for lookup, title in self.available_choices:
            yield {
                'selected': self.chosen_value == lookup,
                'display': title,
                'query_string': self.get_query_string({ self.parameter_name: lookup })
            }

    def get_query_string(self, new_params=None):
        if new_params is None:
            new_params = {}
        p = self.params.copy()
        for k, v in new_params.items():
            if v is None:
                if k in p:
                    del p[k]
            else:
                p[k] = v
        return '?%s' % urlencode(sorted(p.items()))


class PeriodOption(Option):
    title = 'By period'
    parameter_name = 'period'
    available_choices = (('month', 'Monthly'), ('week', 'Weekly'), ('day', 'Daily'))
    default_value = 'month'


class RollingOption(Option):
    title = 'By rolling'
    parameter_name = 'rolling'
    available_choices = (('no', 'No'), ('yes', 'Yes'))
    default_value = 'no'


