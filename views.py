from django.shortcuts import render
from django.http import HttpResponse

import sqlite3 as lite

# Create your views here.

def index(request):


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

      deviceTable = '<table>'
      deviceTable += "<tr><th>IPAddr</th><th>Descr</th><th>State</th><th>LastStateChange</th><th>SuppressCount</th><th>CurrentSuppressCount</th></tr>"
      for row in rows:
         deviceTable += "<tr><td>%(IPAddr)s</td><td>%(Descr)s</td><td>%(State)s</td><td>%(LastStateChange)s</td><td>%(SuppressCount)d</td><td>%(CurrentSuppressCount)d</td></tr>" % row
      deviceTable += '</table>'

      footer = '<p><a href="/iotmon/log">View Log</a>'

      return HttpResponse("<h3>Current Device Monitoring info</h3>\n"+deviceTable+footer)




def log(request):


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

      deviceTable = '<table>'
      deviceTable += "<tr><th>LogDate</th><th>IPAddr</th><th>Descr</th><th>PreviousState</th><th>CurrentState</th></tr>"
      for row in rows:
         deviceTable += "<tr><td>%(LogDate)s</td><td>%(IPAddr)s</td><td>%(Descr)s</td><td>%(PreviousState)s</td><td>%(CurrentState)s</td></tr>" % row
      deviceTable += '</table>'

      header = '<html><head><title>IoT Monitor</title></head><body>'
      footer = '<p><a href="/iotmon">Back</a></body></html>'

      return HttpResponse(header+"<h3>Device Monitoring Log</h3>\n"+deviceTable+footer)
