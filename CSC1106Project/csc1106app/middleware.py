class XFrameOptionsMiddleware():
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if request.path.startswith('/media/invoices/') or request.path.startswith('/media/sales/'):
            response['X-Frame-Options'] = 'SAMEORIGIN'  # Or comment out to remove the header
        return response