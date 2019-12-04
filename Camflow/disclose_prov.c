#include "provenance.h"
#include <fcntl.h>
#include <unistd.h>
#include <errno.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

//Will continuously get called from Python for each node
//creating a linked list for the edges to search through and use

void node_agent(char* node) {
	disclose_agent(node);
}

/* Discloses activity and pushes the activity_t onto a linked list
 * 
 */
activity_t cam_activity(char* node, int id) {
	return disclose_activity(node);
}

entity_t cam_entity(char* node, int id){
	return disclose_entity(node);
}

void edge_uses(entity_t from, activity_t to) {
	disclose_uses(from, to);
}


void edge_generates(activity_t from, entity_t to) {
	disclose_generates(from, to);
}

void edge_informs(activity_t from, activity_t to) {
	disclose_informs(from, to);
}
