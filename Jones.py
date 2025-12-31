from sympy import symbols, simplify
from PlanarDiagram import PlanarDiagram
A,t = symbols('A t',positive = True)
def kauffman(crossings):
    if len(crossings) == 0 or (len(crossings) == 1 and len(crossings[0]) == 0):
        #trivial case
        return 1
    
    #working cross by cross
    cross = crossings[0]
    #initiallising each element of cross
    a,b,c,d = cross
    #E, F, G, H store the indices of the crossings that arcs a, b, c, d connect to, respectively.
    #If an arc forms a loop (connects back to the same crossing), the index is 0.
    connections = [0 if len(arcConnect(crossings,i)) ==1 else crossings.index(arcConnect(crossings,i)[0]) if arcConnect(crossings,i)[1] == cross else crossings.index(arcConnect(crossings,i)[1]) for i in cross]
    E,F,G,H = connections 

    smoothedA = aSmoothing(crossings,a,b,c,d,E,F,G,H)
    smoothedB = bSmoothing(crossings,a,b,c,d,E,F,G,H)
    if E==0 and F == 0 and G == 0 and H== 0:
        # if both arcs are loops
        if len(crossings)==1: #if the only component of the diagram is this
            if cross[0] == cross[1]: # if the western and eastern arcs are loops        
                return -A **3 
            else: 
                return -A**-3    # if the northern and southern arcs are loops
        else: 
            if cross[0] == cross[1]:
                return (A**5 + A)* kauffman(crossings[1:])
            else:
                return (A**-5 + A**-1)* kauffman(crossings[1:])  
    elif  (G==0 and F ==0) or (E == 0 and H == 0): # if the northern or southern arcs are loops and multiplies that term by the necessary (-A^2 -A^-2) factor          
        return simplify(kauffman(smoothedB) * (-A**1 - A**-3) + A* kauffman(smoothedA) )
    elif (G==0 and H ==0) or (E == 0 and F == 0): # if the western or eastern arcs are loops and multiplies that term by the necessary (-A^2 -A^-2) factor     
        return simplify(kauffman(smoothedA) * (-A**3 - A**-1) + (A**-1)* kauffman(smoothedB))
    else:
        return simplify(A* kauffman(smoothedA) + (A**-1)* kauffman(smoothedB))
    
def aSmoothing(originalcrossings,a,b,c,d,E,F,G,H):
    #Returns a list of crossings where the crossing [a,b,c,d] is smoothed such that connecting a (se) to b (ne) and d (sw) to c (nw)

    crossings = [crossing[:] for crossing in originalcrossings] #deep copy of originalcrossings

    if G == 0 and F == 0: #Checks if there a north loop and smooths a (se) goes to d (sw)
        h = crossings[H]
        h[h.index(d)] = a
    elif E == 0 and H == 0: #Checks if there isnt a south loop and smooths b (ne) to c (nw)
        f = crossings[F]
        f[f.index(b)] = c
    else:
        if E!= 0 or F != 0: #Checks if there is a east loop and smooths a (se) goes to b (ne)
            f = crossings[F]
            f[f.index(b)] = a
        if G != 0 or H !=0:  #Checks if there is a west loop and smooths d (sw) goes to c (nw) 
            h = crossings[H]
            h[h.index(d)] = c
    del crossings[0]
    #relabeling
    arcs = sorted({arc for crossing in crossings for arc in crossing})
    mapping = {old:new+1 for new,old in enumerate(arcs)}
    crossings = [[mapping[arc] for arc in crossing] for crossing in crossings]
    return crossings

def bSmoothing(originalcrossings,a,b,c,d,E,F,G,H):  
#Returns a list of crossings where the crossing [a,b,c,d] is smoothed such that a (se) goes to d (sw) and b (ne) to c (nw)

    crossings = [crossing[:] for crossing in originalcrossings] #deep copy of originalcrossings

    if G == 0 and H == 0: #Checks if there is a west loop and smooths a (se) goes to b (ne)
        f = crossings[F]
        f[f.index(b)] = a
    elif E == 0 and F == 0: #Checks if there is a east loop and smooths d (sw) goes to c (nw)
        g = crossings[G]
        g[g.index(c)] = d
    else:
        if G != 0 or F!= 0: #Checks if there isnt a north loop and smooths b (ne) to c (nw)
            g = crossings[G]
            g[g.index(c)] = b        
        if H !=0 or E != 0: #Checks if there isnt a south loop and smooths a (se) goes to d (sw)
            h = crossings[H]
            h[h.index(d)] = a
 
    del crossings[0]
    #relabeling
    arcs = sorted({arc for crossing in crossings for arc in crossing})
    mapping = {old:new+1 for new,old in enumerate(arcs)}
    crossings = [[mapping[arc] for arc in crossing] for crossing in crossings]
    return crossings      
def arcConnect(crossings,arc):
    #returns which crossing(s) a specific arc appears in 
    return [cross for cross in crossings if arc in cross]
def jones(pd):
    #Determines Jones polynomial from a PlanarDiagram object. Returns in terms of t.
    crossings = pd.pd
    k = simplify((-A**3)**-(pd.writhe())* kauffman(crossings))
    if len(pd.components)==1: # gives t = A^-4 for knots
        return simplify(k.subs(A**-4,t))
    else:
        return simplify(k.subs(A**-2,t)) # gives t = A^-2 for links


def Poly(pd):
    PD = PlanarDiagram(pd)
    print("Jones polynomial: ", jones(PD))
    return jones(PD)





pd1 = [[8,3,1,4],[4,1,5,2],[2,7,3,8],[6,6,7,5]]
pd2 = [[4,1,5,2],[2,5,3,6],[6,3,1,4]]
pd3 = []

pds = [pd1, pd2, pd3]

for each in pds:
    Poly(each)