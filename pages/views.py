from django.shortcuts import render
from .tools import get_course
from .models import ParseResult
from django.db.models import Sum


def IndexView(request):
    #parseresult = ParseResult.objects.order_by('-delivery_time')
    parseresult = ParseResult.objects.all()

    sum = ParseResult.objects.aggregate(Sum('price'))

    context = {
        'parseresult': parseresult,
        'sum': sum,
    }
    return render(request,
                  template_name='pages/index.html',
                  context=context)
