#!/usr/bin/python3
import os
import json
import django
os.chdir('..')
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'psbookprogress.settings')
django.setup()

from progress.models import Problem

with open('uva.json', 'r') as f:
    data = json.load(f)
