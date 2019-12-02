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

#JSON File
data = {}

#NODES

def get_agent():
        ag_prefix = 'a1'
        return json.dumps(data['agent'])

def get_all_activities():
    activities = data['activity']
    for activity in activities:
        ac_prefix = int(activity[5:])
        activity_i = {activity: activities[activity]}
        yield json.dumps(activity_i), ac_prefix

def extract_entity_type(node):
    string = node.split(":")
    return ''.join([i for i in string[-1] if not i.isdigit()])

#split this into data (d), library (l), environment, function (f) nodes
def get_all_entities():
    entities = data['entity']
    for entity in entities:
        # entity_id = extract_id(json.dumps(entity))
        entity_i = json.dumps({entity: entities[entity]})
        if extract_entity_type(entity) == 'd':
            entity_id = extract_id(json.dumps(entity))
            get_all_data(entity_i, entity_id)
        elif extract_entity_type(entity) == 'f': 
            entity_id = extract_id(json.dumps(entity))
            get_all_functions(entity_i, entity_id)
        elif extract_entity_type(entity) == 'l':
            entity_id = extract_id(json.dumps(entity))
            get_all_libraries(entity_i, entity_id)
        else:
            feedcamflow.node_environment(entity_i)
def get_all_data(data_node, name):
    feedcamflow.push_data_node(data_node.encode('utf-8'), name)
    
def get_all_functions(function_node, name):
    feedcamflow.push_function_node(function_node.encode('utf-8'), name)

def get_all_libraries(library_node, name):
    feedcamflow.push_library_node(library_node.encode('utf-8'), name)

#EDGES
def extract_id(node):
    string = node.split(":")
    # return int(''.join([i for i in string[-1] if i.isdigit()]))
    try:
        x = int(''.join(filter(str.isdigit, string[-1])))
        return x
    except ValueError:
        print("oops! that node did not have a numeral designator.")

def get_all_p2p():
    if 'wasInformedBy' in data:
        return get_all_edges(data['wasInformedBy'], 'prov:informant', 'prov:informed')

def get_all_p2d():
    if 'wasGeneratedBy' in data:
        return get_all_edges(data['wasGeneratedBy'], 'prov:activity', 'prov:entity')

def get_all_d2p(from_data, to_procedure):
    feedcamflow.edge_uses_data(from_data, to_procedure)

def get_all_f2p(from_function, to_procedure):
    feedcamflow.edge_uses_function(from_function, to_procedure)

def get_all_df2p():
    df2p_edges = data['used']
    for df2p in df2p_edges:
        if extract_entity_type(df2p_edges[df2p]['prov:entity']) == 'd':
            get_all_d2p(extract_id(json.dumps(df2p_edges[df2p]['prov:entity'])), extract_id(json.dumps(df2p_edges[df2p]['prov:activity'])))
        elif extract_entity_type(df2p_edges[df2p]['prov:activity']) == 'f':
            get_all_f2p(extract_id(json.dumps(df2p_edges[df2p]['prov:entity'])), extract_id(json.dumps(df2p_edges[df2p]['prov:activity'])))

def get_all_l2f():
    if 'hadMember' in data:
        return get_all_edges(data['hadMember'], 'prov:collection', 'prov:entity')
    
def get_all_edges(edge_type, from_node, to_node):
    edges = edge_type
    for edge in edges:
        edge_prefix = edge
        yield(extract_id(json.dumps(edges[edge][from_node])), extract_id(json.dumps(edges[edge][to_node])))


################################################ USER LEVEL API ################################################

disclosed_activities = {}

def import_prov(filename):
    global data
    with open(filename) as f:
        data = json.load(f)

def disclose_agent():
    feedcamflow.disclose_agent(get_agent())

def disclose_activities():
    for activity, act_id in get_all_activities():
        disclosed_activities[act_id] = feedcamflow.push_activity(activity.encode('utf-8'), act_id)
    
def disclose_entities():
    get_all_entities()

def disclose_used():
    get_all_df2p()

def disclose_generated():
    for from_activity, to_entity in get_all_p2d():
        feedcamflow.edge_generates(from_activity, to_entity)

def disclose_informed():
    for from_activity, to_activity in get_all_p2p():
        feedcamflow.edge_informs(from_activity, to_activity)

def disclose_member():
    for from_library, to_function in get_all_l2f():
        feedcamflow.edge_member(from_library, to_function)

def main():
    if len(sys.argv) < 2:
        sys.exit("Missing argument, must be of the form: python parse_prov.py <some json file>")
    if len(sys.argv) > 2:
        sys.exit("Too many arguments, must be of the form: python parse_prov.py <some json file>")
    import_prov(sys.argv[1])
    disclose_agent()
    disclose_activities()
    disclose_entities()
    # feedcamflow.printList()
    disclose_used()
    disclose_generated()
    disclose_informed()


if __name__ == "__main__":
    main()
