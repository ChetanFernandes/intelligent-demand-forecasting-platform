import logging
from pythonjsonlogger import jsonlogger
from dotenv import load_dotenv
load_dotenv()
import os, sys

def setup_logging():

    log_level = os.getenv("LOG_LEVEL","INFO")

    # -----------------------------------------
    # Application logger
    # -----------------------------------------
    logger = logging.getLogger() #  Get the root logger

    logger.setLevel(log_level) # set log level

    # Do not propagate to root logger
    #logger.propagate = False # use this only when you are using child logger 
    # logger = logging.getLogger("demand")

    # Remove default handlers
    # Prevent duplicate log output
    logger.handlers.clear() # Remove all handlers that are currently attached to this logger.
    # Remember that a logger needs a handler to decide where the log goes.

    formatter = jsonlogger.JsonFormatter(fmt="%(asctime)s %(levelname)s %(name)s %(message)s")


 #--------------- write in file ----------------------

    #log_dir = os.path.join(os.getcwd(), "logs")
    #os.makedirs(log_dir, exist_ok=True)
    #log_file = os.path.join(log_dir, "log.txt")

    #file_handler = logging.FileHandler(log_file)
    #file_handler.setFormatter(formatter)

    #logger.addHandler(file_handler)


   
#---------------Write in console/stdout------------------
    console_log_handler = logging.StreamHandler(sys.stdout) # Sends logs to console.
    
    console_log_handler.setFormatter(formatter)

    logger.addHandler(console_log_handler)

    # -----------------------------------------
    # Suppress noisy third-party INFO logs
    # -----------------------------------------
    logging.getLogger("boto3").setLevel(logging.WARNING)
    logging.getLogger("botocore").setLevel(logging.WARNING)
    logging.getLogger("s3transfer").setLevel(logging.WARNING)
    logging.getLogger("sagemaker").setLevel(logging.WARNING)

    return logger

'''
                    Python Application
                           │
             ┌─────────────┴─────────────┐
             │                           │
       Your logger                  AWS SDK loggers
       INFO/WARNING/ERROR                 │
             │                    ┌───────┴────────┐
             │                    │                │
             │                  INFO          WARNING/ERROR
             │                    │                │
             │                 SUPPRESS          ALLOW
             │
             └──────────────┬────────────────────┘
                            │
                       ROOT LOGGER
                            │
                     StreamHandler
                            │
                          stdout
                            │
                         Docker
                            │
                       CloudWatch
                            │
                         Grafana
'''