"""
WSGI config for g project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'g.settings')

python_home = '/home/vagrant/.cache/pypoetry/virtualenvs/dj-vtp8n0h9-py3.10'

activate_this = python_home + '/bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))

application = get_wsgi_application()
