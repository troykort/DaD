# %% [markdown]
# # Binary search
# 

# %%
arr = [1, 2, 3, 4, 5,6,7,8,9,10,11,12,13,14,15,16]

def binary_search(arr, target):
    low = 0
    high = len(arr) - 1

    while low <= high:
        mid = (low + high) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            low = mid + 1
        else:
            high = mid - 1

    return -1

target = 7
index = binary_search(arr, target)
if index != -1:
    print(f"{target} gevonden op index {index}")
else:
    print(f"{target} niet gevonden in de array")



# %% [markdown]
# O(Logn), omdat na elke niveau de zoek ruimte gehalveerd wordt

# %% [markdown]
# # Print Adjacency List

# %%
class AdjNode:
    def __init__(self, data):
        self.vertex = data
        self.next = None
 
class Graph:
    def __init__(self, vertices):
        self.V = vertices
        self.graph = [None] * self.V
 
    def add_edge(self, src, dest):
       
        node = AdjNode(dest)
        node.next = self.graph[src]
        self.graph[src] = node
 
        node = AdjNode(src)
        node.next = self.graph[dest]
        self.graph[dest] = node
 
    def print_graph(self):
        for i in range(self.V):
            print("Adjacency list of vertex {}\n head".format(i), end="")
            temp = self.graph[i]
            while temp:
                print(" -> {}".format(temp.vertex), end="")
                temp = temp.next
            print(" \n")

if __name__ == "__main__":
    V = 5
    graph = Graph(V)
    graph.add_edge(0, 1)
    graph.add_edge(0, 4)
    graph.add_edge(1, 2)
    graph.add_edge(1, 3)
    graph.add_edge(1, 4)
    graph.add_edge(2, 3)
    graph.add_edge(3, 4)
 
    graph.print_graph()

# %% [markdown]
# O(n) omdat elke edge moet idividueel worden gechecked

# %% [markdown]
# # Binary Search Tree
# 
# 

# %%
class Node:
    def __init__(self, key):
        self.left = None
        self.right = None
        self.val = key

def search(root, val):
 
    if root:
        if root.val == val:
            print('found')

        if root.val > val:
            search(root.left, val)

        search(root.right, val)

root = Node(10)
root.left = Node(7)
root.right = Node(12)
root.left.left = Node(3)
root.left.right = Node(6)

search(root,0)

# %% [markdown]
# O(Logn), omdat na elke niveau de zoek ruimte gehalveerd wordt


