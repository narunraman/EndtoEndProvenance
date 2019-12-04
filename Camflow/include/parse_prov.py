# author: Narun Raman

###################################
#
# To Use:
# Call import_prov to set the global data variable
# Now can use any of the functions to extract the nodes and edges from the JSON

import json
import string
import sys


provenance_dict = {}
fine_grained = False
disclosed_activities = {}
disclosed_entities = {}
####### HELPER FUNCTIONS ####### 

def extract_id(node):
    return json.dumps(node).split(":")[-1][:-1]


############# NODES ############

def get_agent():
    return json.dumps(provenance_dict['agent'])[1:-1]

def get_all_activities():
    activities = provenance_dict['activity']
    for key, value in activities.items():
        activity = ""
        act_id = extract_id(key)
        if(not fine_grained):
            activity = json.dumps([val for key, val in value.items() if 'name' in key.lower()][0])
        else:
            activity = json.dumps(key) + ":" + json.dumps(value)
        yield ("\"prov:label\":" + activity).encode('utf-8'), act_id

def get_all_entities():
    entities = provenance_dict['entity']
    for key, value in entities.items():
        entity = ""
        en_id = extract_id(key)
        if(not fine_grained):
            entity = json.dumps([val for key, val in value.items() if 'name' in key.lower()][0])
        else:
            entity = json.dumps(key) + ":" + json.dumps(value)
        yield ("\"prov:label\":" + entity).encode('utf-8'), en_id


############ EDGES ############

def get_all_p2p():
    if 'wasInformedBy' in provenance_dict:
        return get_all_edges(provenance_dict['wasInformedBy'], 'prov:informant', 'prov:informed')

def get_all_p2d():
    if 'wasGeneratedBy' in provenance_dict:
        return get_all_edges(provenance_dict['wasGeneratedBy'], 'prov:activity', 'prov:entity')

def get_all_df2p():
    if 'used' in provenance_dict:
        return get_all_edges(provenance_dict['used'], 'prov:entity', 'prov:activity')

def get_all_l2f():
    if 'hadMember' in provenance_dict:
        return get_all_edges(provenance_dict['hadMember'], 'prov:collection', 'prov:entity')
    
def get_all_edges(edge_type, from_node, to_node):
    edges = edge_type
    for edge in edges:
        edge_prefix = edge
        yield(extract_id(edges[edge][from_node]), extract_id(edges[edge][to_node]))


