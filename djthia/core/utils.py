# -*- coding: utf-8 -*-

import os

from django.conf import settings
from django.core.cache import cache
from djimix.core.utils import get_connection
from djimix.core.utils import xsql
from djimix.sql.students import VITALS


def get_status(cid):
    """Determine if the student is eligible to participate."""
    key = 'gearup_status_{0}'.format(cid)
    status = cache.get(key)
    if not status:
        phile = os.path.join(settings.BASE_DIR, 'sql/gearup.sql')
        with open(phile) as incantation:
            sql = '{0} AND Program_Enrollment_Record.id={1}'.format(
                incantation.read(), cid,
            )
        connection = get_connection()
        with connection:
            row = xsql(sql, connection, key=settings.INFORMIX_DEBUG).fetchone()
            status = False
            if row:
                status = True
            cache.set(key, status)

    return status


def get_student(cid):
    """Fetch student data."""
    key = 'student_vitals_{0}'.format(cid)
    student = cache.get(key)
    if not student:
        with get_connection() as connection:
            cursor = connection.cursor().execute(VITALS(cid=cid))
            # obtain the column names
            columns = [column[0] for column in cursor.description]
            row = cursor.fetchone()
            if row:
                student = dict(zip(columns, row))
                cache.set(key, student)
    return student
