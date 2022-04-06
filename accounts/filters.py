from attr import fields
import django_filters

from .models import *

class OrdrFilter(django_filters.FilterSet):
    class Meta:
        model = Order
        fields = '__all__'
        exclude = ['Customer']
        
