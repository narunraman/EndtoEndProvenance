#include "provenance.h"
#include <fcntl.h>
#include <unistd.h>
#include <errno.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct Node {
    int name;
    union {
	    activity_t a;
	    entity_t e;
    } Data;
    struct Node* next;
} Node;

Node* activity_head = NULL;

/* Entity nodes, separated to search easily
 *
 */
Node* data_head = NULL;
Node* function_head = NULL;
Node* library_head = NULL;

//NODES
//Will continuously get called from Python for each node
//creating a linked list for the edges to search through and use

void node_agent(char* node) {
	disclose_agent(node);
}

void node_environment(char* node){
	disclose_entity(node);
}

/* Discloses activity and pushes the activity_t onto a linked list
 * 
 */
void push_activity(char* node, int name) {
	Node *a = malloc(sizeof(Node));
	a -> name = name;
	a -> Data.a = disclose_activity(node);
	a -> next = activity_head;
	activity_head = a;
}

void push_data_node(char* node, int name) {
	Node *e = malloc(sizeof(Node));
	e -> name = name;
	e -> Data.e = disclose_entity(node);
	e -> next = entity_head;
	data_head = e;
}

void push_function_node(char *node, int name) {
	Node *e = malloc(sizeof(Node));
	e -> name = name;
	e -> Data.e = disclose_entity(node);
	e -> next = entity_head;
	function_head = e;
}

void push_library_node(char *node, int name) {
	Node *e = malloc(sizeof(Node));
	e -> name = name;
	e -> Data.e = disclose_entity(node);
	e -> next = entity_head;
	library_head = e;
}

/* These are the functions for the retrieving and disclosing edges
 *
 */

entity_t get_entity(int node, struct Node *e) {
	while(e != NULL) {
		if(e -> name == node) {
			return e -> Data.e;
		}
	}
	printf("The edge's corresponding entity node does not exist!");
	exit(EXIT_FAILURE);
}

activity_t get_activity(int node, struct Node *a) {
	while(a != NULL) {
		if(a -> name == node) {
			return a -> Data.a;
		}
	}
	printf("The edge's corresponding activity node does not exist!");
	exit(EXIT_FAILURE);
}
	

void edge_member(int from, int to) {
	//disclose_something(get_entity(from, library_head), get_entity(to, function_head));
}

void edge_uses_data(int from, int to) {
	disclose_uses(get_entity(from, data_head), get_activity(to, activity_head));
}

void edge_uses_function(int from, int to) {
	disclose_uses(get_entity(from, function_head), get_activity(to, activity_head));
}

void edge_generates(int from, int to) {
	disclose_generates(get_activity(from, activity_head), get_entity(to, data_head));
}

void edge_informs(int from, int to) {
	disclose_informs(get_activity(from, activity_head), get_activity(to, activity_head));
}
