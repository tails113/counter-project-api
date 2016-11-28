import pprint
from flask import Flask, request
from celery import Celery
from celery.utils.log import get_task_logger
from kombu import Queue, Exchange
import local_settings

# Loading initial config
config = local_settings.env
app = Flask(__name__)

celery = Celery(
     config.get( 'APPLICATION_NAME', 'counter_project' ),
     broker=config.get( 'CELERY_BROKER' ),
     backend=config.get( 'CELERY_BACKEND' )
)

#Set the default celery queue
celery.conf.update(
     CELERY_DEFAULT_QUEUE = config.get('CELERY_DEFAULT_QUEUE'),
     CELERY_TASK_RESULT_EXPIRES = config.get('CELERY_TASK_RESULT_EXPIRES'),
     CELERY_QUEUES = (
          Queue(
               config.get('CELERY_DEFAULT_QUEUE'),
               Exchange(config.get('CELERY_DEFAULT_QUEUE')),
               routing_key=config.get('CELERY_DEFAULT_QUEUE')),
     )
)

# Used to display errors on webpage       
@app.errorhandler( 500 )
def internal_500_error( exception ):
     app.logger.exception( exception )
     return pprint.pformat( exception ), 500

@app.errorhandler( 404 )
def internal_404_error( exception ):
     app.logger.exception( exception )
     return 'Counter Project<br/>\n%s<br/>\n%s' % ( exception, request.url ), 404

@app.errorhandler( 401 )
def internal_401_error( exception ):
     app.logger.exception( exception )
     return 'Counter Project<br/>\n%s<br/>\n%s' % ( exception, request.url ), 401

@app.route('/get', methods=['GET'])
def get():
     response = celery.send_task('counter_project.core.modify_counter') 
     return response.get(timeout = 15)

@app.route("/status", methods=['GET'])
def status():
     response = celery.send_task('counter_project.core.request_counter') 
     return response.get(timeout = 15)

if __name__ == "__main__":
     app.run()
