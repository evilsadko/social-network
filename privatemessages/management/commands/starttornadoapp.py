import signal
import time

import tornado.httpserver
import tornado.ioloop

from django.core.management.base import BaseCommand, CommandError

from privatemessages.tornadoapp import application

class Command(BaseCommand):
    args = '[port_number]'
    help = 'Starts the Tornado application for message handling.'

    def sig_handler(self, sig, frame):
        """Catch signal and init callback"""
        tornado.ioloop.IOLoop.instance().add_callback(self.shutdown)

    def shutdown(self):
        """Stop server and add callback to stop i/o loop"""
        self.http_server.stop()

        io_loop = tornado.ioloop.IOLoop.instance()
        io_loop.add_timeout(time.time() + 2, io_loop.stop)

    def handle(self, *args, **options):
        if len(args) == 1:
            try:
                port = int(args[0])
            except ValueError:
                raise CommandError('Invalid port number specified')
        else:
            port = 8998

        self.http_server = tornado.httpserver.HTTPServer(application)
        # self.http_server.listen(port, address="127.0.0.1")
        self.http_server.listen(port, address="192.168.1.50")
        # self.http_server.listen(port, address="178.158.131.41") server error not IP

        # Init signals handler
        signal.signal(signal.SIGTERM, self.sig_handler)

        # This will also catch KeyboardInterrupt exception
        signal.signal(signal.SIGINT, self.sig_handler)
        print "PORT", port
        tornado.ioloop.IOLoop.instance().start()
