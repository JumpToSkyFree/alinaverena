from django.http import HttpResponse
from .models import AnonymousClient, Client


def get_client_ip(request) -> str:
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')

    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def check_client_exists(request):
    ipaddress = get_client_ip(request)

    if ipaddress is None:
        return ipaddress

    anon_client = AnonymousClient.objects.filter(user_ipaddress=ipaddress)
    client = Client.objects.filter(user_ipaddress=ipaddress)

    return (client is not None and anon_client is not None), ipaddress, client


def add_client_ip(ipaddress):
    c = AnonymousClient(user_ipaddress=ipaddress)
    c.save()


class UserIPAddressRegistrationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not check_client_exists(request):
            ip = get_client_ip(request)
            add_client_ip(ip)

        return self.get_response(request)
