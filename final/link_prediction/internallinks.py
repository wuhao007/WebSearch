from __future__ import division
import operator


def buildgraph():
    adj_list = {} # this is the graph structure.
    user_list = []
    venue_list = []

    f = open("checkin", "r")
    line = f.readline() #ignore the first line
    for line in f:
        line = line.split()
        if line[0] in user_list:
            pass
        else:
            user_list.append(line[0])

        if line[1] in venue_list:
            pass
        else:
            venue_list.append(line[1])
		
        if(line[0] in adj_list):
			adj_list[line[0]].append(line[1])
        else:
			adj_list[line[0]] = []
			adj_list[line[0]].append(line[1])

        if(line[1] in adj_list):
			adj_list[line[1]].append(line[0])
        else:
			adj_list[line[1]] = []
			adj_list[line[1]].append(line[0])
    #print adj_list
    
    return adj_list, user_list, venue_list



def main():
    adj_list, user_list, venue_list = buildgraph()
    Pgraph,score_list = createPgraph(adj_list,user_list,venue_list)
    internal_links = internallinks(user_list,venue_list,adj_list,Pgraph)

    #print internal_links
    result_list = []

    for node1 in internal_links:
        if node1 in user_list:
            node2 = internal_links[node1]
            score = score_internal_link(score_list,(node1,node2[0]),adj_list)
            result_list.append([node1,node2,score])
    result_list.sort(key=operator.itemgetter(2))

    print result_list




# this will score one link at a time
def score_internal_link(score_list,link,adj_list):
    place = link[1]
    user = link[0]
    score_total = 0

    for u in adj_list[place]:
        if u != user:
            score_total = score_total+ score(u,user,adj_list,score_list)

    return score_total


def addedge(graph, u, v):
    if u in graph:
        if v in graph[u]:
            pass
        else:
            graph[u].append(v)
    else:
        graph[u] = []
        graph[u].append(v)
    if v in graph:
        if u in graph[v]:
            pass
        else:
            graph[v].append(u)

    else:
        graph[v] = []
        graph[v].append(u)

# a function that helps to compute the score

def score(u1,u2,adj_list,score_list):
    score = len(set(adj_list[u1]) & set(adj_list[u2]))
    if u1 > u2:
        temp = u1
        u1 = u2
        u2 = temp
    score_list[(u1,u2)] = score

    return score


# this function is to get the projection graph
def createPgraph(adj_list,user_list,venue_list):
    Pgraph = {}
    score_list = {}
    for u1 in user_list:
        for p in adj_list[u1]:
            for u2 in adj_list[p]:
                if u2 != u1:
                    addedge(Pgraph,u1,u2)
                    score(u1,u2,adj_list,score_list)
    return Pgraph, score_list







# identifying the internal links
def internallinks(user_list,venue_list,adj_list,Pgraph):
    internal_links = {}
    for u in user_list:
        for p in venue_list:
            if p not in adj_list[u]:
                internal = True
                for user_p in adj_list[p]:
                    if user_p not in Pgraph[u]:
                        internal = False
                        break
                if internal:
                    addedge(internal_links,u,p)
    return internal_links




main()







































































