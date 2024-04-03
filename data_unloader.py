import pickle
import numpy as np

bar = (1, 2)
class PersistentUnpickler(pickle.Unpickler):
    def persistent_load(self, pers_id):
        """Return the object identified by the persistent id"""
        if pers_id == "it's a bar":
            return bar
        raise pickle.UnpicklingError("This is just an example for one persistent object!")

def test_1():
    with open("external_data/graph/8.pickle", "rb") as in_stream:
        foo2 = PersistentUnpickler(in_stream).load()
        # print(foo2)
        # print(vars(foo2))
        for variable in vars(foo2):
            print(variable)
        print(type(foo2._node[0]['polygon']))
        print(foo2._node[0]['polygon'])
        print(foo2._node[0]['polygon'].bounds)

        # for funct in dir(foo2):
        #     print(funct)
        #print(foo2.variable)
        #print(foo2.edge_attr_dict_factory.keys())

def test_2():
    data_npy = np.load('graph_data/geometry-directed/63091.npy', allow_pickle=True)
    print(type(data_npy))
    print(data_npy.item().keys())
    print(data_npy.item()['edges'])
    print(len(data_npy.item()['feats']))
    #np.set_printoptions(suppress=True, precision=1, formatter={'float_kind':'{:0.2f}'.format})

def test_3():
    with open("graph_data/geometry_feats-directed.pkl", "rb") as in_stream:
        foo3 = PersistentUnpickler(in_stream).load()
    print(len(foo3['63091'][0][0]))
    print(foo3['63091'][2][0])

    print(len(foo3['63091'][0]))
    print(foo3['63091'][0])

    print(len(foo3['63091']))

def test_4():
    with open("data/rico_box_info.pkl", "rb") as in_stream:
        foo2 = PersistentUnpickler(in_stream).load()
    print(foo2['63091'])

    for key in foo2['63091']:
        print(key + ' ' + str(foo2['63091'][key]))

test_4()
