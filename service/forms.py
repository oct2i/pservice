from django import forms
from .models import Candidate


class CandidateForm(forms.ModelForm):

    class Meta:
        model = Candidate
        fields = ('name', 'age', 'email', 'residence_planet',)
