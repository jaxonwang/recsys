import main.core.CFpredictor as prd
dao = prd.new_DAO_interface()
print prd.item_based_predict_by_knn(dao,806,421)
