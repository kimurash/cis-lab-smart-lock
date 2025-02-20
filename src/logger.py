from logging import getLogger
from logging.handlers import RotatingFileHandler
from logging import Formatter

def get_logger():
    logger = getLogger('cis-lab-smart-lock')

    # ログを出力するレベルを設定
    logger.setLevel('WARNING')

    # ハンドラを生成
    handler = RotatingFileHandler(
        filename='smartlock.log',
        maxBytes=10 * 1024 * 1024, # 10MB
        backupCount=1,
        encoding='utf-8'
    )
    # フォーマッタを生成
    formatter = Formatter('%(levelname)-8s %(asctime)s %(filename)s:%(lineno)d %(message)s')
    # ハンドラにフォーマッタを設定
    handler.setFormatter(formatter)
    # ロガーにハンドラを設定
    logger.addHandler(handler)

    return logger

