import falcon, json, utils, make_json_serializable
from models import Reservation

class ReservationResource(object):

    lx = [
        Reservation('Alice', 'Board Room'),
        Reservation('Bob', 'Lecture Hall'),
        Reservation('Joe', 'Meeting Room 1')
    ]
    items = {}

    def __init__(self):
        for o in ReservationResource.lx:
            self.add_reservation(o)

    def on_get(self, req, res):
        ls = list(ReservationResource.items.values())
        res.body = utils.tojson(ls)

    def on_post(self, req, res):
        raw_json = req.stream.read()
        result = json.loads(raw_json, encoding='utf-8')
        o = Reservation(result['client_name'], result['location'])
        self.add_reservation(o)
        res.body = utils.tojson(o)

    def on_put(self, req, res):
        raw_json = req.stream.read()
        result = json.loads(raw_json, encoding='utf-8')
        o = ReservationResource.items[str(result['reservation_id'])]
        o.client_name = result['client_name']
        o.location = result['location']
        res.body = utils.tojson(o)

    def add_reservation(self, o):
        assert isinstance(o, Reservation)
        if o.reservation_id == 0:
            key = len(ReservationResource.items)
            for k, v in ReservationResource.items.items():
                if str(k) == str(key):
                    key += 1

            o.reservation_id = key

        ReservationResource.items[str(o.reservation_id)] = o
        return o