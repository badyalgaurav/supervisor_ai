from multiprocessing import cpu_count

# Socket Path
bind = 'unix:/var/supAPI/supervisor_ai/sup_cloud_fapi/gunicorn.sock'

# Worker Options
workers = cpu_count() + 1
worker_class = 'uvicorn.workers.UvicornWorker'

# Logging Options
loglevel = 'debug'
accesslog = '/var/LiveIXIA/IXIAFastAPI/access_log'
errorlog =  '/var/LiveIXIA/IXIAFastAPI/error_log'
