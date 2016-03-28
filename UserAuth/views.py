import urllib
import requests
from django.utils import timezone
from .models import SocialAuth
from django.conf import settings
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User
from django.contrib.auth import load_backend, login, authenticate, logout
from drchronoAPI.api import get_user_details
from Greeting.models import Greetings
from django.contrib import messages

AUTHORIZATION_URL = 'https://drchrono.com/o/authorize/?'
ACCESS_TOKEN_URL = 'https://drchrono.com/o/token/'
ACCESS_TOKEN_METHOD = 'POST'
USER_DATA_URL = "https://drchrono.com/api/users/current"


def authorize_url():
    """
    returns the authorization url for drchrono
    """
    params = {
            "client_id": settings.DRCHRONO_KEY,
            "response_type": "code",
            "redirect_uri": settings.REDIRECT_URI,
            "scope": settings.DRCHRONO_SCOPE
    }
    authorization_url = AUTHORIZATION_URL + urllib.urlencode(params)
    return authorization_url


def start_login(request):
    """
    redirects the user to the drchrono website for login
    """
    url = authorize_url()
    return HttpResponseRedirect(url)


def login_user(request, user):
    """
    Log in a user without requiring credentials using ``login`` from
    ``django.contrib.auth``, first finding a matching backend
    """
    for backend in settings.AUTHENTICATION_BACKENDS:
        if user == load_backend(backend).get_user(user.pk):
            user = authenticate(username=user.username)
            login(request, user)
            break


def is_user_doctor(user):
    """
    checks whether the user is a doctor or not(office-staff)
    """
    if user['is_doctor'] is True:
        return True
    return False


def get_access_tokens(code):
    """
    get the access token and other details using the authorization code
    returns the response from the API server
    """
    params = {
        "grant_type": "authorization_code",
        "client_id": settings.DRCHRONO_KEY,
        "client_secret": settings.DRCHRONO_SECRET,
        "redirect_uri": settings.REDIRECT_URI,
        "code": code,
    }
    response = requests.post(ACCESS_TOKEN_URL, data=params)
    return response


def add_update_user_and_greeting(user):
    """
    creates a new user and also creates a new Greeting object with default content for that user
    returns user object if user is doctor or else None
    """
    if is_user_doctor(user):
        username = user['username']
        doctor_id = user['doctor']
        user, created = User.objects.get_or_create(username=username)
        if created:
            user.save()
        try:
            greeting = Greetings.objects.get(doctor=doctor_id)
        except Greetings.DoesNotExist:
            greeting = Greetings.objects.create(user=user, doctor=doctor_id)
        greeting.save()
        return user
    else:
        return None


def add_social_auth(user, tokens):
    """
    creates a UserAuth object for the user with the access-token and other info
    """
    try:
        social = SocialAuth.objects.get(user=user)
        social.access_token = tokens['access_token']
        social.expires_in = tokens['expires_in']
        social.refresh_token = tokens['refresh_token']
    except SocialAuth.DoesNotExist:
        social = SocialAuth.objects.create(user=user, access_token=tokens['access_token'],
                                           expires_in=tokens['expires_in'], refresh_token=tokens['refresh_token'])
    social.save()


def authorize(response):
    """
    authorizes the user to homepage or profile page, based on successful login or not.
    """
    error = response.GET.get('error', '')
    if error:                               # error in the authorization code
        return HttpResponse("Error Occurred {}".format(error))
    code = response.GET.get('code', '')
    tokens = get_access_tokens(code)
    if tokens.status_code == 200:           # successful fetching of tokens
        tokens = tokens.json()
        print tokens
        user = get_user_details(tokens['access_token'])
        if user.status_code == 200:         # successful get of user data from API
            user = add_update_user_and_greeting(user.json())
            if user:                        # user is doctor
                add_social_auth(user, tokens)
                login_user(response, user)
                return HttpResponseRedirect(reverse('home'))
            else:
                messages.add_message(response, messages.ERROR, "The system is currently only for doctors.", fail_silently=True)
                return HttpResponseRedirect(reverse('home'))
        else:
            messages.add_message(response, messages.ERROR, "The system couldn't fetch your details, "
                                                 "Our team will look into the issue", fail_silently=True)
            return HttpResponseRedirect(reverse('home'))
    else:
        messages.add_message(response, messages.ERROR, "There was a problem authorizing you", fail_silently=True)
        return HttpResponseRedirect(reverse('home'))


def authorization_callback(request):
    """
    Receives the response from the drchrono and starts token exchange and login the user
    """
    return authorize(request)


def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))


def is_access_token_active(created, expires_in):
    """
    returns True if access-token is not expired, else returns False
    """
    now = timezone.now()
    diff = (now - created).seconds
    if diff > expires_in:
        return True
    return False


def do_refresh_token(social_auth):
    """
    refreshes the access_token, if it is expired
    """
    params = {
        "grant_type": "refresh_token",
        "client_id": settings.DRCHRONO_KEY,
        "client_secret": settings.DRCHRONO_SECRET,
        "redirect_uri": settings.REDIRECT_URI,
        "refresh_token": social_auth.refresh_token
    }
    response = requests.post(ACCESS_TOKEN_URL, data=params)
    if response.status_code == 200:
        data = response.json()
        print data
        social_auth.access_token = data['access_token']
        social_auth.expires_in = data['expires_in']
        social_auth.refresh_token = data['refresh_token']
        social_auth.save()
        return data['access_token']
    else:
        response.raise_for_status()


def update_access_token(user):
    """
    update the access-token of user if expired
    """
    social_auth = SocialAuth.objects.get(user=user)
    if is_access_token_active(social_auth.created, social_auth.expires_in):
        access_token = social_auth.extra_data['access_token']
    else:
        access_token = do_refresh_token(social_auth)
    return access_token


class PasswordlessAuthBackend(ModelBackend):
    """
    Log in to Django without providing a password.
    """
    def authenticate(self, username=None):
        try:
            return User.objects.get(username=username)
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
