import psycopg2
import math
from connect import connect
gX = connect()
curr = gX.cur
def clearCluster():
    curr.execute("drop table if exists centroids")
    curr.execute("drop table if exists clusters")
    gX.conn.commit()
