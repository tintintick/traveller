def compose_url(url_dict):
    args = ''
    if len(url_dict['args']) == 0:
        url = url_dict['host'] + url_dict['path']
        return url

    for key, value in url_dict['args'].items():
        args += key + '=' + value + '&'
    url = '{0}{1}?{2}'.format(url_dict['host'], url_dict['path'], args[:-1])
    return url
