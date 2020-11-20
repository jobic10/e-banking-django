from .models import Customer


def this(request):
    customer = Customer.objects.get(user=request.user)
    return {'this': customer}
