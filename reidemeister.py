#   -----------------------------------------------------------------------------------------------------------
#   ===========================================================================================================

#   ===========================================================================================================
# Reidemeister moves
#   ===========================================================================================================
class knot:
    def __init__(self, crossings):
        self.crossings = [list(c) for c in crossings]
        print("Knot created with crossings:\n", self.crossings)
    
    # Helper functions
    def arcs(self):
        return [a for c in self.crossings for a in c] # list of all arcs in the knot

    def adjacent(self, c, a, b):
        i, j = c.index(a), c.index(b)
        return (i - j) % 4 in (1, 3)

    def same_strand(self, c, a, b):
        i, j = c.index(a), c.index(b)
        return (i - j) % 4 == 2
    
    def counts(self, crossings):
        c = []
        for cross in crossings:
            try:
                c.extend(cross)
            except TypeError:
                c.append(cross)
        counts = {a: c.count(a) for a in c} # number:count
        # print(counts)
        return counts
    
    def wrap(self, s):
        N = max(self.arcs())
        return (s - 1) % N + 1


    # def crossing_sign(self, c):
    #     # consistent PD convention
    #     return 1 if (c[0], c[2]) != (c[1], c[3]) else -1

#   -----------------------------------------------------------------------------------------------------------
#   ## Reidemeister 1:
#   -----------------------------------------------------------------------------------------------------------
    # detection:
    def find_R1(self):
        for i, c in enumerate(self.crossings):
            counts = {a: c.count(a) for a in c}
            if len(sorted(counts.values())) < 4: # == [1,1,2]: # If one of the arcs appears twice
                print("R1 Move found at crossing index:", i, "\n")
                return i
        return None

    # solving:
    def R1(self, idx=find_R1):
        if idx is None:
            raise ValueError("No R1 Move found to apply.")

        c = self.crossings[idx] # The crossing to be removed
        # identify loop arc
        loop = None
        for place in c:
            if c.count(place) == 2:
                loop = place
                break
        if loop is None:
            raise ValueError("No loop arc found at the specified crossing index.")

        # identify arc to connect
        print("Crossing to be removed:", c)
        splice = [place for place in c if place != loop]
        print("To splice: ", splice)

        # remove crossing
        self.crossings.pop(idx)

        # reconnect arcs by changing one part of the spice to the other
        for i, crossing in enumerate(self.crossings):
            for j in range(4):
                if crossing[j] == splice[1]:
                    print("Connecting arc", splice[0], "with arc", splice[1], "in crossing index", i, "at position", j)
                    self.crossings[i][j] = splice[0] 
        
        # relabel arcs to simplify
        arcs = sorted({arc for crossing in self.crossings for arc in crossing})
        mapping = {old:new+1 for new,old in enumerate(arcs)}
        self.crossings = [[mapping[arc] for arc in crossing] for crossing in self.crossings]
        print("R1 applied. New PD:\n", self.crossings)

        # check that the move was successful
        if (find := self.find_R1()) is not None:
            raise ValueError("R1 Move was not successful; the same move can still be applied.")
        else:
            return True


