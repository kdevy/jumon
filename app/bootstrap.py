from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from app.consts import Consts
import os, logging, time
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env"))

db = None

start_time = None

def create_app():
    global db

    db = SQLAlchemy()
    app = Flask(__name__)

    app.secret_key = "TL3kMJFVYseSEDNhjPW5kcRDVQLtXdRwNpGUuBbz"

    app.logger.setLevel(logging._nameToLevel.get(
        os.getenv('LOGGING_LEVEL')) or logging.INFO)
    log_handler = logging.FileHandler(os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "logs/app/common.log"))
    log_formatter = logging.Formatter(
        '[%(asctime)s][%(levelname)s][%(module)s]: %(message)s')
    log_handler.setFormatter(log_formatter)
    app.logger.addHandler(log_handler)

    @app.before_request
    def before_request_callback():
        global start_time
        start_time = time.time()
        app.logger.info("Start application.")
        app.logger.info("request : path = %s, method = %s, remote addr = %s"% (request.path, request.method, request.remote_addr))
        app.logger.info("UA : %s"% (request.user_agent.string))

    @app.after_request
    def after_request_callback(response):
        global start_time
        lap = time.time() - start_time
        app.logger.info("lap : %s s" % (format(lap, '.6f')))
        app.logger.info("Exsit application.")

        return response

    @app.context_processor
    def system():
        system = {
            "lang": "ja",
            "charset": "UTF-8",
        }
        return {"system": system, "consts": Consts}

    app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://{user}:{password}@{host}/{dbName}?charset=utf8".format(
            user = os.getenv('DB_USER'),
            password = os.getenv('DB_PASS'),
            host = os.getenv('DB_HOST'),
            dbName = os.getenv('DB_NAME')
        )

    if int(os.getenv('LOGGING_SQL', 0)):
        app.config["SQLALCHEMY_ECHO"] = True
        logging.basicConfig()
        sql_logger = logging.getLogger("sqlalchemy.engine")
        sql_logger.addHandler(log_handler)

    db.init_app(app)

    from app.modules import home
    app.register_blueprint(home.app)

    return app