import vector
a = vector.SparseVector([1,2,3],[1.1,1.3,1.2],14)
b = vector.SparseVector([1,2,3],[1.2,1.4,1.3],14)
print a,b
print vector.pearsonr(a,b)

