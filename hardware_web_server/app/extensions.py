
from flask_cors import CORS
cors = CORS()

from app.comm.FlaskRabbitMQ import FlaskRabbitMQ
rabbit = FlaskRabbitMQ()


