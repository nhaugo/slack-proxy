#!/usr/bin/python
"""
Copyright (c) 2014 Nathan Haugo nhaugo@gmail.com
All rights reserved.

Redistribution and use in source and binary forms are permitted
provided that the above copyright notice and this paragraph are
duplicated in all such forms and that any documentation,
advertising materials, and other materials related to such
distribution and use acknowledge that the software was developed
by the <organization>.  The name of the
<organization> may not be used to endorse or promote products derived
from this software without specific prior written permission.
THIS SOFTWARE IS PROVIDED ``AS IS'' AND WITHOUT ANY EXPRESS OR
IMPLIED WARRANTIES, INCLUDING, WITHOUT LIMITATION, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.
"""
import argparse
import BeautifulSoup
import daemon
import logging
import tornado.ioloop
import tornado.web
import urllib2

class MainHandler(tornado.web.RequestHandler):
    def get(self, slug):
      img = "http://www.submitawebsite.com/blog/wp-content/uploads/2010/06/404.png"
      body = '<img src="http://www.submitawebsite.com/blog/wp-content/uploads/2010/06/404.png">'
      if slug == 'i':
        body = '<img src="%s">' % img
      else:
        url = "http://%s.jpg.to" % (slug)
        response = urllib2.urlopen(url)
        body = response.read()
      try:
        img = BeautifulSoup.BeautifulSoup(body).img['src']
      except:
        print "Bad img in %s" % body
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
