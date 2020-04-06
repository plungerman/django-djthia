# -*- coding: utf-8 -*-

from djthia.core.utils import get_finaid


class FinancialAidMiddleware(object):
    """Determine if the user must complete the Exit Counseling Form."""

    def __init__(self, get_response):
        """One-time configuration and initialization."""
        self.get_response = get_response

    def __call__(self, request):
        """Code executed for each request/response after the view is called."""
        response = self.get_response(request)
        return response

    def process_template_response(self, request, response):
        """Check status and set the template context."""
        response.context_data['finaid'] = get_finaid(request.user.id)
        return response
