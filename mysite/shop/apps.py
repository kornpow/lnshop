from django.apps import AppConfig
import os
import logging

logger = logging.getLogger('root')

class ShopConfig(AppConfig):
	name = 'shop'
	
	def ready(self):
		from . import jobs

		# print("starting jobs!")
		logger.info('starting jobs!')
		logger.info(f"environment info: {os.getenv('RUN_MAIN')}")
		
		if os.environ.get('RUN_MAIN', None) != True:
			jobs.start_scheduler()