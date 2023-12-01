import logging, os

PATH = os.path.dirname(os.path.abspath(__file__))

logging.basicConfig(
    filename=os.path.join(PATH, './output/app.log'),
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s]: %(message)s'
)

LOGGER = logging.getLogger(__name__)