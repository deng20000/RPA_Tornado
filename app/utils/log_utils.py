import logging
import traceback
import sys
from datetime import datetime

def log_exception(exc: Exception, logger=None):
    """
    记录异常信息，包含行号、时间等。
    - logger 可选，未传则自动输出到控制台。
    """
    exc_type, exc_obj, tb = sys.exc_info()
    fname = traceback.extract_tb(tb)[-1].filename if tb else 'unknown'
    line_no = traceback.extract_tb(tb)[-1].lineno if tb else -1
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    msg = f"[{now}] Exception in {fname} at line {line_no}: {exc}\n{traceback.format_exc()}"
    if logger is None:
        print(msg)
    else:
        logger.error(msg) 