def get_status_message(code):
    match code:
        case 200:
            return "OK"
        case 404:
            return "Not Found"
        case 418:
            return "I'm a teapot"
        case _:
            return "Unknown"
