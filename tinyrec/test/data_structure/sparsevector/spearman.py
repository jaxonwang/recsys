from main.data_structure import sparseVector 


'''
a = sparseVector.SparseVector([1,2,3,4,5,6,7,8,9,10],[4,3,2,4,4,2,3,1,2,3],14)
b = sparseVector.SparseVector([1,2,3,4,5,6,7,8,9,10],[4,3,2,4,5,2,3,1,1,3],14)
print sparseVector.spearman(a,b,False)
print sparseVector.cosine(a,b,False)
print sparseVector.pearsonr_hasvalue_both(a,b,False)
print sparseVector.pearsonr(a,b,False)
'''
a = sparseVector.SparseVector([1,2,3,4,5,6,7,8,9,10],[1,2,3,4,5,6,7,8,9,10],11)
b = sparseVector.SparseVector([1,2,3,4,5,6,7,8,9,10],[4,3,2,4,5,2,3,1,1,3],11)
print sparseVector.spearman(a,b,False)
print sparseVector.cosine(a,b,False)
print sparseVector.pearsonr_hasvalue_both(a,b,False)
print sparseVector.pearsonr(a,b,False)
