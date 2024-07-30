import logging


logging.basicConfig(format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s',
                    level=logging.INFO,
                    filename='logs/notify.log',
                    filemode='a',
                    encoding='utf-8')

logger = logging.getLogger("log")


