# -*- coding: utf-8 -*-

import os

from django.conf import settings
from django.core.cache import cache
from djimix.core.utils import get_connection
from djimix.core.utils import xsql


def get_status(request):
    """Determine if the student is eligible to participate."""
    status = request.session.get('gearup_status')
    if not status:
        phile = os.path.join(settings.BASE_DIR, 'sql/gearup.sql')
        with open(phile) as incantation:
            sql = '{0} AND Program_Enrollment_Record.id={1}'.format(
                incantation.read(), request.user.id,
            )
        connection = get_connection()
        with connection:
            row = xsql(sql, connection, key=settings.INFORMIX_DEBUG).fetchone()
            if row:
                status = request.session['gearup_status'] = True

    return status
