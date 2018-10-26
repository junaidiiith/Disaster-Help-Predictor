from django import forms
from blog.models.image import Image

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ('name', 'document', )
