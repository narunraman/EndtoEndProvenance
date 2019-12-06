#include "provenance.h"
#include <fcntl.h>
#include <unistd.h>
#include <errno.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

/* 
 * camflowrapper
 * EndtoEndProvenance
 * author: Narun Raman
 *
 *
 * C program calling CamFlow API disclosing language level provenance
 * to CamFlow
 */



void node_agent(char* node) {
	disclose_agent(node);
}

/*
 * functions returning disclosed u_int64 CamFlow values to python
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
