# predict/forms.py
from django import forms

class HousePriceForm(forms.Form):
    # 共通のウィジェット設定
    # min_value=0 を入れることで、マイナス値の入力をブラウザ側で防げます
    
    n1 = forms.FloatField(
        label='平均地域所得',
        widget=forms.NumberInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': '例：50000ドル',
            'step': '1000'
        }),
        min_value=0
    )
    
    n2 = forms.FloatField(
        label='平均築年数',
        widget=forms.NumberInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': '例：7年',
            'step': '0.1'
        }),
        min_value=0
    )
    
    n3 = forms.FloatField(
        label='1戸あたり平均部屋数',
        widget=forms.NumberInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': '例：5部屋',
            'step': '0.1'
        }),
        min_value=0
    )
    
    n4 = forms.FloatField(
        label='1戸あたり寝室数',
        widget=forms.NumberInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': '例：3部屋',
            'step': '0.1'
        }),
        min_value=0
    )
    
    n5 = forms.FloatField(
        label='地域人口',
        widget=forms.NumberInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': '例：20000人',
            'step': '100'
        }),
        min_value=0
    )