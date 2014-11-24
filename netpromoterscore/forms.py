from django import forms
from .models import PromoterScore

class PromoterScoreForm(forms.ModelForm):
    reason = forms.CharField(max_length=512, required=False)

    class Meta:
        model = PromoterScore
        fields = ('score', 'reason', 'user')