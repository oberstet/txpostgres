from txkqreactor import kqreactor
kqreactor.install()

from twisted.internet import reactor

from txpostgres.txpostgres import Connection

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

def observer(notify):
   print "NOTIFY", notify

conn = Connection()
conn.addNotifyObserver(observer)
d = conn.connect(host = options.host, database = options.database, user = options.user, password = options.password)
d.addCallback(lambda _: conn.runOperation("LISTEN test"))

print "reactor class", reactor.__class__
reactor.run()
