"""
ASGI config for news_aggregator project.
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'news_aggregator.settings')

application = get_asgi_application()