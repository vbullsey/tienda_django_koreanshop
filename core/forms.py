from django import forms 
from django_countries.fields import CountryField

PAGO_CHOICES = {
    ('C', 'Credito'),
    ('D', 'Debito'),
    ('T', 'Transferencia'),
    ('P', 'PayPal'),
    ('R', 'Retiro en Tienda')
    
}

COMUNA_CHOICES = {
    ('cerrillos', 'Cerrillos'),
    ('cerro-navia', 'Cerro Navia'),
    ('conchali', 'Conchalí'),
    ('el-bosque', 'El Bosque'),
    ('estación-central', 'Estación Central'),
    ('huechuraba', 'Huechuraba'),
    ('independencia', 'Independencia'),
    ('la-cisterna', 'Cisterna'),
    ('la-florida', 'La Florida'),
    ('la-granja', 'La Granja'),
    ('la-pintana', 'La Pintana'),
    ('la-reina', 'La Reina'),
    ('las-condes', 'Las Condes'),
    ('lo-barnechea', 'Lo Barnechea'),
    ('lo-espejo', 'Lo Espejo'),
    ('lo-prado', 'Lo Prado'),
    ('macul', 'Macul'),
    ('maipu', 'Maipú'),
    ('nunoa', 'Ñuñoa'),
    ('padre-hurtado', 'Padre Hurtado'),
    ('pedro-aguirre-cerda', 'Pedro Aguirre Cerda'),
    ('penanolen', 'Peñalolén'),
    ('pirque', 'Pirque'),
    ('providencia', 'Providencia'),
    ('pudahuel', 'Pudahuel'),
    ('puente-alto', 'Puente Alto'),
    ('quinta-normal', 'Quinta Normal'),
    ('recoleta', 'Recoleta'),
    ('renca', 'Renca'),
    ('san-bernardo', 'San Bernardo'),
    ('san-joaquin', 'San Joaquín'),
    ('san-jose-de-maipo', 'San José de Maipo'),
    ('san-miguel', 'San Miguel'),
    ('san-ramon', 'San Ramón'),
    ('penalolen', 'Peñalolén'),
    ('santiago', 'Santiago')
}


class CheckoutForm(forms.Form):
    direccion = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Direccion'
    }))
    direccion_departamento = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'placeholder': 'Departamento o Casa'
    }))
    comuna = forms.ChoiceField(label='' ,choices=COMUNA_CHOICES, widget=forms.Select(attrs={
        'class': 'custom-select d-block w-100'
    }))
    zip = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control'
    }))
    misma_direccion_pago = forms.BooleanField(required=False)
    guardar_informacion = forms.BooleanField(required=False)
    opcion_pago = forms.ChoiceField(
        widget=forms.RadioSelect, choices=PAGO_CHOICES)


