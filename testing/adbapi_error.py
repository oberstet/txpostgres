from twisted.internet import reactor
from twisted.enterprise import adbapi

import sys
from optparse import OptionParser

parser = OptionParser()
parser.add_option("-n", "--hostname", dest = "host", help = "PostgreSQL database host.")
parser.add_option("-d", "--database", dest = "database", help = "Database name.")
parser.add_option("-u", "--user", dest = "user", help = "User name.")
parser.add_option("-p", "--password", dest = "password", help = "User password.")

(options, args) = parser.parse_args()

if not options.host or not options.database or not options.user or not options.password:
   parser.print_help()
   sys.exit(0)

def success(res):
   print "success", res

def failed(err):
   print "%s %s" % (err.type, err.value)
   print err.value.pgcode
   print err.value.pgerror
   return err

conn = adbapi.ConnectionPool("psycopg2",
                             host = options.host,
                             database = options.database,
                             user = options.user,
                             password = options.password)

d1 = conn.runQuery("select * from nonexistent")
d1.addCallbacks(success, failed)
d1.addBoth(lambda _: reactor.stop())

reactor.run()
