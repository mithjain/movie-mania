def get_clean_url(url: str, leading=True, trailing=True):
    """
    this method removes leading or trailing `/` if asked for
    """
    if leading and url.startswith('/'):
        url = url[1:]
    if trailing and url.endswith('/'):
        url = url[:-1]
    return url
