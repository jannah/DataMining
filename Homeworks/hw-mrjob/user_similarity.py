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
    
    def calcualte_cardinality(self, user_id, biz_ids):
        biz_id = set(biz_ids)
#        print 'step 1: UNIQUE'
#        print "%s\t%s\t%s" % (user_id, len(biz_id), ", ".join(str(e) for e in biz_id))
        ids = []
        for id in biz_id:
            ids.append(id)
        yield user_id, (ids, len(biz_id))
 
    def reverse_map(self, user_id, values):
        ids, cardinality = values
#        print '%s\t%s' % (ids, cardinality)
        for id in ids:
            yield id, (user_id, cardinality)
        
    def split_reduce(self, ids, values):
#        yield "PAIRS", values
        list = []
#        print "%s\t%s" % (ids, ",".join(str(e) for e in values))
        for value in values:
            list.append(value)
#            user_id, cardinality = value
#            print "%s\t%s\t%s" % (ids, user_id, cardinality)
#        print ids
        yield "PAIRS", list
            
            
    def pair_collect_map(self, key, values):
        for user1, user2 in combinations(values,2):
            c = user1[1]+user2[1]
            yield (user1[0], user2[0], user1[1], user2[1]), c
#        user_id, cardinality = values
#        print "%s\t%s" % (user_id, cardinality)
    
    def normalize_reduce(self, ids, cardinality):
        count = 0
        cards =[]
        for card in cardinality:
            count+=1
            cards.append(card)
#            print "%s\t%s" % (count, card)
        
        jindex = count/float((cards[0]-count))
        if jindex>=0.5:
            yield  jindex, (ids[0], ids[1], ids[2], ids[3])
    
    def print_output(self, jindex, ids):
        for id in ids:
            print "%.2f\t%s" % (jindex, "\t".join(str(e) for e in id))
  
    
    def steps(self):
        """TODO: Document what you expect each mapper and reducer to produce:
        extract_businesses: <line, record> => <user_id, biz_id>
        reducer1:<user_id, [biz_ids]>               =>  <user_id,[biz_ids, c1] where c = len(biz_id)
        mapper2: <user_id,[biz_ids, c]              =>  <biz_id, [user_id, len(biz_ids)]>
        reducer2:<biz_id, [user_id, c]>             =>  <"PAIR", [user_id, len(biz_ids)]>
        mapper3: <_,[biz_ids, len(biz_ids)]         =>  <[user_id, user2_id, c1, c2], c1_2> where c1_2 = c1+c2
        reducer3:<[user_id,user2_id,c1,c2], [c1_2]> =><jindex, [user_id, user2_id, c1, c2]> where jindex = len([c1_2])/(c1_2-len([c1_2])
        reducer4:formatted output
        
        """
        return [
            self.mr(mapper=self.extract_biz_ids,reducer=self.calcualte_cardinality),
            self.mr(mapper=self.reverse_map, reducer=self.split_reduce),
            self.mr(mapper=self.pair_collect_map, reducer=self.normalize_reduce),
            self.mr(reducer=self.print_output)
#            self.mr(mapper=self.max_similarity, reducer=self.select_max),
#            self.mr(mapper=...),
        ]


if __name__ == '__main__':
    UserSimilarity.run()
