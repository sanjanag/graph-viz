import psycopg2
import math
from connect import connect
gX = connect()
curr = gX.cur
def clearTemp():
    print "Starting deletion"
    #print cur.fetchone()[0]
    curr.execute("drop table if exists vt")
    print "Dropped vt"
    curr.execute("drop table if exists v")
    print "Dropped v"
    curr.execute("drop table if exists delta")
    print "Dropped Delta"
    curr.execute("drop table if exists deltat")
    print "Dropped DeltaT"
    curr.execute("drop table if exists a")
    print "Dropped A"
    curr.execute("drop table if exists d")
    print "Dropped d"
    gX.conn.commit()
    print "Committed"