#   -----------------------------------------------------------------------------------------------------------
#   ## Reidemeister 2:
#   -----------------------------------------------------------------------------------------------------------
    # detection:
    def find_R2(self):
        print("\nSearching for R2 Moves")
        n = len(self.crossings) # number of crossings

        # check all adjacent pairs of crossings
        for i in self.crossings:
            print("\nCrossing:", i)
            for j in self.crossings:
                # check if they share an over/under arc (are adjacent and suitable for R2)
                over_arcs_i = [i[1], i[3]] # over arcs of crossing i
                over_arcs_j = [j[1], j[3]] # over arcs of crossing j
                under_arcs_i = [i[0], i[2]] # under arcs of crossing i
                under_arcs_j = [j[0], j[2]] # under arcs of crossing j
                shared_over = set(over_arcs_i).intersection(set(over_arcs_j))
                shared_under = set(under_arcs_i).intersection(set(under_arcs_j))
                
                if i == j:
                    continue
                elif shared_over != set() and shared_under != set():
                    print("Comparing with crossing:", j)
                    
                    print("Shared over arcs:", shared_over)
                    print("Shared under arcs:", shared_under)
                    
                    # i and j are adjacent and share an over/under arc
                    print("Adjacent crossings R2 move found:", i, "and", j, "\n")
                    idx1 = self.crossings.index(i)
                    idx2 = self.crossings.index(j)
                    return (idx1, idx2)
                else:
                    print("Comparing with crossing:", j)
        return None

    # solving:
    def R2(self, idx=find_R2):
        c1 = self.crossings[idx[0]]
        c2 = self.crossings[idx[1]]
        print("Performing Reidemeister Move 2 between crossings:", c1, "and", c2)
        # Implementation of Reidemeister Move 2
        #assign pairs and splice
        pairs = []
        splice_c1 = {}
        splice_c2 = {}
        for place1 in c1:
            if place1 in c2:
                pairs.append(place1)
            else:
                splice_c1[c1.index(place1)%2] = place1 # even index = under, odd index = over
        for place2 in c2:
            if place2 not in c1:
                splice_c2[c2.index(place2)%2] = place2
        print("Pairs to be removed:", pairs)
        # print("To splice from crossing 1:", splice_c1)
        # print("To splice from crossing 2:", splice_c2)

        # remove crossings
        self.crossings.pop(max(idx))
        self.crossings.pop(min(idx))
        # print("Crossings removed. Current PD:\n", self.crossings)

        # reconnect arcs by changing one part of the spice to the other
        splice1 = [splice_c1[0], splice_c2[0]]
        splice2 = [splice_c1[1], splice_c2[1]]
        print("Splice 1 (under):", splice1)
        print("Splice 2 (over):", splice2, "\n")

        for i, crossing in enumerate(self.crossings):
            for j in range(4):
                if crossing[j] == splice1[1]:
                    print("Connecting arc", splice1[0], "with arc", splice1[1])
                    self.crossings[i][j] = splice1[0] 
                elif crossing[j] == splice2[1]:
                    print("Connecting arc", splice2[0], "with arc", splice2[1])
                    self.crossings[i][j] = splice2[0]
        # print("New PD before relabeling:\n", self.crossings)

        # relabel arcs to simplify
        arcs = sorted({arc for crossing in self.crossings for arc in crossing})
        mapping = {old:new+1 for new,old in enumerate(arcs)}
        self.crossings = [[mapping[arc] for arc in crossing] for crossing in self.crossings]
        print("R2 applied. New PD:\n", self.crossings)

        # check that the move was successful
        if (find := self.find_R2()) is not None:
            raise ValueError("R2 Move was not successful; the same move can still be applied.")
        else:
            return True
        return True


