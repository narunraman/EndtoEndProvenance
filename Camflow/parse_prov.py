# author: Narun Raman

###################################
#
# To Use:
# Call import_prov to set the global data variable
# Now can use any of the functions to extract the nodes and edges from the JSON

import json
import ctypes
import string
import sys



feedcamflow = ctypes.CDLL("./disclose2cam.so")
provenance_dict = {}
fine_grained = False

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


################################################ USER LEVEL API ################################################

disclosed_activities = {}
disclosed_entities = {}

def import_prov(filename):
    global provenance_dict
    with open(filename) as f:
        provenance_dict = json.load(f)

def set_granularity(granularity):
    if(type(granularity) == bool):
        parse_prov.fine_grained = granularity
    else:
        print("Please provide a boolean value for granularity")

def get_granularity():
    if(parse_prov.fine_grained):
        print("fine granularity")
    else:
        print("regular granularity")

def disclose_agent():
    feedcamflow.disclose_agent(get_agent().encode('utf-8'))

def disclose_activities():
    for activity, act_id in get_all_activities():
        disclosed_activities[act_id] = feedcamflow.cam_activity(activity)
    
def disclose_entities():
    for entity, en_id in get_all_entities():
        disclosed_entities[en_id] = feedcamflow.cam_entity(entity)

def disclose_used():
    for from_entity, to_activity in get_all_df2p():
        feedcamflow.edge_uses(disclosed_entities[from_entity], disclosed_activities[to_activity])

def disclose_generated():
    for from_activity, to_entity in get_all_p2d():
        feedcamflow.edge_generates(disclosed_activities[from_activity], disclosed_entities[to_entity])

def disclose_informed():
    for from_activity, to_activity in get_all_p2p():
        feedcamflow.edge_informs(disclosed_activities[from_activity], disclosed_activities[to_activity])

def disclose_member():
    for from_library, to_function in get_all_l2f():
        feedcamflow.edge_member(disclosed_entities[from_library], disclosed_entities[to_function])

def disclose_prov():
    disclose_activities()
    disclose_entities()
    disclose_used()
    disclose_generated()
    disclose_informed()

def main():
    if len(sys.argv) < 2:
        sys.exit("Missing argument, must be of the form: python parse_prov.py <some json file>")
    if len(sys.argv) > 2:
        sys.exit("Too many arguments, must be of the form: python parse_prov.py <some json file>")
    import_prov(sys.argv[1])
    # disclose_agent()
    disclose_prov()

if __name__ == "__main__":
    main()
