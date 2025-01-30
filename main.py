import matplotlib.pyplot as plt
import networkx as nx

class Node:
    def __init__(self, key, color='VERMELHO', parent=None):
        self.key = key
        self.left = None
        self.right = None
        self.parent = parent
        self.color = color

class RedBlackTree:
    def __init__(self):
        self.NIL = Node(None, color='PRETO')
        self.NIL.left = self.NIL
        self.NIL.right = self.NIL
        self.NIL.parent = None
        self.root = self.NIL

    def insert(self, key):
        new_node = Node(key, parent=None)
        new_node.left = self.NIL
        new_node.right = self.NIL

        parent = None
        current = self.root

        while current is not self.NIL:
            parent = current
            if new_node.key < current.key:
                current = current.left
            else:
                current = current.right

        new_node.parent = parent

        if parent is None:
            self.root = new_node
        elif new_node.key < parent.key:
            parent.left = new_node
        else:
            parent.right = new_node

        new_node.color = 'VERMELHO'
        self._fix_insert(new_node)

    def _fix_insert(self, node):
        while node.parent and node.parent.color == 'VERMELHO':
            if node.parent == node.parent.parent.left:
                uncle = node.parent.parent.right
                if uncle and uncle.color == 'VERMELHO':
                    node.parent.color = 'PRETO'
                    uncle.color = 'PRETO'
                    node.parent.parent.color = 'VERMELHO'
                    node = node.parent.parent
                else:
                    if node == node.parent.right:
                        node = node.parent
                        self._left_rotate(node)
                    node.parent.color = 'PRETO'
                    node.parent.parent.color = 'VERMELHO'
                    self._right_rotate(node.parent.parent)
            else:
                uncle = node.parent.parent.left
                if uncle and uncle.color == 'VERMELHO':
                    node.parent.color = 'PRETO'
                    uncle.color = 'PRETO'
                    node.parent.parent.color = 'VERMELHO'
                    node = node.parent.parent
                else:
                    if node == node.parent.left:
                        node = node.parent
                        self._right_rotate(node)
                    node.parent.color = 'PRETO'
                    node.parent.parent.color = 'VERMELHO'
                    self._left_rotate(node.parent.parent)
            if node == self.root:
                break
        self.root.color = 'PRETO'

    def _left_rotate(self, x):
        y = x.right
        x.right = y.left
        if y.left is not self.NIL:
            y.left.parent = x
        y.parent = x.parent
        if x.parent is None:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.left = x
        x.parent = y

    def _right_rotate(self, y):
        x = y.left
        y.left = x.right
        if x.right is not self.NIL:
            x.right.parent = y
        x.parent = y.parent
        if y.parent is None:
            self.root = x
        elif y == y.parent.right:
            y.parent.right = x
        else:
            y.parent.left = x
        x.right = y
        y.parent = x

    def search(self, key):
        node = self._search(self.root, key)
        return node if node is not self.NIL else None

    def _search(self, node, key):
        if node is self.NIL or key == node.key:
            return node
        if key < node.key:
            return self._search(node.left, key)
        return self._search(node.right, key)

    def inorder_traversal(self, node):
        if node is not self.NIL:
            self.inorder_traversal(node.left)
            print(f'{node.key} ({node.color})')
            self.inorder_traversal(node.right)

    def visualize_tree(self):
        def add_edges(graph, node):
            if node and node != self.NIL:
                if node.left != self.NIL:
                    graph.add_edge(f'{node.key}', f'{node.left.key}')
                if node.right != self.NIL:
                    graph.add_edge(f'{node.key}', f'{node.right.key}')
                add_edges(graph, node.left)
                add_edges(graph, node.right)

        def get_colors(graph):
            colors = []
            for node in graph.nodes():
                node_obj = self.search(int(node))
                if node_obj and node_obj.color == 'VERMELHO':
                    colors.append('red')
                else:
                    colors.append('black')
            return colors

        graph = nx.DiGraph()
        add_edges(graph, self.root)

        pos = nx.spring_layout(graph)
        colors = get_colors(graph)
        labels = {node: f'{node}' for node in graph.nodes()}

        nx.draw(graph, pos, with_labels=True, labels=labels, node_color=colors, node_size=4000, font_color='white', font_size=10)

        plt.show()

# Exemplo de uso
rbt = RedBlackTree()
rbt.insert(10)
rbt.insert(20)
rbt.insert(30)
rbt.insert(15)
rbt.insert(25)
rbt.insert(5)

print(f'A raiz da árvore é: {rbt.root.key} ({rbt.root.color})')

rbt.inorder_traversal(rbt.root)
rbt.visualize_tree()
