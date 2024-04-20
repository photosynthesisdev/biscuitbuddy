from multiprocessing import cpu_count

bind = 'unix:/tmp/gunicorn.sock'

workers = cpu_count() +1
worker_class = 'uvicorn.workers.UvicornWorker'

loglevel = 'error'
accessslog = '/root/biscuitbuddy/bin/access_log'
errorlog = '/root/biscuitbuddy/bin/error_log'