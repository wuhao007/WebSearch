from __future__ import division
import operator


def buildgraph():
    adj_list = {} # this is the graph structure.
    user_list = []
    venue_list = []

    f = open("check_in_data", "r")
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
	


def bfs_whole_tree(graph, start):
    queue = []
    visited = {}
    results = {}
    #count = 1
    queue.insert(0,[start,0])

    visited[start] = 1 # mark the first node as visited

    while queue:

        node_to_explore = queue.pop()
        results[node_to_explore[0]] = node_to_explore[1]
        #print node_to_explore
        #count = count+1
        for link in graph[node_to_explore[0]]:
            if link in visited:
                #ignore
                pass
            else:
                visited[link] = 1
                level = node_to_explore[1]+1
                queue.insert(0,[link,level])
    return results




# def bfs(graph, start, end):
#     queue = []
#     visited = {}
#     #count = 1
#     queue.insert(0,[start,0])
#     visited[start] = 1 # mark the first node as visited

#     while queue != None:
        
#         node_to_explore = queue.pop()
#         #print node_to_explore
#         #count = count+1
#         for link in graph[node_to_explore[0]]:
#             if link == end:
#                 level = node_to_explore[1]+1
#                 return level
#             if link in visited:
#                 #ignore
#                 pass
#             else:
#                 level = node_to_explore[1]+1
#                 queue.insert(0,[link,level])
        
#     return 10000000000



def run(user, graph, venue_list):
    
    dic_all_path = [] #this list will contain all the potential path along with the scores.
    results = bfs_whole_tree(graph,user)
    for venueid in venue_list:
        if venueid not in results:
            continue
        score = results[venueid]
        if score <=2:
            continue
        dic_all_path.append([user,venueid,score])
    # sorted_result = sorted(dic_all_path.iteritems(),key=operator.itemgetter(1))
    dic_all_path.sort(key=operator.itemgetter(2))
    print dic_all_path







def run_testing(user, graph, venue_list):

    all_links_len = len(graph[user])
    if all_links_len%2 == 1:
        traning_len = int(all_links_len/2)+1
    else:
        traning_len = int(all_links_len/2)


    testing_data = [] # this data is for check whether the results are right

    for i in range(traning_len):
        testing_data.append(graph[user].pop())


    # print "now the following link should be the same"
    # print testing_data
    # print graph[user]

    dic_all_path = [] #this list will contain all the potential path along with the scores.
    results = bfs_whole_tree(graph,user)
    for venueid in venue_list:
        if venueid not in results:
            continue
        score = results[venueid]
        if score <=2:
            continue
        dic_all_path.append([user,venueid,score])
    # sorted_result = sorted(dic_all_path.iteritems(),key=operator.itemgetter(1))
    dic_all_path.sort(key=operator.itemgetter(2))
    # print dic_all_path
    right_count = 0 # this counts the true positive results

    # print dic_all_path
    for path in dic_all_path:
        if path[1] in testing_data:
            right_count += 1

    precision = right_count/traning_len
    recall = right_count/all_links_len
    # print recall
    # print precision
    return recall, precision



graph,user_list,venue_list = buildgraph()

total_recall = 0
total_precision = 0


for uid in user_list:
    recall, precision = run_testing(uid, graph,venue_list)
    total_recall+=recall
    total_precision += precision


print total_recall
print total_precision

print total_recall/len(user_list)
print total_precision/len(user_list)
# def run_testing(user, graph, venue_list):
#     #use some of the data as traning data.#
#     testing_data = []

#     total = len(graph[user])
#     traning_len = total/2
#     test_data_len = total-traning_len
#     testing_data.append(graph[user].pop())
    
#     print testing_data


#     #####################################
#     dic_all_path = [] #this list will contain all the potential path along with the scores.

#     for venueid in venue_list:
#         score = bfs(graph, user, venueid)
#         if score <=2:
#             continue
#         dic_all_path.append([user,venueid,score])
#     # sorted_result = sorted(dic_all_path.iteritems(),key=operator.itemgetter(1))
#     dic_all_path.sort(key=operator.itemgetter(2))
#     print dic_all_path

#     precision_count = 0

#     for path in dic_all_path:
#         if path[1] in testing_data:
#             precision_count += 1
#     precision = precision_count/len(dic_all_path)
#     recall = precision_count/test_data_len
#     print recall
#     print precision



#graph,user_list,venue_list = buildgraph()

#run_testing("1619051", graph, venue_list)
#print bfs(graph, "wei", "4")






































