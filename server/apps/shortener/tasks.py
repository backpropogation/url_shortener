import logging

from apps.shortener.service import _clear_expired_links
from config import app

logger = logging.getLogger('root')


@app.task(bind=True, name='cleaner')
def clear_expired_links(self):
    logger.info('Executing clear expired links')
    try:
        _clear_expired_links()
        logger.info('Successfully cleared expired links')
    except Exception as exc:
        logger.info(f'Retrying to clear because of  {str(exc)[:50]}')
        self.retry(countdown=60, exc=exc, max_retries=3)
        logger.critical('Couldn\'t clear expired links')
