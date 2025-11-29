from django import forms
from .models import Prediction, Stock

class PredictionForm(forms.ModelForm):
    class Meta:
        model = Prediction
        fields = ['prediction']


class StockForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ['symbol', 'name', 'price', 'total_supply']



class BuyStockForm(forms.Form):
    shares = forms.IntegerField(min_value=1)