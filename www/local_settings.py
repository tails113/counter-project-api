import os
env = {
    'CELERY_BROKER': 'redis://localhost:6379/0',
    'CELERY_BACKEND': 'redis://localhost:6379/0',
    'CELERY_TASK_RESULT_EXPIRES': 1440,
    'REDIS': "localhost",
    'REDIS_DB': 0,
    'REDIS_PORT': 6379,
    'CELERY_DEFAULT_QUEUE': 'counter-project',
    'HOME_DIR': os.path.dirname( os.path.realpath( __file__ ) ),
    'VIRTUALENV_DIR': os.path.dirname( os.path.realpath( __file__ ) ) +  "/env/lib/python2.7/site-packages"
}
