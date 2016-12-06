from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.core.urlresolvers import reverse

import sqlite3 as lite

# import the logging library
import logging
# Get an instance of a logger
logger = logging.getLogger(__name__)

# Create your views here.

def index(request):

   logger.info("entering views.index")

   # https://docs.djangoproject.com/en/1.10/intro/tutorial03/

   #-----------------------------------------------------------------------------------
   # Connect to iotmon device database
   #-----------------------------------------------------------------------------------

   db = lite.connect('%s%s.db' % ("/usr/local/bin/", "iotmon.py"))
   # The default cursor returns the data in a tuple of tuples. When we use a dictionary cursor,
   # the data is sent in the form of Python dictionaries. This way we can refer to the data by their column names.
   db.row_factory = lite.Row

   with db:

      cursor = db.cursor()

      cursor.execute("SELECT * FROM Devices ORDER BY State, Descr")
      rows = cursor.fetchall()

   context = {
      'rows': rows,
   }
   return render(request, 'iotmonui/index.html', context)



def log(request):

   logger.info("entering views.log")

   #-----------------------------------------------------------------------------------
   # Connect to iotmon device database
   #-----------------------------------------------------------------------------------

   db = lite.connect('%s%s.db' % ("/usr/local/bin/", "iotmon.py"))
   # The default cursor returns the data in a tuple of tuples. When we use a dictionary cursor,
   # the data is sent in the form of Python dictionaries. This way we can refer to the data by their column names.
   db.row_factory = lite.Row

   with db:

      cursor = db.cursor()

      cursor.execute("SELECT * FROM Log ORDER BY LogDate Desc")
      rows = cursor.fetchall()

   context = {
      'rows': rows,
   }
   return render(request, 'iotmonui/log.html', context)

   if False:
      deviceTable = '<table>'
      deviceTable += "<tr><th>LogDate</th><th>IPAddr</th><th>Descr</th><th>PreviousState</th><th>CurrentState</th></tr>"
      for row in rows:
         deviceTable += "<tr><td>%(LogDate)s</td><td>%(IPAddr)s</td><td>%(Descr)s</td><td>%(PreviousState)s</td><td>%(CurrentState)s</td></tr>" % row
      deviceTable += '</table>'

      header = '''
      <!DOCTYPE html>
      <html>
         <head>
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <title>IoT Monitor Log</title>
         </head>
         <body>
      '''
      footer = '<p><a href="'+reverse('iotmonui:index')+'">Back</a></body></html>'

      return HttpResponse(header+"<h3>Device Monitoring Log</h3>\n"+deviceTable+footer)
