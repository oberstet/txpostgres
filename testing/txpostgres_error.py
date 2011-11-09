from twisted.internet import reactor
from txpostgres.txpostgres import ConnectionPool, Connection

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

conn = Connection()
d = conn.connect(host = options.host,
                 database = options.database,
                 user = options.user,
                 password = options.password)
d.addCallbacks(lambda _: conn.runQuery("select * from nonexistent"), failed)
d.addCallbacks(success, failed)
d.addBoth(lambda _: reactor.stop())

reactor.run()
