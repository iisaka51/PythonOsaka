import pickle

class Node:
    """ 簡単な有向グラフ """
    def __init__(self, name):
        self.name = name
        self.connections = []

    def add_edge(self, node):
        """ このノードと他のノードの間にエッジを作成 """
        self.connections.append(node)

    def __iter__(self):
        return iter(self.connections)

def preorder_traversal(root, seen=None, parent=None):
    """ グラフのエッジを生成するジェネレータ関数 """
    if seen is None:
        seen = set()
    yield (parent, root)
    if root in seen:
        return
    seen.add(root)
    for node in root:
        recurse = preorder_traversal(node, seen, root)
        for parent, subnode in recurse:
            yield (parent, subnode)

def show_edges(root):
    """ グラフのすべてのエッジを出力 """
    for parent, child in preorder_traversal(root):
        if not parent:
            continue
        print(f'{parent.name:>5} -> {child.name:>2} ({id(child)}')


# ノードを設定
root = Node('root')
a = Node('a')
b = Node('b')
c = Node('c')

# ノード間のエッジを追加
root.add_edge(a)
root.add_edge(b)
a.add_edge(b)
b.add_edge(a)
b.add_edge(c)
a.add_edge(a)

print('ORIGINAL GRAPH:')
show_edges(root)

# Pickle and unpickle the graph to create
# a new set of nodes.
# グラフをPickle化/非Pickle化して、新しいノードセットを作成
dumped = pickle.dumps(root)
reloaded = pickle.loads(dumped)

print('\nRELOADED GRAPH:')
show_edges(reloaded)
