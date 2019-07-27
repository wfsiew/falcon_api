import falcon, json, utils, make_json_serializable
from models import Reservation

class ReservationRepo(object):

    lx = [
        Reservation('Alice', 'Board Room'),
        Reservation('Bob', 'Lecture Hall'),
        Reservation('Joe', 'Meeting Room 1')
    ]
    items = {}

    @classmethod
    def init(cls):
        for o in cls.lx:
            cls.add_reservation(o)

    @classmethod
    def add_reservation(cls, o):
        assert isinstance(o, Reservation)
        if o.reservation_id == 0:
            key = len(cls.items)
            for k, v in cls.items.items():
                if str(k) == str(key):
                    key += 1

            o.reservation_id = key

        cls.items[str(o.reservation_id)] = o
        return o

    @classmethod
    def delete_reservation(cls, id):
        del cls.items[str(id)]

class ReservationUpdateResource(object):

    def on_get(self, req, res, id):
        o = ReservationRepo.items[id]
        res.body = utils.tojson(o)

    def on_delete(self, req, res, id):
        ReservationRepo.delete_reservation(id)
        res.body = utils.tojson({ 'success': 1 })

    def on_patch(self, req, res, id):
        raw_json = req.stream.read()
        result = json.loads(raw_json, encoding='utf-8')
        o = ReservationRepo.items[id]
        o.client_name = result['client_name']
        o.location = result['location']
        res.body = utils.tojson(o)

class ReservationResource(object):

    def on_get(self, req, res):
        ls = list(ReservationRepo.items.values())
        res.body = utils.tojson(ls)

    def on_post(self, req, res):
        raw_json = req.stream.read()
        result = json.loads(raw_json, encoding='utf-8')
        o = Reservation(result['client_name'], result['location'])
        ReservationRepo.add_reservation(o)
        res.body = utils.tojson(o)

    def on_put(self, req, res):
        raw_json = req.stream.read()
        result = json.loads(raw_json, encoding='utf-8')
        o = ReservationRepo.items[str(result['reservation_id'])]
        o.client_name = result['client_name']
        o.location = result['location']
        res.body = utils.tojson(o)