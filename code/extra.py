import psycopg2
import math
from connect import connect
gX = connect()
cur = gX.cur

def degree():
    qback = 'drop  view degree'
    cur.execute(qback)
    q = 'create view degree as select count(testedges.row_id),testnodes.id from testedges, testnodes where testedges.column_id = testnodes.id group by testnodes.id order by testnodes.id;'
    cur.execute(q)
    q1 = 'select min(count) from degree'
    cur.execute(q1)
    min_deg = cur.fetchone()[0]
    q2 = 'select max(count) from degree'
    cur.execute(q2)
    max_deg = cur.fetchone()[0]
    q3 = 'select avg(count) from degree'
    cur.execute(q3)
    avg_deg =cur.fetchone()[0]
    q4 = 'select stddev(count) from degree'
    cur.execute(q4)
    dev_deg = cur.fetchone()[0]
    return (min_deg, max_deg, avg_deg, dev_deg)
    
def get_cluster_node(i):
    cur.execute( 'select node_id from clusters where cluster_id = %s',(i))
    nodes = cur.fetchall()
    return nodes

'''select A.row_id,count(A.column_id) from testedges as A,neigh as B,neigh as C where B.source=C.source and B.neigh=A.row_id and C.neigh = A.column_id group by (A.row_id);
create view neigh as select A.id, B.id from testnodes as A,testnodes as B ,testedges as C where (A.id = C.row_id and B.id = C.column_id ) or (A.id = C.column_id and B.id = C.row_id) ;'''
    
if __name__ == '__main__':
    A = get_degree()
    print A
