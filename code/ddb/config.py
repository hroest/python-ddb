import MySQLdb
from ddb import perl

#Here you can set some variables like the db name and the location of the 
#Perl DDB installation. Also 

mysql_conf_file = "~/.my.cnf"
commondb = "ddbMeta"
perl_ddb_location = '/projects/'

debug = True
debug = False

















###########################################################################
## Do not modify anything below this line
###########################################################################

if perl_ddb_location != '':
    perl.eval( "use lib '%s'" % perl_ddb_location)

def get_db_connector():
    db = MySQLdb.connect(read_default_file=mysql_conf_file)

