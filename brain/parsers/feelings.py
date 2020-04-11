def parse_feelings(data):
    if 'feelings' not in data:
        return  # TODO: handle this case
    feelings = data['feelings']
    return feelings


parse_feelings.field = 'feelings'
