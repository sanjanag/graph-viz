#!/usr/bin/python2
import numpy as np
import matplotlib
import psycopg2
import math
from connect import connect
import networkx as nx
import matplotlib.pyplot as plt
gX = connect()
cur = gX.cur


def abstract():
    query = "select B.cluster_id as row_id,C.cluster_id as column_id,count(*) as weight from testedges as A,clusters As B,clusters as C where A.row_id = B.node_id and A.column_id = C.node_id and B.cluster_id != C.cluster_id and C.cluster_id < B.cluster_id group by (B.cluster_id, C.cluster_id)"
    cur.execute(query)
    data = cur.fetchall()
    return data


if __name__ == '__main__':
    abstract()
