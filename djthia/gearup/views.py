# -*- coding: utf-8 -*-

from django.conf import settings
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from djtools.utils.mail import send_mail

from djthia.gearup.forms import QuestionnaireForm


def home(request, pid=None):
    """Home view with form."""
    if settings.DEBUG:
        to_list = [settings.SERVER_EMAIL]
    else:
        to_list = [settings.GEARUP_EMAIL]

    if request.method == 'POST':
        form = QuestionnaireForm(request.POST, request.FILES)
        if form.is_valid():
            grad = form.save()
            email = settings.DEFAULT_FROM_EMAIL
            if grad.email:
                email = grad.email
            subject = "[Submit] {0} {1}".format(grad.first_name, grad.last_name)
            send_mail(
                request, to_list, subject, email, 'gearup/email.html', grad,
            )
            return HttpResponseRedirect(reverse_lazy('gearup_success'))
    else:
        form = QuestionnaireForm()
    return render(request, 'gearup/form.html', {'form': form})


def search(request):
    """Generic search."""
    return render(request, 'gearup/search.html', {})
