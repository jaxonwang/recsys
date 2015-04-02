
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

/*
 *return NULL if malloc fail
 */
LinkedList * new_Linked_list();

/*
 *return -1 if malloc fail
 */
int list_append(LinkedList * list,void *data);

void * list_iterator_next(LinkedList * list);

void list_iterator_reset(LinkedList * list);

LinkedListNode * list_iterator_getcursor(LinkedList * list);

void list_iterator_setcursor(LinkedList * list, LinkedListNode * cur );

int list_get_len(LinkedList * l);

void destory_linked_list(LinkedList * list);
