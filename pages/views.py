from django.shortcuts import render
from .tools import get_course
from .models import ParseResult


def IndexView(request):
    #parseresult = ParseResult.objects.order_by('-delivery_time')
    parseresult = ParseResult.objects.all()

    context = {
        'parseresult': parseresult,
    }
    return render(request,
                  template_name='pages/index.html',
                  context=context)
