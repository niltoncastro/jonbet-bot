from datetime import datetime


def display_message(message):
    """Exibe mensagens formatadas com a data e hora."""
    current_time = datetime.now().strftime('%Y%m%d%H%M%S')
    formatted_message = f"{current_time} - {message}"
    print(formatted_message)
