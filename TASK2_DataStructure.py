# Adjacency Matrix that represent how many people is living in the same building.
def add_name(mat,i,j):
    mat[i][j] = 1
    mat[j][i] = 1

def display_mat(mat):
    for n in mat:
        print(" ".join(map(str , n)))

# people living in the same building or not
V = 5
mat = [[0] * V for _ in range(V)]

add_name(mat, 0 ,1)
add_name(mat, 0 ,2)
add_name(mat, 1 ,2)
add_name(mat, 2 ,3)
add_name(mat, 1 ,4)

print("Adjacency Matrix of the result:")
display_mat(mat)

# Adjacency List 
def add_listname(adj, i ,j):
    adj[i].append(j)
    adj[j].append(i)

def display_list(adj):
    for n in range(len(adj)):
        print(n , ": " , end="")
        for i in adj[n]:
            print(i, end=" ")
        print()

V = 5
adj = [[] for _ in range(V)]

add_listname(adj, 0 ,1)
add_listname(adj, 0 ,2)
add_listname(adj, 1 ,2)
add_listname(adj, 2 ,3)
add_listname(adj, 1 ,4)

print("Adjacency List of the result: ")
display_list(adj)
