# -*- coding: utf-8 -*-

from django.contrib import admin
from djthia.gearup.models import Annotation
from djthia.gearup.models import Document
from djthia.gearup.models import Questionnaire


admin.site.register(Annotation)
admin.site.register(Document)
admin.site.register(Questionnaire)
