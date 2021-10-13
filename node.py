import requests as req
from scrapy.http import TextResponse
from scrapy.http.response import text
import regex as re

url = 'https://www.topsoe.com/careers/available-jobs'
#url = 'https://karriere.forsvaret.dk/job/'
req = req.get(url).content
response = TextResponse(url=url, body=req)




tags_list = response.xpath('body//a')
tags_ancestor_list = response.xpath('//a/ancestor::node()').getall()

class node:

    def __init__(self, node, raw_node, ancestor):
        self.node = node
        self.raw_node = raw_node
        self.ancestor = ancestor
        self.node_attributes = raw_node.attrib

    def get_node(self):
        return self.node
    
    def get_ancestor(self):
        return self.ancestor

    def get_node_attributes(self):
        return self.node_attributes.get("href")


def get_tag(ancestor):
    return "<"+re.findall(r'<(.*?)>', ancestor)[0]+">"

def compare_ancestors(list_of_nodes):
    clustered_node_list = list()
    match_list = list()
    for index, node in enumerate(list_of_nodes):
        some_list = list()
        if index in match_list or "javascript" in node.get_node():
            continue
        list_node_ancestors = node.get_ancestor()
        for other_index, other_node in enumerate(list_of_nodes[index+1:]):
            if "javascript" in other_node.get_node():
                break
            list_other_node_ancotors = other_node.get_ancestor()
            if len(list_node_ancestors) == len(list_other_node_ancotors):
                match_list.append(other_index+index+1)
                some_list.append(other_node)
                #print(other_index+index+1)
                #print(index,f"OG Node:{len(list_node_ancestors)}",node.get_node(),"---",index+other_index,f"other node {len(list_other_node_ancotors)}:", other_node.get_node() )
            else:
                some_list.append(node)
                break
        if some_list:
            clustered_node_list.append(some_list)
    return clustered_node_list





node_list = list()

for tag in tags_list:
    node_tag = get_tag(tag.get())
    raw_ancestors   = tag.xpath('ancestor::node()').getall()
    clean_ancestors = list()

    for ancestor in raw_ancestors:
        clean_ancestors.append(get_tag(ancestor))

    node_list.append(node(node_tag, tag, clean_ancestors)) 

x = compare_ancestors(node_list)

for index, y in enumerate(x):
    print(index,y)

#print(len(tags_list))
