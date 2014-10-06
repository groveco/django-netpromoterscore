from django import forms
from .models import PromoterScore

class PromoterScoreForm(forms.ModelForm):
    score = forms.IntegerField(min_value=-1, max_value=10, required=False)
    reason = forms.CharField(max_length=512, required=False)

    class Meta:
        model = PromoterScore
        fields = ('score', 'reason', 'user')
