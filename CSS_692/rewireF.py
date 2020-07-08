def rewireR(G,r,ctol=10):
    import networkx as nx
    import random as rn
    from copy import deepcopy
    U=nx.Graph()
    m=G.size()
    mr=int(r*m)
    if mr%2==1 and mr<m:
        mr=mr+1
    edgelist=list(G.edges())
    rn.shuffle(edgelist)
    edgerandom=deepcopy(edgelist[:mr])
    for (i,j) in edgelist[mr:]:
        U.add_edge(i,j)
    unmatched=True
#    print m, mr, U.size(),U.size()+mr
    c=0
    while unmatched:
        pairs=[]
        paired=0
        unpaired=[]
        for mo in range(0,mr,2):
            (i1,j1)=edgerandom[mo]
            (i2,j2)=edgerandom[mo+1]
            if i1!=j2 and i2!=j1:
                pairs.append((i1,j2))
                pairs.append((i2,j1))
            else:
                unpaired.append((j1,i1))
                unpaired.append((i2,j2))
        for (i,j) in pairs:
            if not U.has_edge(i,j):
                U.add_edge(i,j)
                paired=paired+1
            else:
                unpaired.append((i,j))
#        print mr,paired,mr-paired,len(unpaired),U.size(),m-U.size()
        if paired<mr:
            c=c+1
            if c==ctol:
                print "QUITTING AT",c,"STILL UNPAIRED",mr-paired
                return(U)
            print "RESHUFFLE",c,"STILL UNPAIRED",mr-paired
            edgelist=list(U.edges())
            rn.shuffle(edgelist)
            edgerandom=deepcopy(edgelist[:mr-paired])
            for (i,j) in edgerandom:
                if U.has_edge(i,j):
                    U.remove_edge(i,j)
            edgerandom=edgerandom+unpaired
            mr=2*(mr-paired)
        else:
            unmatched=False
    return(U)