#   -----------------------------------------------------------------------------------------------------------
#   ## Reidemeister 3:
#   -----------------------------------------------------------------------------------------------------------
    # detection:
    def find_R3(self, counts=counts):
        print("Searching for Reidemeister Move 3")

        # check all triplets of crossings
        # check adjacency
        adjacent_list = []
        seen = set()
        cross_copy = self.crossings.copy()
        for i in (cross_copy): # make a copy to modify to remove used crossings
            # print("\nCrossing:", i)
            for j in (cross_copy):
                if i == j:
                    continue
                for k in (cross_copy):
                    if k == i or k == j:
                        continue
                    # print("Comparing with crossing:", j, "and crossing:", k)
                    
                    crossings_triplet = [i, j, k]
                    #compare two at a time:
                    cross_1_2 = [crossings_triplet[0], crossings_triplet[1]]
                    cross_2_3 = [crossings_triplet[1], crossings_triplet[2]]
                    cross_1_3 = [crossings_triplet[0], crossings_triplet[2]]

                    if 2 in [c for c in counts(self, cross_1_2).values()] and 2 in [c for c in counts(self, cross_2_3).values()] and 2 in [c for c in counts(self, cross_1_3).values()] and 2 in [c for c in counts(self, cross_1_3).values()]:
                        # print("Crossings are all adjacent.")
                        key = frozenset(tuple(x) for x in crossings_triplet)
                        if key not in seen:
                            seen.add(key)
                            adjacent_list.append(crossings_triplet)
        
        print("\nAdjacent crossing triplets found:")
        print(*adjacent_list, sep="\n")

        # check R3 configuration for each adjacent triplet
        R3_list = []
        for triplet in adjacent_list:
            i, j, k = triplet
            # check one strand goes over the other strands
            over_strands = []
            under_strands = []
            for cross in triplet:
                # used extend to get rid of embedded lists
                over_strands.extend([cross[1], cross[3]]) # over strand is at index 1 and 3
                under_strands.extend([cross[0], cross[2]]) # under strand is at index 0 and 2
            # print("\nOver strands:", over_strands)
            # print("Under strands:", under_strands)
            
            # check if there are three in a row over and three in a row under for R3 move
            over, under = False, False
            for s in set(over_strands):
                s1 = self.wrap(s + 1)
                s2 = self.wrap(s + 2)
                if over_strands.count(s1) > 1 and over_strands.count(s2) > 0:
                    over = True
            for s in set(under_strands):
                s1 = self.wrap(s + 1)
                s2 = self.wrap(s + 2)
                if under_strands.count(s1) > 1 and under_strands.count(s2) > 0:
                    under = True
            if over and under:
                # print("\nR3 configuration found with crossings:", i, ",", j, "and", k)
                # crossing indexes
                idx1 = self.crossings.index(i)
                idx2 = self.crossings.index(j)
                idx3 = self.crossings.index(k)
                triplet = [idx1, idx2, idx3]
                R3_list.append(triplet)
            else:
                None
                # print("No R3 configuration with crossings:", i, ",", j, "and", k)
                
        if R3_list != []:
            print("\nR3 Moves found at crossing indexes:")
            print(*R3_list, sep="\n")
            print("With crossings:", *[[self.crossings[i] for i in c] for c in R3_list], sep="\n")
        else:
            print("No R3 moves found")
        return R3_list if (R3_list != []) else None
        
    # solving:
    def R3(self, idx=find_R3):
        print("\nPerforming Reidemeister Move 3")
        # Implementation of Reidemeister Move 3
        for triplet in idx:
            c1 = self.crossings[triplet[0]]
            c2 = self.crossings[triplet[1]]
            c3 = self.crossings[triplet[2]]
            print("\nApplying R3 Move to crossings:", c1, ",", c2, "and", c3)
            
            strands_over = []
            strands_under = []
            for cross in [c1, c2, c3]:
                strands_over.extend([cross[1], cross[3]]) # used extend to get rid of embedded lists
                strands_under.extend([cross[0], cross[2]])
            # print("Over strands:", strands_over)
            # print("Under strands:", strands_under)    
            # get rid of duplicates
            strands_over = list(set(strands_over))
            strands_under = list(set(strands_under))
            # print("Unique over strands:", strands_over)
            # print("Unique under strands:", strands_under)
            
            # seperate strands 
            for each in strands_over:
                s1 = self.wrap(each + 1)
                s2 = self.wrap(each + 2)
                if s1 in strands_over and s2 in strands_over:
                    strand1 = (each, s1, s2)
            for each in strands_under:
                s1 = self.wrap(each + 1)
                s2 = self.wrap(each + 2)
                if s1 in strands_under and s2 in strands_under:
                    strand2 = (each, s1, s2)
            strands = set(strands_over + strands_under)
            # print("Strands involved in R3 move:", strands)
            strand3 = tuple(set(strands) - set(strand1) - set(strand2))
            
            print("First(Over) strand involved in R3 move: A = ", strand1)
            print("Second(Over-Under) strand involved in R3 move: B = ", strand3)
            print("Third(Under) strand involved in R3 move: C = ", strand2)
            
            ## Implementation of R3 moves on the PD:
            
            # works for under bottom going left, both going up:
            if False:
                A = strand1
                B = strand3
                C = strand2

                # Crossings
                A_C = [B[0], A[1], B[1], A[0]] # A over C
                A_B = [C[0], A[2], C[1], A[1]] # A over B
                B_C = [C[1], B[2], C[2], B[1]] # B over C
                
                print(A_C)
                print(A_B)
                print(B_C)
            
            # works for under bottom going right, both going up
            elif False:
                A = strand1
                B = strand3
                C = strand2

                # Crossings
                A_C = [C[1], A[1], C[2], A[0]] # A over C
                A_B = [B[1], A[2], B[2], A[1]] # A over B
                B_C = [C[0], B[1], C[1], B[0]] # B over C
                
                print(A_C)
                print(A_B)
                print(B_C)

            # works for under bottom going right, both going down
            elif True:
                A = strand1
                B = strand3
                C = strand2
                
                # Crossings
                A_C = [C[1], A[1], C[2], A[0]] # A over C
                A_B = [B[2], A[1], B[1], A[2]] # A over B
                B_C = [C[0], B[1], C[1], B[0]] # B over C
                            
                print(A_C)
                print(A_B)
                print(B_C)
                
            # works for under bottom going left, both going down:
            elif False:
                A = strand1
                B = strand3
                C = strand2

                # Crossings
                A_C = [B[1], A[0], B[0], A[1]] # A over C
                A_B = [C[0], A[2], C[1], A[1]] # A over B
                B_C = [C[2], B[1], C[1], B[2]] # B over C
                
                print(A_C)
                print(A_B)
                print(B_C)







