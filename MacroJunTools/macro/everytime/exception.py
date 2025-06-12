import sys
from functools import wraps
from selenium.common.exceptions import (NoSuchElementException, 
                                        WebDriverException, 
                                        NoSuchWindowException)
from MacroJunTools.macro.everytime.transform import _selenium_error_transform

def exception_handler(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        manager = _get_manager_from_args(*args)

        try:
            return func(self, *args, **kwargs)
        
        except KeyboardInterrupt:
            if manager:
                manager.stop()
            sys.exit("Execution stopped by user (Ctrl+C).")
        
        except NoSuchElementException as e:
            # The login method should continue even if an element is not found
            raise _selenium_error_transform(e)
        
        except (WebDriverException, NoSuchWindowException) as e:
            if manager:
                manager.stop()
            sys.exit("Terminating due to ChromeDriver connection failure.")

        except Exception as e:
            if manager:
                manager.stop()
            sys.exit("Terminating due to an unknown error.")

    return wrapper

def _get_manager_from_args(*args):
    """
    클래스 인스턴스 메서드면 self에서 manager를 찾고,
    일반 함수면 첫 번째 인자를 manager로 간주.
    """
    if len(args) == 0:
        return None

    first_arg = args[0]

    # 클래스 인스턴스 메서드인 경우 (self)
    if hasattr(first_arg, 'browser'):
        return getattr(first_arg, 'browser', None)

    # 일반 함수일 경우 첫 인자를 manager로 간주
    if hasattr(first_arg, 'stop'):
        return first_arg

    return None