from schedule import Scheduler
import threading
from time import sleep
import os

from shop.models import Order
# from lnd_pyshell.lnd_rest import *
import logging

logger = logging.getLogger('root')

scheduler = Scheduler()

def run_threaded(job_func):
	job_thread = threading.Thread(target=job_func)
	job_thread.start()

def checkInvoices():
	print('Checking Invoices!')
	orders = Order.objects.filter(paid=True)
	print(f"There are {orders.count()} paid for orders")
	neworders = Order.objects.filter(paid=False)
	newpaid = 0
	for aorder in neworders:
		pr = aorder.payment_request
		rhash = decodePR(pr)['payment_hash']
		checkpaid = lookupInvoice(rhash)['settled']
		# Update if unpaid order is now paid
		if checkpaid:
			newpaid += 1
			aorder.paid = True
			aorder.save()


def start_scheduler():
	pass
	# logger.info("starting scheduler")
	# scheduler.every(5).seconds.do(run_threaded,checkInvoices)
	# x = threading.Thread(target=thread_function, daemon=True)
	# x.start()


def thread_function():
	while True:
		scheduler.run_pending()
		print('scheduler ping')
		sleep(2)


