''' Import libraries, assign n and Pr'''

import matplotlib
import numpy
import random
import networkx as nx
import matplotlib.pyplot as plt

n = 10
p = .2

print_graph=0
create_graph_iter=0
create_graph_iter_p=1
create_graph_iter_p_n=0

''' create list of nodes from n '''
def create_node_list(n):
    nodes = list() # n
    for i in range(0,n):
        nodes.append(i)
    return(nodes)
    

''' create list of links from nodes list and Pr '''
def create_links(nodes,p):
    links = list() # k
    completed = list()
    #random.seed(a=55)
    for i in nodes:
        if completed.count(i) == 0:
            for j in nodes:
                if j > i:
                    rand = random.random()
                    if rand < p:
                        links.append((i,j))
            completed.append(i)
    return(links)

''' Print links and nodes'''
def print_nodes_links(nodes,links):
    print()
    print(nodes)
    for i in links:
        print(i)
    print()

''' Count the degrees (k) of each node'''
def count_k(nodes,links):
    k_dict = {}
    for i in nodes:
        k_dict[i] = 0
        for j in links:
            if j.count(i) >0:
                k_dict[i]+=1
#    for k,v in k_dict.items(): #uncomment to show
#        print(k,v)
    return(k_dict)

''' Calculate the average links for all nodes'''
def calc_mean_k_sub_i(k_dict):
    n=0
    k_val=0
    for k,v in k_dict.items():
        k_val+=v
        n+=1
    mean_k_sub_i = k_val/n
    return(mean_k_sub_i)

''' Create a NetworkX graph'''
def create_nx_graph(nodes,links):
    G = nx.Graph()
    G.add_nodes_from(nodes)
    G.add_edges_from(links)
    return(G)

'''Draw Graph'''
def draw_graph(G):
    nx.draw(G,with_labels=True,font_weight='bold')

'''Create histogram of distribution of degrees'''
def k_distribution(k_dict,n):
    h_dict={}
    for i in range(0,n):
        h_dict[i]=0
    for k,v in k_dict.items():
        h_dict[v]+=1
    return(h_dict)

'''Create bar chart'''
def hist_dict(dict_,string):
    plt.bar(range(len(dict_)), list(dict_.values()), width = .8,align= "center")
    plt.xticks(range(len(dict_)),list(dict_.keys()))
    plt.show() # Comment out this or plt.savefig(string)
#    plt.savefig(string) # Comment out this or plt.show()
    
''' Create and optionally display a graph'''

def create_draw_graph(n,p):
    nodes = create_node_list(n)
    links = create_links(nodes,p)
    G = create_nx_graph(nodes,links) #convert to NetworkX graph
    draw_graph(G) #display NetworkX graph
    k_dict = count_k(nodes,links)
    mean_k_sub_i = calc_mean_k_sub_i(k_dict)
#    print("Mean K_sub_i = ",mean_k_sub_i)
#    print(k_dict)
    k_dist=k_distribution(k_dict,n)
#    print(k_dist)
    return(k_dict,k_dist,links,mean_k_sub_i)


def create_graph(n,p):
    nodes = create_node_list(n)
    links = create_links(nodes,p)
#    G = create_nx_graph(nodes,links) #convert to NetworkX graph
#    draw_graph(G) #display NetworkX graph
    k_dict = count_k(nodes,links)
    mean_k_sub_i = calc_mean_k_sub_i(k_dict)
#    print("Mean K_sub_i = ",mean_k_sub_i)
#    print(k_dict)
    k_dist=k_distribution(k_dict,n)
#    print(k_dist)
    return(k_dict,k_dist,links,mean_k_sub_i)

''' Count all triangles in a graph'''
def count_triangles(links,n): #global method
    nodes = create_node_list(n)
#    print(nodes)
    triangles = 0
    lists = list()
    for edge in links:
        edge = list(edge)
        lists.append(edge)
    for node in nodes:
        temp_list = list()
        for i in lists:
            if i[0] == node:
                temp_list.append(i[1])
#        print("list of edges with iterated node: ",node)
#        print(temp_list)
#        print()
        while len(temp_list) > 0:
#            print("shortening lists")
            for x in range(1,len(temp_list)):
#                print(x)
                temp1 = [temp_list[0],temp_list[x]]
                for item in lists:
                    if item==temp1:
                        triangles+=1
#                        print("Triangle found between ",node,temp1)
#                print(temp1)
            temp_list.pop(0)
#            print(temp_list)
#    print("Triangles in graph: ",triangles)
    return(triangles)

''' Iterate over a set of parameters for graphs'''
def iterate_graph(n,p):

    sum_k_dist={}
    counter=0
    triangles = 0
    mean_k = list()
    for i in range(0,100):
        k_dict,k_dist,links,mean_k_sub_i = create_graph(n,p)
        if counter==0:
            sum_k_dist=k_dist
        elif counter > 0:
            for k,v in k_dist.items():
                sum_k_dist[k] = sum_k_dist.get(k) + v
        mean_k.append(mean_k_sub_i)
        triangles += count_triangles(links,n)
        counter+=1
#    print(sum_k_dist)
    string = ("Graph.png")
    hist_dict(sum_k_dist,string)
    sum_mean_k=0
    for i in mean_k:
        sum_mean_k += float(i)
    average_mean_k = sum_mean_k / len(mean_k)
    average_triangles = triangles / counter
    print("n: ",n)
    print("Pr: ",p)
    print("Average number of links: ",average_mean_k)
    print("Average triangles: ",average_triangles)


''' Iterate through a set of probabilities for graphs of a given size'''
def iterate_p(n):
#    n = 30
    p = .0
    r = .10
    sum_k_dist={}
    quant_proba = round(int(1/r))
#    print(quant_proba)
    for a in range(0,quant_proba):
        triangles=0
        sum_k_dist={}
        mean_k=list()
        counter=0
        for i in range(0,100):
            k_dict,k_dist,links,mean_k_sub_i = create_graph(n,p)
            mean_k.append(mean_k_sub_i)
            if counter==0:
                sum_k_dist=k_dist
            elif counter > 0:
                for k,v in k_dist.items():
                    sum_k_dist[k] = sum_k_dist.get(k) + v
            triangles += count_triangles(links,n)
            counter+=1
#        print(sum_k_dist)
#        string = ("Graph P"+str(a)+".png") #uncomment this and next line for historgrams
#        hist_dict(sum_k_dist,string)
        average_triangles = triangles / counter
        sum_mean_k=0

        for i in mean_k:
            sum_mean_k += float(i)
        average_mean_k = sum_mean_k / len(mean_k)
        print("n: ",n)
        print("P(k): ",p)
        print("<k>: ",average_mean_k)
        print("Average Triangles: ",average_triangles)
        print()
        p=p+r
        


def main(n,p,a,b,c,d):
    if a == 1:
        G=create_draw_graph(n,p)
    if b==1:
        iterate_graph(n,p)
    if c==1:
        iterate_p(n)
    if d==1:
        for i in range(1,4):
            n=i*10
            iterate_p(n)


main(n,
     p,print_graph,
     create_graph_iter,
     create_graph_iter_p,
     create_graph_iter_p_n
     )

 #%%