import traceback
from base.forms import RegistrationForm
from base.models import RequestCounter
from locations.models import State, Continent
from server.classes import DjangoAppLogger
from server.config import  ZOMATO_IFRAME_URL

logger = DjangoAppLogger(__name__)


def cleanup_social_account(backend, uid, user=None, *args, **kwargs):
    try:
        if user and kwargs.get('is_new', False):
            user.username = kwargs['details']['username']
            user.url = kwargs['response']['html_url']
            user.save()
    except Exception as ex:
        logger.write_to_console(str(ex),traceback, ' clean up after social login.')
    return {'user': user}


def custom_context(request):
    return {
        'zomato_url': ZOMATO_IFRAME_URL,
        'locations': State.objects.all().values_list('name', flat=True).order_by('name'),
        'continents': Continent.objects.all().values_list('name', flat=True).order_by('name'),
        'registrationform': RegistrationForm()
    }
def CustomRequestMiddleware(get_response):
    # Below function serves the purpose of testing a custom middleware.
    # This function keeps track of number of requests processed by this application and clears
    def middleware(request):
        # if the message is passed to the template once, remove the message from the next request.
        # this message is used mainly for error messages.
        if 'message_shown' in request.session and 'message' in request.session:
            if request.session['message_shown']:
                request.session['message'] = None
                request.session['message_shown'] = False
            elif request.session['message'] is not None:
                request.session['message_shown'] = True
        else:
            request.session['message'] = None
            request.session['message_shown'] = False

        obj = RequestCounter.objects.first()
        if obj is None:
            obj = RequestCounter.objects.create(count=0)
        obj.count += 1
        obj.save()
        response = get_response(request)
        return response

    return middleware




def validate_password(password):
    if len(password) >= 7 and any(char.isdigit() for char in password) and any(
            char.isalpha() for char in str(password)):
        return True
