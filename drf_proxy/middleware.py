import logging
import time
import requests
from django.utils import timezone


"""Логирование"""

logger = logging.getLogger(__name__)


"""Получение метрик"""

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start_time = time.time()
        user = request.user.username
        ip_address = request.META.get('REMOTE_ADDR')
        user_agent = request.META.get('HTTP_USER_AGENT', 'Unknown')
        referrer = request.META.get('HTTP_REFERER', 'Direct Access')

        location = self.get_location(ip_address)

        logger.info(
            f"Request: {request.method}, Path: {request.path}, User: {user}, "
            f"IP: {ip_address}, User-Agent: {user_agent}, Referrer: {referrer}, "
            f"Location: {location}, Time: {timezone.now().isoformat()}"
        )

        response = self.get_response(request)
        duration = time.time() - start_time

        logger.info(
            f"Response: {response.status_code}, Duration: {duration:.2f} seconds"
        )

        return response

    def get_location(self, ip_address):
        """Определение локации клиента"""
        try:
            response = requests.get(f'https://ipinfo.io/{ip_address}/json')
            data = response.json()
            location = data.get('city', 'Unknown') + ', ' + data.get('region', 'Unknown') + ', ' + data.get('country', 'Unknown')
            logger.info(location)
            return location
        except Exception as e:
            logger.error(f"Error of getting IP {ip_address}: {e}")
            return 'Unknown'
