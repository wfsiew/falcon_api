import decimal, datetime

def getdict(o):
    dic = {}

    if o is None:
        return None

    for k, v in o.__dict__.items():
        if isinstance(v, decimal.Decimal):
            dic[k] = float(v)

        elif isinstance(v, datetime.datetime):
            dic[k] = str(v)

        else:
            dic[k] = v

    return dic

class JsonModel(object):

    def tojson(self):
        return getdict(self)

class Reservation(JsonModel):

    def __init__(self, client_name=None, location=None):
        self.reservation_id = 0
        self.client_name = client_name
        self.location = location