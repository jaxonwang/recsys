#include <stdlib.h>
#include <stdio.h>
#include <Python.h>
#include <math.h>
#include "linkedlist.h"

/*
 .##..##.######.#####..######.######.##..##.
 .##..##.##.....##..##...##...##......####..
 .##..##.####...#####....##...####.....##...
 ..####..##.....##..##...##...##......####..
 ...##...######.##..##...##...######.##..##.
 ...........................................
 */
struct s_sparse_vector{
	LinkedList * storelist; 	//store as a list
	int vectorlen;

};

struct s_vec_cell{
	int index;
	double value;
};

typedef struct s_sparse_vector sparse_vector;
typedef struct s_vec_cell vec_cell;

sparse_vector * new_sparse_vector(int indices[],double values[],const int length,int veclen){
	sparse_vector * sv = (sparse_vector *)malloc(sizeof(sparse_vector));
	if(!sv) 	return NULL;
	sv->vectorlen = veclen;
	sv->storelist = new_Linked_list();
	if(!sv->storelist) return NULL;

	int i;
	for(i = 0;i < length;i++){
		vec_cell * new_cell = (vec_cell *)malloc(sizeof(vec_cell));
		if(!new_cell) return NULL;
		new_cell->index = indices[i];
		new_cell->value = values[i];
		if(list_append(sv->storelist,new_cell) == -1)
			return NULL;
	}

	return sv;
}

int sparse_vector_get_size(sparse_vector * sv){
	return list_get_len(sv->storelist);
}

int sparse_vector_get_vector_len(sparse_vector * sv){
	return sv->vectorlen;
}

vec_cell * sparse_vector_next_none_zero(sparse_vector * sv){
	 return list_iterator_next(sv->storelist);
}

void destroy_sparse_vec(sparse_vector * sv){

	vec_cell * cell;
	list_iterator_reset(sv->storelist);
	while((cell= list_iterator_next(sv->storelist)) != NULL)
		free(cell);
	destory_linked_list(sv->storelist);
	free(sv);
}

double sparse_vector_get_mean(sparse_vector * sv){
	long double total = 0;

	vec_cell * cell;
	//set curser to the head
	list_iterator_reset(sv->storelist);
	while((cell= list_iterator_next(sv->storelist)) != NULL)
		total += cell->value;
	return (double)(total / sparse_vector_get_vector_len(sv));
}

double sparse_vector_get_variance(sparse_vector * sv){
	double mean = sparse_vector_get_mean(sv);

	vec_cell * cell;
	double var = 0;
	//set curser to the head
	list_iterator_reset(sv->storelist);
	while((cell= list_iterator_next(sv->storelist)) != NULL){
		double tmp = cell->value - mean;
		var += tmp * tmp;
	}
	return var;
}

/*
.########..##....##.########.##.....##..#######..##....##
.##.....##..##..##.....##....##.....##.##.....##.###...##
.##.....##...####......##....##.....##.##.....##.####..##
.########.....##.......##....#########.##.....##.##.##.##
.##...........##.......##....##.....##.##.....##.##..####
.##...........##.......##....##.....##.##.....##.##...###
.##...........##.......##....##.....##..#######..##....##
 */


/*************MY PYTHON OBJECT SPARSE VECTOR***************************/
//sparse vextor pytype
typedef struct {
	PyObject_HEAD
	sparse_vector * sv;
} SparseVectorObject;


static void SparseVector_dealloc(SparseVectorObject * self){
	destroy_sparse_vec(self->sv);
	self->ob_type->tp_free((PyObject*)self);
}
static PyObject * SparseVector_str(PyObject * pyobj){

	SparseVectorObject * obj = (SparseVectorObject *) pyobj;
	LinkedListNode * cur_store = list_iterator_getcursor(obj->sv->storelist);
	vec_cell * cell;
	//set curser to the head
	list_iterator_reset(obj->sv->storelist);
	char * buffer  = (char *) malloc(obj->sv->vectorlen * 30); 
	if(!buffer) {
		PyErr_NoMemory();
		return NULL;
	}
	char * cursor = buffer;
	while((cell= list_iterator_next(obj->sv->storelist)) != NULL){
		cursor += sprintf(cursor,"%d:%.1f\n",cell->index,cell->value);
	}
	//restore
	list_iterator_setcursor(obj->sv->storelist,cur_store);

	PyObject * ret = Py_BuildValue("s",buffer);
	free(buffer);
	return ret;
}

