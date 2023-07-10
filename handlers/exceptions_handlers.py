import logging
from datetime import datetime
from selenium.common.exceptions import TimeoutException

# Declare outputs and errors directory paths
outputs_path = "outputs"
error_path = f"{outputs_path}/errors"

# Setup logging config
logging.basicConfig(level=logging.WARNING,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Decorator that handles general exceptions by printing the message and then raising them
def exceptions_handler(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logging.error(f"Exception occurred: {str(e)}", exc_info=True)
    return wrapper


# Decorator that handles timeout exceptions by printing the message and then raising them
# Based on arguments passed to scraper_util.py: webdriver_wait_class(driver: WebDriver, timeout: int, class_name: str)
def timeout_exceptions_handler(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except TimeoutException:
            kwargs["driver"].save_screenshot(
                f"{error_path}/{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}_timeout_exception.png")
            raise TimeoutException(f"Waiting for {kwargs['class_name']} timed out after {kwargs['timeout']}s")
    return wrapper