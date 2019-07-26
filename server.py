import falcon, cherrypy
from resource import reservation_resource

api = falcon.API()
api.add_route('/reservation', reservation_resource.ReservationResource())

if __name__ == '__main__':
    cherrypy.tree.graft(api, '/api')

    cherrypy.server.unsubscribe()

    server = cherrypy._cpserver.Server()

    server.socket_host = "0.0.0.0"
    server.socket_port = 8000
    server.thread_pool = 20

    server.subscribe()

    cherrypy.engine.start()
    cherrypy.engine.block()