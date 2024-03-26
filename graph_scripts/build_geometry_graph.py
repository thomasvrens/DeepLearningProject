from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import numpy as np
import os
import pickle
from multiprocessing import Pool, Value

class Counter(object):
    def __init__(self):
        self.val = Value('i', 0)

    def add(self, n=1):
        with self.val.get_lock():
            self.val.value += n

    @property
    def value(self):
        return self.val.value


def build_geometry_graph(id):
    counter.add(1)
    feats = all_feats[id]
    num_boxes = feats.shape[0]
    edges = []
    relas = []
    
    if id == '71073':
        print('breakpoint')
    
    for i in range(num_boxes):
        if Directed:
            start = 0
        else:
            start = i
        for j in range(start, num_boxes):
            if i==j:
                continue
            # iou and dist thresholds
#            if feats[i][j][3] < Iou or feats[i][j][6] > Dist:
#                continue
            edges.append([i, j])
            relas.append(feats[i][j])

    # in case some trouble is met
    if edges == []:
#        print('id: ', id )
        f = open("../data/single_component_images_directed.txt", "a")
        f.write('%s\n'%(id))
#        edges.append([0, 1])
#        relas.append(feats[0][1])
        edges.append([0, 0])
        relas.append(feats[0][0])

    edges = np.array(edges)
    relas = np.array(relas)
    graph = {}
    graph['edges'] = edges
    graph['feats'] = relas
    np.save(os.path.join(SaveDir, str(id)), graph)

    if counter.value % 100 == 0 and counter.value >= 100:
#    if counter.value % 2 == 0:
        print('{} / {}'.format(counter.value, num_images))


Directed = True  # directed or undirected graph
SaveDir = "../graph_data/geometry-{}directed".format('' if Directed else 'un')
GeometryFeatsPath = '../graph_data/geometry_feats-{}directed.pkl'.format('' if Directed else 'un')

if os.path.exists(SaveDir):
    # raise Exception("dir already exists")
    pass
else:
    os.mkdir(SaveDir)

counter = Counter()
print("loading geometry features of all box pairs....")
with open(GeometryFeatsPath, 'rb') as f:
    all_feats = pickle.load(f)
num_images = len(all_feats)
print("Loaded %d images...." % num_images)

#%%
if __name__ == '__main__':
    p = Pool(20)
    print("[INFO] Start")
    results = p.map(build_geometry_graph, all_feats.keys())
    print("Done")

#for key in all_feats.keys():
#    build_geometry_graph(key)

