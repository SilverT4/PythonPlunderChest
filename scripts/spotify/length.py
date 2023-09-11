import datetime

def milliseconds_to_hms(milliseconds):
    # Convert milliseconds to seconds
    seconds = milliseconds / 1000

    # Use divmod to get hours, minutes, and remaining seconds
    hours, remainder = [round(t) for t in divmod(seconds, 3600)]
    minutes, seconds = [round(t) for t in divmod(remainder, 60)]

    formatted_time = f"{hours}:{f'0{minutes}' if minutes < 10 else minutes}:{f'0{seconds}' if seconds < 10 else seconds}" if hours >= 1 else f"{minutes}:{f'0{seconds}' if seconds < 10 else seconds}"

    return formatted_time
def formatn(n,s):
    if n == 1:
        return '{n} {s}'.format(n=n,s=s)
    else:
        return '{n} {s}s'.format(n=n,s=s)
def runtime(ms):
    # Convert milliseconds to seconds
    seconds = ms / 1000

    # Use divmod to get hours, minutes, and remaining seconds
    hours, remainder = [round(t) for t in divmod(seconds, 3600)]
    minutes, seconds = [round(t) for t in divmod(remainder, 60)]

    formatted_time = []

    # Use the formatn function to format hours, minutes, and seconds
    if hours > 0:
        formatted_time.append(formatn(hours, "hour"))
    if minutes > 0:
        formatted_time.append(formatn(minutes, "minute"))
    if seconds > 0:
        formatted_time.append(formatn(seconds, "second"))

    return ', '.join(formatted_time)