
from main.data_structure import sparseVector as vector

a = vector.SparseVector([1,2,3],[8,9,10],4)
b = vector.SparseVector([1,2,3],[8,9,10],4)
print vector.cosine(a,b)

a = vector.SparseVector([1,2,3],[1,0,1],5)
b = vector.SparseVector([1,2,3],[0,1,0],5)
print vector.cosine(a,b)
