from django.http import HttpResponse


def healthOK(request):
    return HttpResponse("OKAY")