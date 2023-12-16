import logging

from finance_trade.exceptions import CustomException


logger = logging.getLogger(__name__)


def custom_error_handler(error: CustomException):
    logger.exception(str(error), exc_info=error)
    return {"status": "error", "msg": error.msg}, error.code

