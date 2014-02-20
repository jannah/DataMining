from mrjob.job import MRJob
from mrjob.protocol import JSONValueProtocol
try:
    from itertools import combinations
except ImportError:
    from metrics import combinations

def compute_jaccard_index(set_1, set_2):
        n = len(set_1.intersection(set_2))
        return n / float(len(set_1) + len(set_2) - n) 
class UserSimilarity(MRJob):
    INPUT_PROTOCOL = JSONValueProtocol

    ###
    # TODO: write the functions needed to
    # 1) find potential matches,
    # 2) calculate the Jaccard between users, with a user defined as a set of
    # reviewed businesses
    ##/
    
   
    
    def extract_biz_ids(self, _, record):
         if record['type'] == 'review':
#            print "%s\t%s" % (record['user_id'], record['business_id'])
            yield (record['user_id'], record['business_id'])
    
    def unique_biz_ids(self, user_id, biz_ids):
        biz_id = set(biz_ids)
#        print 'step 1: UNIQUE'
#        print "%s\t%s\t%s" % (user_id, len(biz_id), ", ".join(str(e) for e in biz_id))
        ids = []
        for id in biz_id:
            ids.append(id)
        yield None, [user_id, ids]
 
        
    def calculate_similarity(self, user_id, values):
#        print "%s" % values
#        print "%s\t%s" % (user_id, ", ".join(str(e) for e in biz_id))
#        for value in values:
#            user_id, biz_ids = value
#            print "%s\t%s" % (user_id, biz_ids)
        for user1, user2 in combinations(values,2):
#            print "%s\t%s" % (user1[0], user2[0])
            user1set = set(user1[1])
            user2set = set(user2[1])
            similarity = compute_jaccard_index(user1set, user2set)
#            if similarity>0:
#                print "%s\t%s\t%.2f\t%s\t%s" % (user1[0], user2[0], similarity, len(user1set), len(user2set))
            if similarity>=0.5:
#                print similarity
                yield user1[0], (similarity, user2[0], len(user1set), len(user2set))
        
        
    def max_similarity(self, user_id, values):
#        print user_id
        similarity, user2, user1size, user2size = values
        yield ["MAX", [similarity, (user_id, user2, user1size, user2size)]]
 
    def select_max(self, user_id, values):
        temp = []
        for value in values:
            temp.append(value)
            similarity, [user1, user2, user1size, user2size] = value
#            if similarity <1.00 and similarity>=0.20:
            print "%.2f\t%s\t%s\t%s\t%s" % (similarity, user1, user2,user1size, user2size)
        yield max(temp)
        
   
    
    def steps(self):
        """TODO: Document what you expect each mapper and reducer to produce:

        extract_businesses: <line, record> => <user_id, biz_id>
        reducer1:<user_id, [biz_ids]> => <user_id,[biz_ids]> UNIQUE
        reducer2: <user_id, [biz_ids]> => <[user_id, user2_id], [biz_ids], [biz2_ids]>
        mapper3:<[[user_id, user2_id]], [[biz_ids], [biz2_ids]]> => <similarity, [user_id, user2_id]>
        
        """
        return [
            self.mr(mapper=self.extract_biz_ids,reducer=self.unique_biz_ids),
#            self.mr(mapper=self.build_user_maps),
            self.mr(reducer=self.calculate_similarity),
            self.mr(mapper=self.max_similarity, reducer=self.select_max),
#            self.mr(mapper=...),
        ]


if __name__ == '__main__':
    UserSimilarity.run()
