import argparse

def str_to_bool(value):
    """Convert string to boolean."""
    if isinstance(value, bool):
        return value
    if value.lower() in ("yes", "true", "t", "1"):
        return True
    elif value.lower() in ("no", "false", "f", "0"):
        return False
    else:
        raise argparse.ArgumentTypeError("Boolean value expected.")
    
def selenium_error_transform(error):
    # Convert the exception to a string
    error_message = str(error)
    
    if "(Session info:" in error_message:
        # Handle specific case if needed
        return error_message.split("\n  (Session info: ")[0]
    
    return error_message
