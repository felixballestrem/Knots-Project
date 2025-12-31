class PlanarDiagram:
    def __init__(self, pd):
        """pd is a list of crossings 
        A crossing is a list of 4 arc labels ordered anti-clockwise
        assume orientation of 1st -> 3rd arc of crossing being incoming underpass"""
        self.pd = pd
        self.components = self.find_components()
        
        self._succs = {} # hash giving next arc in an oriented strand
        self._arc_comps = {} # hash giving the component an arc belongs to
        
        for comp in self.components:
            for i in range(len(comp)):
                self._succs[comp[i-1]] = comp[i]
                self._arc_comps[comp[i]] = comp
        
    
    def get_sign(self,crossing):
        # finds the crossing sign based on succession of arcs in overpass
        if self.get_arc_succ(crossing[3]) == crossing[1]:
            if self.get_arc_succ(crossing[1]) == crossing[3]:
                # special 1 component knot case
                if crossing[2] == crossing[3]:
                    return 1
                else:
                    return -1
            else:
                return 1
        
        else:
            return -1

        
    def writhe(self):
        # sums signs of all crossings
        return sum([self.get_sign(c) for c in self.pd])

    def get_arc_succ(self, arc):
        return self._succs[arc]
    
    
    def get_arc_comp(self,arc):
        return self._arc_comps[arc]

    def get_linking_number(self):
        # sums signs of all crossings that are made up of two components
        acc = 0
        for crossing in self.pd:
            if self.get_arc_comp(crossing[0]) != self.get_arc_comp(crossing[1]):
                acc += self.get_arc_sign(crossing)
        return 1/2 * acc
    
    def find_components(self):
        """Determines the components of a PD
           gives a list of tuples of (consecutively ordered) arc labels """
    
        components = []
        # hash giving consecutive arc labels of an arc in a strand in both directions
        nbrs = {}
        for c in self.pd:
            nbrs.setdefault(c[0], []).append(c[2])
            nbrs.setdefault(c[2], []).append(c[0])
        for c in self.pd:
            nbrs.setdefault(c[1], []).append(c[3])
            nbrs.setdefault(c[3], []).append(c[1])

        visited = set()
        # iterate over all arcs
        for arc in nbrs:
            if arc in visited:
                continue
            stack = [arc]
            visited.add(arc)
            knot = []
            
            # do depth-first-search on the arc to find its knot
            while stack:
                curr = stack.pop()
                knot.insert(0,curr)
                for nbr in nbrs[curr]:
                    if nbr not in visited:
                        visited.add(nbr)
                        stack.append(nbr)
            components.append(tuple(knot))

        return components