from django.utils.deprecation import MiddlewareMixin
from django.contrib.sessions.models import Session
from django.contrib.auth import get_user_model
from .models import UserSession
from django.contrib import messages
from django.utils import timezone
from django.shortcuts import render

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
        request.session.session_invalid = False

        if request.user.is_authenticated:
            current_session_id = request.session.session_key 
            
            user_session, created = UserSession.objects.get_or_create(user=request.user)
            
            try:
                existing_session_exists = Session.objects.filter(session_key=user_session.session_id).exists()
                current_session = Session.objects.get(session_key=current_session_id)
            except Session.DoesNotExist:
                request.session.session_invalid = True
                return 

            if created or user_session.expiry_date < timezone.now() or not existing_session_exists:
                user_session.session_id = current_session.session_key
                user_session.expiry_date = current_session.expire_date
                user_session.save()
                return 
            
            if current_session_id != user_session.session_id:
                current_session.delete()
                request.session.session_invalid = True

    def process_response(self, request, response = None):
        if request.session.session_invalid:
            return render(request, 'login.html')
        
        return response
                    
            
