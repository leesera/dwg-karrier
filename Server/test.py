import graphlab
graphlab.product_key.set_product_key('D75B-9AD5-8257-3E33-E7B3-E7E6-EE34-7D86')
sf = graphlab.SFrame({'user_id': ["0", "0", "0", "1", "1", "2", "2", "2"],'item_id': ["a", "b", "c", "a", "b", "b", "c", "d"]})
m = graphlab.recommender.create(sf)
recs = m.recommend()
print dir(m)
print recs
print dir(recs)
sf.append(graphlab.SFrame({'user_id':["1"],'item_id':["d"]}))
m = graphlab.item_similarity_recommender.create(sf)
ss = m.recommend(["0"])
print ss
nn = m.get_similar_items()
print nn
