#include <Python.h>


static PyObject *
fast_interpreter_evaluate(PyObject *self, PyObject *args)
{
    const char *command;
    int sts;

    if (!PyArg_ParseTuple(args, "s", &command))
        return NULL;
    sts = system(command);
    return PyLong_FromLong(sts);
}

static PyMethodDef FastInterpreterMethods[] = {
    {"evaluate",  fast_interpreter_evaluate, METH_VARARGS, NULL},
    {NULL, NULL, 0, NULL}        /* Sentinel */
};


static struct PyModuleDef fast_interpreter = {
   PyModuleDef_HEAD_INIT,
   "fast_interpreter", /* name of module */
   NULL, /* module documentation, may be NULL */
   -1, /* size of per-interpreter state of the module,
                or -1 if the module keeps state in global variables. */
   FastInterpreterMethods
};


PyMODINIT_FUNC
PyInit_fast_interpreter(void)
{
    PyObject *m;

    m = PyModule_Create(&fast_interpreter);
    if (m == NULL)
        return NULL;

    return m;
}
