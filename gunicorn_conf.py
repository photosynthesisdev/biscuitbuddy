from multiprocessing import cpu_count

'''
This is configuration script, which makes Unix socket for API so that NGINX can communicate to player.
Called by api-bootup (which is called by systemctl service)
'''

bind = 'unix:/tmp/gunicorn.sock'

workers = cpu_count() +1
worker_class = 'uvicorn.workers.UvicornWorker'

loglevel = 'error'
accessslog = '/root/biscuitbuddy/bin/access_log'
errorlog = '/root/biscuitbuddy/bin/error_log'