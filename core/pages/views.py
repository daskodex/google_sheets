from django.shortcuts import render
from .tools import get_course


def IndexView(request):
    context = {
        'currency_course': get_course()
    }
    return render(request,
                  template_name='pages/index.html',
                  context=context)
