#!/usr/bin/python
import argparse
import daemon
import logging
import tornado.ioloop
import tornado.web
import urllib2

class MainHandler(tornado.web.RequestHandler):
    def get(self, slug):
      print slug
      img = "http://www.submitawebsite.com/blog/wp-content/uploads/2010/06/404.png"
      body = '<img src="http://www.submitawebsite.com/blog/wp-content/uploads/2010/06/404.png">'
      if slug == 'i':
        img = self.get_argument("q")
        body = '<img src="%s">' % img
      else:
        url = "http://%s.jpg.to" % (slug)
        response = urllib2.urlopen(url)
        body = response.read()
        img = body[body.find("src=\"")+5:body.find('"', body.find("src=\"")+7)]
      data = """<html>
                <head>
                <meta content="%s" property="og:image"/>
                </head>
                <body>
                %s
                 </body>
                </html> 
            """ % (img, body)
      self.write(data)

application = tornado.web.Application([ (r"/([^/]+)", MainHandler)])

def start_server(port, debug):
  application.listen(port)
  tornado.ioloop.IOLoop.instance().start()

def setup():
  parser = argparse.ArgumentParser()
  parser.add_argument('--port', default=8080,
                      help='http server port')
  parser.add_argument('--debug', action='store_true',
                      help='enable tornado debug mode')
  parser.add_argument('--foreground', action='store_true',
                      help='run server in foreground')
  parser.add_argument('--log-file', default="logs/tornado.log",
                      help='output log when daemonized')
  args = parser.parse_args()
  return args.port, args.debug, args.foreground, args.log_file

def main():
  port, debug, fg, log_file = setup()
  log_fh = open(log_file, 'wa')
  logging.basicConfig(filename=log_file)
  if fg:
    return start_server(port, debug)
  else:
    daemon_context = daemon.DaemonContext(stdout=log_fh, stderr=log_fh)
    with daemon_context:
      return start_server(port, debug)

if __name__ == "__main__":
  main()
