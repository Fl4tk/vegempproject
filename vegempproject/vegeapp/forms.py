from django import forms

class vegeform(forms.Form):
    vegename = forms.CharField(max_length=50)
    latestdate = forms.CharField(max_length=50)
    price = forms.CharField(max_length=50)
    imgurl = forms.CharField(max_length=50)
    weight = forms.CharField(max_length=50)
    unit = forms.CharField(max_length=50)
