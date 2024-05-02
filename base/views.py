from django.contrib.auth import logout, authenticate, login as logon
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect
import traceback
from django.contrib.staticfiles.utils import get_files
from django.contrib.staticfiles.storage import StaticFilesStorage
from django.views.decorators.csrf import csrf_exempt
import json
from base.models import Developer
from locations.models import Country, Continent, State
from server.classes import DjangoAppLogger
from server.config import PASSWORD_COMPLEXITY, BASE_DIR
from server.utils import validate_password

logger = DjangoAppLogger(__name__)


def login(request):
    try:
        message = None
        if request.method == 'POST':
            user = authenticate(
                request, username=request.POST['username'], password=request.POST['password'])
            if user is not None:
                logon(request, user)
                return redirect('home')
            else:
                message = 'Failed to authenticate!'
        return render(request, 'login.html', {'message': message, 'title': 'Login'})
    except Exception as ex:
        logger.write_to_console(str(ex), traceback, 'login')
        request.session['message'] = str(ex)
        return redirect('error')


def register(request):
    try:
        message = None
        from base.forms import RegistrationForm

        if request.method == 'POST':
            form = RegistrationForm(request.POST)
            if form.is_valid():
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']
                if password == form.cleaned_data['password2']:
                    if validate_password(password):
                        Developer.objects.create_user(
                            username=username, password=password)
                        user = authenticate(
                            request, username=username, password=password)
                        if user is not None:
                            logon(request, user)
                            message = 'success'
                        else:
                            message = 'Failed to authenticate!'
                    else:
                        message = PASSWORD_COMPLEXITY
                else:
                    message = 'Passwords do not match!'
            else:
                message = form.errors
        request.session['message'] = message
        return redirect('home')
    except Exception as ex:
        logger.write_to_console(str(ex), traceback, 'register')
        request.session['message'] = str(ex)
        return redirect('error')


@login_required
def resetpassword(request):
    try:
        message = None
        set = None
        if not request.user.has_usable_password():
            set = True
        if request.method == 'POST':
            user = request.user
            if set:
                user.set_password(request.POST['password'])
                user.save()
                return redirect('home')
            else:
                curr_password = request.POST['curr_password']
                user = authenticate(
                    request, username=user.username, password=curr_password)
                if user is not None:
                    user.set_password(request.POST['password'])
                    user.save()
                    return redirect('home')
                message = 'Failed to authenticate!'
        return render(request, 'resetpassword.html', {'set': set, 'message': message, 'title': 'Reset password'})
    except Exception as ex:
        logger.write_to_console(str(ex), traceback, 'reset password')
        request.session['message'] = str(ex)
        return redirect('error')


def home(request):
    try:
        data = {
            'title': 'Home',
            'countries_len': len(Country.objects.all()),
            'continents_len': len(Continent.objects.all()),
            'states_len': len(State.objects.all()),
        }
        return render(request, 'home.html', data)
    except Exception as ex:
        logger.write_to_console(str(ex), traceback, 'Home page')
        request.session['message'] = str(ex)
        return redirect('error')


def sketch(request):
    try:
        s = StaticFilesStorage()
        data = list(get_files(s, location='sketches'))
        return JsonResponse({
            'data': data
        })
    except Exception as ex:
        logger.write_to_console(str(ex), traceback, 'Sketch')
        request.session['message'] = str(ex)
        return redirect('error')


@login_required
def token(request):
    try:
        from rest_framework.authtoken.models import Token
        key, flag = Token.objects.get_or_create(user=request.user)
        return JsonResponse({'token': key.key})
    except Exception as ex:
        logger.write_to_console(str(ex), traceback, 'fetch token')
        request.session['message'] = str(ex)
        return None


@login_required
def logoff(request):
    try:
        logout(request)
        return redirect('home')
    except Exception as ex:
        logger.write_to_console(str(ex), traceback, 'logout')
        request.session['message'] = str(ex)
        return redirect('error')


@csrf_exempt
def visit(request):
    data = {}
    try:
        if request.method == 'POST':
            coordinates_from_client = False
            req_data = json.loads(request.body.decode('utf-8'))
            if 'latitude' in req_data:
                latitude = req_data['latitude']
                longitude = req_data['longitude']
                coordinates_from_client = True
            else:
                ip_address = request.META.get('HTTP_X_FORWARDED_FOR')
                reader = geoip2.database.Reader(
                    os.path.join(BASE_DIR, 'geolite.mmdb'))
                response = reader.city(ip_address)
                latitude = response.location.latitude
                longitude = response.location.longitude
            message_str = f"""
            <!DOCTYPE html>
<html>
<body style="font-family: Arial, sans-serif; margin: 0; padding: 0;">
    <div class="container" style="max-width: 1000px; margin: 0 auto; padding: 20px;">
        <div class="header" style="background-color: #007BFF; color: #fff; padding: 10px; text-align: center;">
            <h1>Message from vishnusayanth.com</h1>
        </div>
        <div class="content" style="padding: 20px;">
            <p>Hello,</p>
            <p>
There has been a new visit at {request.META.get('HTTP_ORIGIN')}.
Visitor location is{" approximately" if coordinates_from_client is False else ""} https://www.google.com/maps?q={latitude},{longitude}
            </p>
        </div>
        <br/>
        <br/>
    </div>
</body>
</html>
"""
            smtp_server = smtplib.SMTP_SSL('smtp.gmail.com', 587)
            smtp_server.login(
                os.environ["EMAIL"], os.environ["EMAIL_PASSWORD"])
            msg = MIMEText(message_str, 'html')
            msg['Subject'] = 'New site visit!'
            msg['From'] = os.environ["EMAIL"]
            msg['To'] = 'vishnusayanth@gmail.com'
            resp = smtp_server.sendmail(self.from_email, i, msg.as_string())
            smtp_server.quit()
            print('email sent!')
            data = {
                'data': True,
            }
    except Exception as ex:
        log(ex, traceback.format_exc())
        data = {
            'error': str(ex)
        }
    return JsonResponse(data)