static int SparseVector_init(PyObject * type, PyObject *args, PyObject *kwds){
	SparseVectorObject * self = (SparseVectorObject *)type;
	PyObject * indices;
	PyObject * values;

	indices = PyTuple_GetItem(args,0);
	values = PyTuple_GetItem(args,1);
	const int vectorlen = PyInt_AsLong(PyTuple_GetItem(args,2));
	const int indiceslen = PyList_Size(indices);
	
	if(indiceslen!=PyList_Size(values)){
		PyErr_SetString(PyExc_ValueError,"Tow list length and vector length do not match.");
		return -1;
	}
	//convert to sparse vector struct 
	int * tmp_indices = (int *)malloc(sizeof(int)*indiceslen);
	double * tmp_values = (double *)malloc(sizeof(double)*indiceslen);
	if(!(tmp_indices&&tmp_values)){
		PyErr_NoMemory();
		return -1;
	}

	int i;
	for(i=0;i < indiceslen;i++){
		tmp_indices[i] = PyInt_AsLong(PyList_GetItem(indices,i));
		if(tmp_indices[i] >= vectorlen){ //bigger than specific vector length
			PyErr_SetString(PyExc_ValueError,"Index exceed the vector length.");
			free(tmp_indices);
			free(tmp_values);
			return -1;
		}
		tmp_values[i] = PyFloat_AsDouble(PyList_GetItem(values,i));
	}
	
	self->sv = new_sparse_vector(tmp_indices,tmp_values,indiceslen,vectorlen);

	if(!self->sv){
		PyErr_NoMemory();
		free(tmp_indices);
		free(tmp_values);
		return -1;
	}

	free(tmp_indices);
	free(tmp_values);

	return 0;

}
//python type object
static PyTypeObject vector_SparseVectorType = {
	PyObject_HEAD_INIT(NULL)
	0,                         /*ob_size*/
	"vector.SparseVector",            /*tp_name*/
	sizeof(SparseVectorObject),/*tp_basicsize*/
	0,                         /*tp_itemsize*/
	(destructor)SparseVector_dealloc,  /*tp_dealloc*/
	0,                         /*tp_print*/
	0,                         /*tp_getattr*/
	0,                         /*tp_setattr*/
	0,                         /*tp_compare*/
	0,                         /*tp_repr*/
	0,                         /*tp_as_number*/
	0,                         /*tp_as_sequence*/
	0,                         /*tp_as_mapping*/
	0,                         /*tp_hash */
	0,                         /*tp_call*/
	SparseVector_str,          /*tp_str*/
	0,                         /*tp_getattro*/
	0,                         /*tp_setattro*/
	0,                         /*tp_as_buffer*/
	Py_TPFLAGS_DEFAULT,        /*tp_flags*/
	"SparseVector objects",    /* tp_doc */
};


/*************MY PYTHON METHOD***************************/

static PyObject * pearsonr(PyObject * self,PyObject *args){
	
	SparseVectorObject * x_pyobj = (SparseVectorObject *) PyTuple_GetItem(args,0);
	SparseVectorObject * y_pyobj = (SparseVectorObject *) PyTuple_GetItem(args,1);

	sparse_vector * x = x_pyobj->sv;
	sparse_vector * y = y_pyobj->sv;

	list_iterator_reset(x->storelist);
	list_iterator_reset(y->storelist);

	int size = x->vectorlen;
	if(size != y->vectorlen){
		PyErr_SetString(PyExc_ValueError,"Different vector length.");
		return NULL;
	}

	if((int)PyTuple_GetItem(args,2) && PyInt_AsLong(PyTuple_GetItem(args,2)) == 1)
		size--; 	//id start from 1
	
	double Ex = 0;
	double Ey = 0;
	double Exy = 0;
	double Ex2 = 0;
	double Ey2 = 0;

	vec_cell * cell_x = list_iterator_next(x->storelist);	
	vec_cell * cell_y = list_iterator_next(y->storelist);	

	for(;;){

		if((cell_x == NULL)||(cell_y == NULL))
			break;
		int index_x = cell_x->index;
		int index_y = cell_y->index;

//		printf("x %f\ty %f\n",cell_x->value,cell_y->value);

		if(index_x > index_y){
			Ey += cell_y->value;
			Ey2 += cell_y->value * cell_y->value;
			cell_y = list_iterator_next(y->storelist);	
		}else if(index_x < index_y){
			Ex += cell_x->value;
			Ex2 += cell_x->value * cell_x->value;
			cell_x = list_iterator_next(x->storelist);	
		}else{
	//		printf("x %d\ty %d\n",index_x,index_y);
			Ex += cell_x->value;
			Ex2 += cell_x->value * cell_x->value;
			Ey += cell_y->value;
			Ey2 += cell_y->value * cell_y->value;
			Exy += cell_x->value * cell_y->value;
			cell_y = list_iterator_next(y->storelist);	
			cell_x = list_iterator_next(x->storelist);	
		}
	}

	while(cell_x){
		Ex += cell_x->value;
		Ex2 += cell_x->value * cell_x->value;
		cell_x = list_iterator_next(x->storelist);
	}

	while(cell_y){
		Ey += cell_y->value;
		Ey2 += cell_y->value * cell_y->value;
		cell_y = list_iterator_next(y->storelist);
	}
	//printf("Ex %f\n Ey %f\n Exy %f\n Ex2 %f\n Ey2 %f\n",Ex,Ey,Exy,Ex2,Ey2);

	double personr = (Exy - Ex * Ey / size) / \
			 sqrt((Ex2 - Ex * Ex / size) * (Ey2 - Ey * Ey / size ));
	return Py_BuildValue("f",personr);
} 


static PyMethodDef vector_methods[] = {
	{"pearsonr", pearsonr,METH_VARARGS, "pearsonr(sparsevector_x,sparsevector_y,startfromone = False) --> pearson correlation value\n\
if startfromone is True, the index will start from one, that is\n\
the length of the vectors will minus by one.\n"
	},

       	{NULL}  /* Sentinel */
};

#ifndef PyMODINIT_FUNC
#define PyMODINIT_FUNC void
#endif

PyMODINIT_FUNC initvector(){
	PyObject * m;

	vector_SparseVectorType.tp_new = PyType_GenericNew;
	vector_SparseVectorType.tp_init = SparseVector_init;

	if(PyType_Ready(&vector_SparseVectorType) < 0)
		return;
	m = Py_InitModule("vector",vector_methods);
	Py_INCREF(&vector_SparseVectorType);
	PyModule_AddObject(m,"SparseVector",(PyObject *)&vector_SparseVectorType);

}

/*
int main(){
	int indices[5] = {1,3,5,7,9};
	double values[5] = {1.5,2.5,3,5.5,4};

	sparse_vector * sv = new_sparse_vector(indices,values,sizeof(indices)/4);
	
	printf("%f\n",sparse_vector_get_mean(sv));
	printf("%f\n",sparse_vector_get_variance(sv));
	
	destroy_sparse_vec(sv);
}

*/
	
