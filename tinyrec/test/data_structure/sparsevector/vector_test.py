from main.data_structure import vector
from main.data_structure import sparseVector
a = vector.SparseVector([1,2,3],[1.1,17,1.2],14)
b = vector.SparseVector([1,2,3],[1.2,1.4,1.3],14)
print a,b
print vector.pearsonr(a,b,False)
print vector.pearsonr(a,b,True)

a = sparseVector.SparseVector([1,2,3],[1.1,17,1.2],14)
b = sparseVector.SparseVector([1,2,3],[1.2,1.4,1.3],14)
print a,b
print sparseVector.pearsonr(a,b,False)
print sparseVector.pearsonr(a,b,True)


a = sparseVector.SparseVector([1,2,3],[4,4,5],4)
b = sparseVector.SparseVector([1,2,3],[4,4,5],4)
print a,b
print sparseVector.pearsonr(a,b,True)

