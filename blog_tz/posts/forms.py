from django import forms
from .models import Comments



class CommentForm(forms.ModelForm):
	content = forms.CharField(label = '', widget = forms.Textarea(attrs = {'class':'form-control', 'rows': 4, 'cols':100, 'placeholder': 'Type the comment'}))
	class Meta:
		model = Comments
		fields = ['content']
