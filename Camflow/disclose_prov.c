#include "provenance.h"
#include <fcntl.h>
#include <unistd.h>
#include <errno.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct Node {
    int id;
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
activity_t push_activity(char* node, int id) {
	Node *a = malloc(sizeof(Node));
	a -> id = id;
	a -> Data.a = disclose_activity(node);
	a -> next = activity_head;
	activity_head = a;
	return a -> Data.a;
}

void push_data_node(char* node, int id) {
	Node *e = malloc(sizeof(Node));
	e -> id = id;
	e -> Data.e = disclose_entity(node);
	e -> next = data_head;
	data_head = e;
}

void push_function_node(char *node, int id) {
	Node *e = malloc(sizeof(Node));
	e -> id = id;
	e -> Data.e = disclose_entity(node);
	e -> next = function_head;
	function_head = e;
}

void push_library_node(char *node, int id) {
	Node *e = malloc(sizeof(Node));
	e -> id = id;
	e -> Data.e = disclose_entity(node);
	e -> next = library_head;
	library_head = e;
}

/* These are the functions for the retrieving and disclosing edges
 *
 */

entity_t get_entity(int node_id, Node *e) {
	while(e != NULL) {
		if(e -> id == node_id) {
			return e -> Data.e;
		}
		e = e -> next;
	}
	printf("The edge's corresponding entity node does not exist!");
	exit(EXIT_FAILURE);
}

activity_t get_activity(int node_id, Node *a) {
	while(a != NULL) {
		if(a -> id == node_id) {
			return a -> Data.a;
		}
		a = a -> next;
	}
	printf("The edge's corresponding activity node does not exist!");
	exit(EXIT_FAILURE);
}
	

activity_t get_act(int node_id) {
	return get_activity(node_id, activity_head);
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

void printActivities(Node *n) {
	while(n != NULL) {
		printf("activity %d is %d\n", n -> id, n -> Data.a);
		n = n -> next;
	}
}

void printEntities(Node *d, Node *f, Node *l) {
	while(d != NULL) {
		printf("data %d is %d\n", d -> id, d -> Data.e);
		d = d -> next;
	}
	while(f != NULL) {
		printf("function %d is %d\n", f -> id, f -> Data.e);
		f = f -> next;
	}
	while(l != NULL) {
		printf("library %d is %d\n", l -> id, l -> Data.e);
		l = l -> next;
	}
}

void printLists() {
	printActivities(activity_head);
	printEntities(data_head, function_head, library_head);
}
