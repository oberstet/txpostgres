import sys
from optparse import OptionParser
import select
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

parser = OptionParser()
parser.add_option("-n", "--hostname", dest = "host", help = "PostgreSQL database host.")
parser.add_option("-d", "--database", dest = "database", help = "Database name.")
parser.add_option("-u", "--user", dest = "user", help = "User name.")
parser.add_option("-p", "--password", dest = "password", help = "User password.")

(options, args) = parser.parse_args()

if not options.host or not options.database or not options.user or not options.password:
   parser.print_help()
   sys.exit(0)

conn = psycopg2.connect(host = options.host,
                        database = options.database,
                        user = options.user,
                        password = options.password)

## without the following line, notification will not work!
conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)

curs = conn.cursor()
curs.execute("LISTEN test")
while True:
   if select.select([conn], [], [], 5) == ([], [], []):
      pass
   else:
      conn.poll()
      while conn.notifies:
         notify = conn.notifies.pop()
         print notify.channel, notify.payload
