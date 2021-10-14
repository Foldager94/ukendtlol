import requests as req
from scrapy.http import TextResponse
import regex as re
import pandas as pd

url = 'https://www.topsoe.com/careers/available-jobs'
#url = 'https://karriere.forsvaret.dk/job/'
req = req.get(url).content
response = TextResponse(url=url, body=req)




tags_list = response.xpath('body//a')

class node:

    def __init__(self, raw_node):
        self.raw_node = raw_node
        self.node = self.get_tag(raw_node.get())
        self.node_attributes = raw_node.attrib
        self.raw_ancestors = self.find_raw_ancestors()
        self.ancestors = self.find_ancestors()
        self.siblings = list()
        self.siblings_nearest_ancestor = None
        
        
    # Getters
    
    def get_node(self):
        return self.node
    
    def get_raw_node(self):
        return self.raw_node
        
    def get_node_href(self):
        return self.node_attributes.get("href")
    
    def get_node_text(self):
        return self.raw_node.xpath("text()").get()
    
    def get_ancestors(self):
        return self.ancestors
    
    def get_sibling_nodes(self):
        return self.siblings
    
    # Finders
    
    def find_raw_ancestors(self):
        return self.raw_node.xpath('ancestor::node()').getall()
    
    def find_ancestors(self):
        ancestor_list = list()
        for raw_ancestor in self.raw_ancestors:
            ancestor = self.get_tag(raw_ancestor)
            ancestor_list.append(ancestor)
        return ancestor_list
    
    # Setters
    
    def set_sibling_nodes(self, sibling_list):
        self.siblings = sibling_list
    
    # Utils
     
    def get_tag(self, tag):
        return "<"+re.findall(r'<(.*?)>', tag)[0]+">"







def compare_ancestors(list_of_nodes):
    
    clustered_node_list = list()
    match_list = list()
    
    for index, node in enumerate(list_of_nodes):
        sibling_list = list()
        if index in match_list or "javascript" in node.get_node():
            continue
        list_node_ancestors = node.get_ancestors()
        for other_index, other_node in enumerate(list_of_nodes[index+1:]):
            if "javascript" in other_node.get_node():
                break
            list_other_node_ancotors = other_node.get_ancestors()
            if len(list_node_ancestors) == len(list_other_node_ancotors):
                match_list.append(other_index+index+1)
                sibling_list.append(other_node)
            else:
                break    
        
        if sibling_list:
            sibling_list.append(node)
            clustered_node_list.append(sibling_list)
    return clustered_node_list


def find_siblings_nearest_ancestor(list_of_nodes):
    ancestor_list = list()
    for node in list_of_nodes:
        ancestor_list.append(node.get_ancestors())
    df = pd.DataFrame(ancestor_list)
    print(df.head())

for tag in tags_list:
    lol = node(tag)
    if lol.get_node_href == 'https://topsoe.applicantpro.com/jobs/':
        print('here')
    else:
        print(lol.get_node_href())


node_list = list()

for tag in tags_list:
    node_list.append(node(tag))

cluster_fuck = compare_ancestors(node_list)
# find_siblings_nearest_ancestor(cluster_fuck[1])
# for fuck in cluster_fuck:
#     for some_node in fuck:
#         print(type(some_node))
#         some_node.set_sibling_nodes(fuck)

for index, y in enumerate(cluster_fuck):
    print(index,y)
    pass


#print(len(tags_list))


