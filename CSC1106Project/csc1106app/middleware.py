from django.utils.deprecation import MiddlewareMixin
from django.contrib.sessions.models import Session
from django.contrib.auth import get_user_model
from .models import UserSession

User = get_user_model()


class XFrameOptionsMiddleware():
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if request.path.startswith('/media/invoices/') or request.path.startswith('/media/sales/'):
            response['X-Frame-Options'] = 'SAMEORIGIN'  # Or comment out to remove the header
        return response
    
class SingleSessionMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.user.is_authenticated:
            current_session_key = request.session.session_key

            #check current user session matches 
            user_sessions = UserSession.objects.filter(user=request.user)
            #if different then check else dont need care
            #need delete if Session.objects.get == same 
            #set a new one

            # Remove all sessions except the current one
            for user_session in user_sessions:
                if user_session.session_id != current_session_key:
                    # Delete session from the session store
                    try:
                        previous_session = Session.objects.get(session_key=user_session.session_id)
                        previous_session.delete()
                    except Session.DoesNotExist:
                        pass
                    
                    # Delete the UserSession record
                    user_session.delete()

            # Update or create the UserSession record for the current session
            user_session, created = UserSession.objects.get_or_create(user=request.user)
            user_session.session_id = current_session_key
            user_session.save()