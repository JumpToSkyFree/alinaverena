from django.http import HttpResponse
from django.conf import settings
from .models import AnonymousClient, Client
from alinaverenaapi import send_message, loop
import telebot


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

    return (len(client) > 0 and len(anon_client) > 0), ipaddress, client


def add_client_ip(ipaddress):
    c = AnonymousClient(user_ipaddress=ipaddress)
    c.save()


class UserIPAddressRegistrationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        status, ipaddress, client = check_client_exists(request)
        if not status:
            add_client_ip(ipaddress)

        return self.get_response(request)

class ClientWebsiteAccessMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        status, ipaddress, client = check_client_exists(request)

        loop.run_until_complete(send_message(f"A new client with ipaddress {ipaddress} have visited the website"))

        return self.get_response(request)