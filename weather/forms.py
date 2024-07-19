from django import forms

class CityForm(forms.Form):
    city = forms.CharField(max_length=100, widget=forms.TextInput(attrs={
        'placeholder': 'Введите название города', 
        'type':'text', 'class':'search-form', 
        'autocomplete':'off',
        'name':'city',
        "class":"search-form",
        "id":"search-input",
        "aria-describedby":"searchCity"
        }))
