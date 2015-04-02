#include <stdlib.h>
#include <stdio.h>
#include "linkedlist.h"


struct s_LinkedListNode{
	struct s_LinkedListNode * next;
	struct s_LinkedListNode * previous;
	void * data;
	
};

struct s_LinkedList{
	struct s_LinkedListNode * head;
	struct s_LinkedListNode * tail;
	struct s_LinkedListNode * curser;
	int list_length;

};

LinkedList * new_Linked_list(){
	//new list
	LinkedList * n_list = (LinkedList * )malloc(sizeof(LinkedList));
	//new head
	LinkedListNode * n_head = (LinkedListNode *)malloc(sizeof(LinkedListNode));

	if(!n_list || ! n_head)
		return NULL;
	n_head->next = NULL;
	n_head->previous = NULL;

	//init list
	n_list->head = n_head;
	n_list->tail = n_head;
	n_list->curser = n_head;
	n_list->list_length = 0;
	return n_list;
}

int list_append(LinkedList * list,void *data){
	LinkedListNode * node = (LinkedListNode *)malloc(sizeof(LinkedListNode));
	if(!node)
		return -1;

	list->tail->next = node;
	node->previous = list->tail;
	node->data = data;
	list->tail = node;
	list->list_length++;

	return 0;
}

void * list_iterator_next(LinkedList * list){
	if((list->curser == list->tail)&&(list->list_length > 0) ){//get to the end
		return NULL;
	}else{
		list->curser = list->curser->next;
		return list->curser->data;	
	}
}

void list_iterator_reset(LinkedList * list){
	list->curser = list->head;
}

LinkedListNode * list_iterator_getcursor(LinkedList * list){
	return list->curser;
}

void list_iterator_setcursor(LinkedList * list, LinkedListNode * cur ){
	list->curser = cur;
}

int list_get_len(LinkedList * l){
	return l->list_length;
}

inline LinkedListNode * list_get_next_node(LinkedListNode * node){
	return node->next;
}

inline LinkedListNode * list_get_previous(LinkedListNode * node){
	return node->previous;
}

void destory_linked_list(LinkedList * list){

	LinkedListNode * pre = list->head;
	LinkedListNode * current;
	while((current = pre->next) != NULL){
		free(pre);
		pre = current;
	}
	free(pre);
	free(list);
}

/*
int main(){
	
	int i;
	int a[1];
	LinkedList * l = new_Linked_list();
	for(i = 0;i < sizeof(a)/sizeof(int);i++){
		a[i] = i;
		list_append(l,&a[i]);
	}

	int * it_data;
	while((it_data = list_iterator_next(l)) != NULL){
		printf("%d\n",*it_data);
	}

	destory_linked_list(l);

}
*/
