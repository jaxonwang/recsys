
/*
 *data structure
 */
struct s_LinkedListNode;
typedef struct s_LinkedListNode LinkedListNode;

struct s_LinkedList;
typedef struct s_LinkedList LinkedList;

/*
 *function
 */
LinkedList * new_Linked_list();

void list_append(LinkedList * list,void *data);

void * list_iterator_next(LinkedList * list);

int list_get_len(LinkedList * l);

void destory_linked_list(LinkedList * list);
