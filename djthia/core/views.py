# -*- coding: utf-8 -*-

from datetime import datetime
import json
import os
import requests

from django.conf import settings
from django.core.cache import cache
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.safestring import mark_safe
from django.views.decorators.csrf import csrf_exempt
from djimix.core.utils import get_connection
from djimix.core.utils import xsql
from djimix.decorators.auth import portal_auth_required
from djthia.core.utils import get_status


@portal_auth_required(
    session_var='DJTHIA_AUTH',
    redirect_url=reverse_lazy('access_denied'),
)
def home(request):
    """Application home."""
    if not request.session.get('gearup_status'):
        get_status(request)
    return render(request, 'home.html', {})


@csrf_exempt
@portal_auth_required(
    session_var='DJTHIA_AUTH',
    redirect_url=reverse_lazy('access_denied'),
)
def clear_cache(request, ctype='blurbs'):
    """Clear the cache for API content."""
    cid = request.POST.get('cid')
    request_type = 'post'
    if not cid:
        cid = request.GET.get('cid')
        request_type = 'get'
    if cid:
        key = 'livewhale_{0}_{1}'.format(ctype, cid)
        cache.delete(key)
        timestamp = datetime.timestamp(datetime.now())
        earl = '{0}/live/{1}/{2}@JSON?cache={3}'.format(
            settings.LIVEWHALE_API_URL, ctype, cid, timestamp,
        )
        try:
            response = requests.get(earl, headers={'Cache-Control': 'no-cache'})
            text = json.loads(response.text)
            cache.set(key, text)
            api_data = mark_safe(text['body'])
        except ValueError:
            api_data = "Cache was not cleared."
        if request_type == 'post':
            content_type = 'text/plain; charset=utf-8'
        else:
            content_type = 'text/html; charset=utf-8'
    else:
        api_data = "Requires a content ID"

    return HttpResponse(api_data, content_type=content_type)
