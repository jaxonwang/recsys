/*
Func Declare
*/



/*
Mermory GC

*/

#define INITIAL_LIST_VALUE 500000

struct s_obj_list{
	int size;
	int stored;
	void * (* list)[];
} ;

typedef struct s_obj_list mem_obj_list;

mem_obj_list * init_objlist(){
	mem_obj_list * objlist = (mem_obj_list *)malloc(sizeof(mem_obj_list));
	objlist->size = INITIAL_LIST_VALUE;
	objlist->stored = 0;
	objlist->list = (void *(*)[])malloc(sizeof(void *) * INITIAL_LIST_VALUE);
	return objlist;
}

//append to mem obj list
void append_to_list(mem_obj_list * objlist,void * obj){
	if (objlist->stored >= objlist->size){
		fprintf(stderr,"full list!\n");
		return;
	}
	(*objlist->list)[objlist->stored++] = obj;

}
void destroy_objlist(mem_obj_list * objlist){
	int i;
	for(i = 0;i < objlist->stored;i++){
		free((*objlist->list)[i]);
	}
	free(objlist->list);
	free(objlist);
}


//////////////////////////////
