from account.models import Producer

def navcontext(request):
    return {'navlist' : Producer.objects.all()}
