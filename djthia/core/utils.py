# -*- coding: utf-8 -*-

import os

from django.conf import settings
from django.core.cache import cache
from djimix.core.utils import get_connection
from djimix.core.utils import xsql
from djimix.people.utils import get_peeps


def get_facstaff():
    """Obtain faculty and staff and build a choices list for form field."""
    peeps = get_peeps('facstaff')
    facstaff = [('', '----select----')]
    for peep in peeps:
        facstaff.append(
            (
                peep['cid'], '{0}, {1}'.format(
                    peep['lastname'], peep['firstname'],
                ),
            ),
        )
    return facstaff


def get_finaid(cid):
    """Determine if the student must complete the Exit Counseling Form."""
    phile = os.path.join(settings.BASE_DIR, 'sql/finaid.sql')
    with open(phile) as incantation:
        sql = '{0} AND id={1}'.format(incantation.read(), cid)
    connection = get_connection()
    with connection:
        row = xsql(sql, connection, key=settings.INFORMIX_DEBUG).fetchone()
        status = False
        if row:
            status = True

    return status


def get_orgs(cid):
    """Fetch the clubs and orgs from informix."""
    orgs = []
    phile = os.path.join(settings.BASE_DIR, 'sql/clubsorgs_student.sql')
    with open(phile) as incantation:
        sql = '{0} {1}'.format(incantation.read(), cid)
    connection = get_connection()
    with connection:
        rows = xsql(sql, connection, key=settings.INFORMIX_DEBUG).fetchall()
        for row in rows:
            if row.name not in orgs:
                orgs.append(row.name)
    return orgs


def get_student(cid):
    """Determine if the student is eligible to participate."""
    key = 'gearup_student_{0}'.format(cid)
    student = cache.get(key)
    if not student:
        phile = os.path.join(settings.BASE_DIR, 'sql/gearup.sql')
        with open(phile) as incantation:
            sql = '{0} AND Program_Enrollment_Record.id={1}'.format(
                incantation.read(), cid,
            )
        with get_connection() as connection:
            cursor = connection.cursor().execute(sql)
            columns = [column[0] for column in cursor.description]
            row = cursor.fetchone()
            if row:
                student = dict(zip(columns, row))
                cache.set(key, student)

    return student
