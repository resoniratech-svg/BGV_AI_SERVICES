import logging
import os


if not os.path.exists("logs"):
    os.makedirs("logs")


logging.basicConfig(

    filename="logs/bgv_ai.log",

    level=logging.INFO,

    format="%(asctime)s %(levelname)s %(message)s"
)


logger = logging.getLogger(__name__)