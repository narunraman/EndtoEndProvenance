

import sys
import ctypes
import json
sys.path.append('include')
import parse_prov

feedcamflow = ctypes.CDLL("./camper.so")

def import_prov(filename):
    with open(filename) as f:
        parse_prov.provenance_dict = json.load(f)

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
    for activity, act_id in parse_prov.get_all_activities():
        parse_prov.disclosed_activities[act_id] = feedcamflow.cam_activity(activity)
    
def disclose_entities():
    for entity, en_id in parse_prov.get_all_entities():
        parse_prov.disclosed_entities[en_id] = feedcamflow.cam_entity(entity)

def disclose_used():
    for from_entity, to_activity in parse_prov.get_all_df2p():
        feedcamflow.edge_uses(parse_prov.disclosed_entities[from_entity], parse_prov.disclosed_activities[to_activity])

def disclose_generated():
    for from_activity, to_entity in parse_prov.get_all_p2d():
        feedcamflow.edge_generates(parse_prov.disclosed_activities[from_activity], parse_prov.disclosed_entities[to_entity])

def disclose_informed():
    for from_activity, to_activity in parse_prov.get_all_p2p():
        feedcamflow.edge_informs(parse_prov.disclosed_activities[from_activity], parse_prov.disclosed_activities[to_activity])

def disclose_member():
    for from_library, to_function in parse_prov.get_all_l2f():
        feedcamflow.edge_member(parse_prov.disclosed_entities[from_library], parse_prov.disclosed_entities[to_function])

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