# computing it on a test PD

PD_test_rand = [[1, 6, 2, 5], [3, 8, 4, 7], [5, 2, 6, 1], [7, 4, 8, 3]]
PD_test_t = [[1,5,2,4],[3,1,4,6],[5,3,6,2]]
PD_test_R1 = [[8,3,1,4],[6,6,7,5],[4,1,5,2],[2,7,3,8]]
PD_test_R2 = [[10,3,1,4],[5,9,6,8],[9,5,10,4],[1,7,2,6],[7,3,8,2]]
PD_test_R3 = [[4,2,5,1],[7,3,8,2],[8,6,1,5],[3,7,4,6]]

PD = PD_test_R3

# print("_"*50, "\n")
# K = knot(PD)
# print("_"*50, "\n")

# print("-"*50)
# print("R1 Test:")
# print("-"*50)
# while True:
#     find = K.find_R1()
#     if find is None:
#         break
#     K.R1(find)
# print("\nNo more R1 Moves found.\n")
# print("_"*50)
# print("\n")

# print("-"*50)
# print("R2 Test:")
# print("-"*50)
# while True:
#     find = K.find_R2()
#     if find is None:
#         break
#     K.R2(find)
# print("\nNo more R2 Moves found.\n")
# print("_"*50)
# print("\n")

# print("-"*50)
# print("R3 Test:")
# print("-"*50)
# find = K.find_R3()
# if find is not None:
#     K.R3(find)
# print("\nNo more R3 Moves found.\n")
# print("_"*50)
# print("\n")

PD1 = [[4,2,5,1],[8,6,1,5],[3,7,4,6]]
PD2 = [[5,1,4,2],[8,6,1,5],[4,6,3,7]]
PD3 = [[5,1,4,2],[1,5,8,6],[4,6,3,7]]
PD4 = [[4,2,5,1],[1,5,8,6],[3,7,4,6]]

PD = PD2
K = knot(PD)

print("R3 test:")
K.R3(K.find_R3())
