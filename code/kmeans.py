import psycopg2
import math
from connect import connect
gX = connect()
cur = gX.cur

def scale_v():
    cur.execute("select min(weight) from v")
    minw = cur.fetchone()[0]
    cur.execute("select max(weight) from v")
    maxw = cur.fetchone()[0]
    cur.execute("update V set weight = (weight-%(minw)s)/(%(maxw)s-%(minw)s)",{'minw':minw, 'maxw':maxw})
    gX.conn.commit()
    cur.execute("update V set weight = 0 where weight < 0.000000000000001")
    gX.conn.commit()

def missing_v():
    cur.execute("select count(*) from testnodes")
    nodes = cur.fetchone()[0]

    for i in range(1,nodes+1):
        cur.execute("select * from V where row_id=%(i)s",{'i':i})
        if(cur.fetchone()==None):
            cur.execute("insert into V values (%(i)s,1,0)",{'i':i})
            gX.conn.commit()
        
def create_centroids():
    cur.execute('''CREATE TABLE IF NOT EXISTS CENTROIDS
    (cluster_id SERIAL NOT NULL,
    weight DOUBLE PRECISION NOT NULL,
    PRIMARY KEY(cluster_id));''')
    gX.conn.commit()


def initialise_centroids(no_clusters):
    cur.execute("insert into CENTROIDS (weight) select weight from (select distinct weight from V) as x order by random() limit %(no)s",{'no':no_clusters})
    gX.conn.commit()

def create_clusters():
    cur.execute('''CREATE TABLE IF NOT EXISTS CLUSTERS
    (node_id INT NOT NULL,
    cluster_id INT NOT NULL,
    prev_cluster_id INT NOT NULL,
    PRIMARY KEY(node_id));''')
    gX.conn.commit()

def assign_cluster():
    cur.execute("insert into CLUSTERS (node_id,cluster_id, prev_cluster_id) select x.row_id as node_id, min(y.cluster_id) as cluster_id, 0 as prev_cluster_id from ( select v.row_id, min(abs(c.weight-v.weight)) as min_distance from centroids as c, v group by v.row_id) as x, (select c.cluster_id,v.row_id,abs(c.weight-v.weight) as distance from centroids as c,v) as y where x.row_id=y.row_id and x.min_distance=y.distance group by x.row_id")
    gX.conn.commit()

def update_centroids(no_clusters):
    for i in range(1,no_clusters+1):
        cur.execute("update centroids set weight=(select avg(v.weight) from V, (select node_id from clusters where cluster_id=%(i)s) as x where x.node_id=v.row_id) where cluster_id=%(i)s",{'i':i})
        gX.conn.commit()

def reassign_cluster():
    cur.execute("update clusters set  cluster_id = x.cluster_id from (select y.row_id as node_id, min(z.cluster_id) as cluster_id from (select v.row_id, min(abs(c.weight-v.weight)) as min_distance from centroids as c,v group by v.row_id) as y, (select c.cluster_id, v.row_id, abs(c.weight-v.weight) as distance from centroids as c,v) as z where y.row_id=z.row_id and y.min_distance=z.distance group by y.row_id) AS x WHERE clusters.node_id = x.node_id")        
    gX.conn.commit()

def prev_cluster():
    cur.execute("update clusters set prev_cluster_id = x.cluster_id from (select cluster_id,node_id  from clusters) as x where x.node_id = clusters.node_id")
    gX.conn.commit()

def cluster_all(k):
    scale_v()
    missing_v()
    create_centroids()
    print "create_centroids"
    initialise_centroids(int(k))
    print "initialise centroids"
    create_clusters()
    print "create_clusters"
    assign_cluster()
    print("assign clusters")
    
    cur.execute("select count(*) from clusters where cluster_id != prev_cluster_id")
    count = cur.fetchone()[0]
    print count

    iter = 0
    while(count != 0):
        print iter
        update_centroids(int(k))
        print "updated centroids"
        prev_cluster()
        print "updated prev cluster"
        reassign_cluster()
        print "reassigned clusters"
        cur.execute("select count(*) from clusters where cluster_id != prev_cluster_id")
        count = cur.fetchone()[0]
        print count
        iter += 1
    
