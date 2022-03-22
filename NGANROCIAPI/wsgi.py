"""
WSGI config for NGANROCIAPI project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/wsgi/
"""

import logging
import os

from django.core.wsgi import get_wsgi_application

from opentelemetry.instrumentation.django import DjangoInstrumentor
from opentelemetry.trace.span import NonRecordingSpan

import nest_asyncio
nest_asyncio.apply()  # required for gevent

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NGANROCIAPI.settings')

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.warning("WSGI called")


def response_hook(span, _, response):
    """Set trace-id in response header for troubleshooting"""
    if not isinstance(span, NonRecordingSpan):
        response.headers["trace-id"] = hex(span.context.trace_id)


DjangoInstrumentor().instrument(response_hook=response_hook)

from opentelemetry.instrumentation.auto_instrumentation import sitecustomize

application = get_wsgi_application()


# if os.environ.get("OTEL_ENABLED") == "yes":
#     from opentelemetry.instrumentation.aiohttp_client import AioHttpClientInstrumentor
#     from opentelemetry.instrumentation.django import DjangoInstrumentor
#     from opentelemetry.instrumentation.redis import RedisInstrumentor
#     from opentelemetry.instrumentation.requests import RequestsInstrumentor
#     # from opentelemetry.instrumentation.wsgi import OpenTelemetryMiddleware
#
#     # application = OpenTelemetryMiddleware(application)
#
#     DjangoInstrumentor().instrument()
#     AioHttpClientInstrumentor().instrument()
#     RedisInstrumentor().instrument()
#     RequestsInstrumentor().instrument()