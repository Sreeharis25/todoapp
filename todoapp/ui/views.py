"""Views for ui app."""
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render


def home(request):
    """View to return index."""
    return render(request, 'index.html')


def serve_partials(request, path):
    """View to server partials."""
    return render(
        request, 'partials/' + path)
