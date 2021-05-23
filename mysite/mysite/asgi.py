"""
ASGI config for mysite project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
# from shop.middleware import websockets
import asyncio

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')

application = get_asgi_application()
# loop = asyncio.get_event_loop()
# application = asyncio.ensure_future(websockets(application))
# application = await websockets(application)
# application = asyncio.run(websockets(application))
# application = websockets(application)