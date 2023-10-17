from dataclasses import fields
from django import forms
from vuapp.models import Flowsheet, TextfileUpload, DicomefileUpload


class FlowSheetForm(forms.ModelForm):
    class Meta:
        model = Flowsheet
        fields = "__all__"


class TextfileUploadForm(forms.ModelForm):
    class Meta:
        model = TextfileUpload
        fields = "__all__"


class DicomfileUploadForm(forms.ModelForm):
    class Meta:
        model = DicomefileUpload
        fields = "__all__"
