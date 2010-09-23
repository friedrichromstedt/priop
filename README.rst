Rationale
---------

Priop is a package for defining priority of functions based on the positional
arguments.  It can be applied to unary, binary, ternary, and higher operators.
Its core, ``priop.Priop``, selects the best-matching function from a set of
functions based on the classes of the arguments given.

Priop is a pun on the contraction of ``priority`` and ``operators``, and is 
pronounced Pri-ops.  Irrespective of its somehow generality, the name is
due to the main application, operators.

Priop provides numpy ufuncs exhibiting the Priop functionality.


How it works
------------

The basis of priops are relational graphs.  Each edge (or triangle, for 
ternary relations, etc.) has a direction, i.e., the pairs comprising the 
relation are ordered.

Priop defines for an ``priop`` taking *N* arguments a list::
    
    graph = [graph edge 1, graph edge 2, ...] .

Each ``graph edge`` is a callable object and holds:

*   A function to call when the graph edge is executed.

*   A number of classes the positional arguments must be instances of when
    called.

*   A definition of a reordering of the positional arguments before calling
    the function.

The priop itself is also a callable object, and once called, it will check 
which of its edges matches and has highest precendence.  The items added last 
have highest precedence.  A graph edge matches an object tuple 
``(obj1, obj2, ..., objN)`` if there are as many positional arguments as 
classes ``(class1, class2, ..., classN)`` defined for the edge and if ``obj1`` 
is an instance of ``class1``, ``obj2`` is an instance of ``class2``, and so on 
for all *N* objects.

Once the matching entry has been found, the corresponding ``function`` is 
called, with the objects as parameters.  The arguments may be reordered before
calling the function, using the specification given at initialisation time of
the edge.  


Operator Overloading with Priop
-------------------------------

As a special case, the ``function`` called with arguments being instances of 
``class1`` and ``class2`` may be a method of ``class1``, and will be called 
then as ``class1.method([self=]obj1, obj2, ..., objN)``.  This means the bound 
method of ``obj1`` from class ``class1`` will be called: 
``obj1.method(obj2)``.  (This analogy only holds assumed that the class of 
``obj1`` did not overload the ``method``, when it's a subclass of ``class1``.)

Thus, the definitions of the operations in the class of one of the operands is 
called when the priop is executed.  Priop provides the additional layer of
selecting which operator definition matches.

The Priop layer consists of the information of relations, which are not 
class-specific, but class *pair* specific.  


Using Priop
-----------


Eligible Graph Edges
^^^^^^^^^^^^^^^^^^^^

Graph edges have to obey the following protocol:

*   A ``.match()`` function taking the positional arguments given to the
    Priop call and returning a truth value saying if the graph egde can be 
    called with this arguments.

*   It must be callable with arguments and keyword arguments.  The pure Python
    definition thus looks like::
        
        def __call__(self, \*args, \*\*kwargs):

Nothing more is required for a graph egde.


Calling the Priop
^^^^^^^^^^^^^^^^^

Calling the graph happens like::
    
    subtract(ua, a)

    subtract(a, ua)

This will match the graph edges defined before against the arguments given 
using the classes stored in the graph edges.  For the second call, the
graph egde will call the function with argument order reversed.

One can also give keyword arguments to the call of the priop.  Only the
positional arguments are used to match the call arguments, and the keyword
arguments are handed over to the underlying function unchanged.


Population of the Priop
^^^^^^^^^^^^^^^^^^^^^^^

The priop, created by::

    priop = Priop()

is populated by adding graph edges to it::
    
    priop.add(graph_edge)

Graph egdes are created like::
    
    graph_edge = GraphEdge(classes, function[, take])

where *classes* is a tuple defining the classes of the positional arguments 
and the length of the positional tuple, *function* is the function the be 
called on execution, and *take* is tuple defining the reordering of the 
arguments before being handed over to the *function*.  If *take* is given, the 
argument tuple to *function* will consist of the elements of the position 
arguments selected by the indices which are the elements of the *take* tuple 
(for an example, see the example section).


Example
-------

We take here as an example the subtraction of objects.  We go into the numpy 
context, where this package arises from.  numpy defines the class ``ndarray``, 
which will treat non-ndarray objects as scalars.  Assume we have a class 
``undarray``, which has ndimensional array functionality too, and knows how to 
combine with ``ndaray``, but ``ndarray`` don't knows how to combine with 
``undarray`` properly.

Calling now::
    
    a - ua

where ``a`` is a ``ndarray`` and ``ua`` is an ``undarray``, adds the ``ua`` as 
a numpy-scalar to each element of ``a``.  In contrast, an element-wise 
behaviour as in::
    
    ua - a

is intended, where ``ua`` recognises the ndarray ``a`` properly and adds it to 
its elements element-wise.

Solving this problem with Priops, means to create an priop ``subtract``::

    subtract = priop.Priop()

and populate it with the appropriate pairs of known-working combinations::
    
    subtract.add(priop.GraphEdge(classes=(undarray, ndarray), 
        function=undarray.__add__))
    subtract.add(priop.GraphEdge(classes=(ndarray, undarray),
        function=undarray.__radd__, take=(1, 0)))

Notice the reversal of the ``classess`` arguments between the two calls.

The first line defines the ordinary ``ua.__add__(a)`` emulation.

The second line defines that when the first operator is a ``ndarray`` ``a``, 
and the second an ``undarray`` ``ua``, the reversed-binary operation
implementation ``undarray.__radd__(ua, a)`` shall be called.  

The ``take`` argument specifies which arguments to take from the operands in 
which order.  ``take=(4, 2)`` would, for an operand list ``args``, result in 
``*(args[4], args[2])`` being handed over to the ``function``.  Without the 
``take`` argument, ``ua`` and ``a`` would not be reversed, and when calling
the second graph egde, ``undarray.__radd__(a, ua)`` would thus be executed.


Implications
------------


Circular relations
^^^^^^^^^^^^^^^^^^

It is possible to create a circle in the relation graph, in the simplest 
case this is implemented when ``priop(A, B)`` calls ``A.op(B)`` and 
``priop(B, A)`` calls ``B.op(A)`` in turn.  In this case we have two ordered 
pairs ``(A, B)`` and ``(B, A)``, comprising the smallest circle::

   |    /-->--\
   |   /       \
   |  A         B
   |   \       /
   |    \--<--/

Also, relations are in general not transitive, meaning if there is an edge 
``(A, B)`` and an edge ``(B, C)``, the egde ``(A, C)`` isn't necessarily 
defined.


Subclassing
^^^^^^^^^^^

When an object is instance of a subclass of the class used for defining the
edge, the edge will still match.  Nevertheless, if there is an egde defined 
matching *better*, then that one will be called.  Edges match better if they
are defined later.


Ambiguity of Edges
^^^^^^^^^^^^^^^^^^

Several edges may match by subclassing of the classes involved.

The priority of edges is defined by the time of their addition to the priop.
Another possibility would be, to use inheritance detection of classes, and
to call those edge which is the most special.  Nevertheless:

1.  This creates even more overhead

2.  It may be undecidable, e.g. if one or the other operand class can be
    choosen more "specialised"

3.  It is more specific than the general graph approach, and thus makes
    additional assumptions, which may be unnecessary or even restrictive
    to the application.

There *is* some linear order in the graph, but it is a linear order
of the graph edges, not of the graph nodes anymore.

Binary operator definitions seem to be more tree-like than linear:

*   Subclasses may open a new branch of operator definitions

*   There are lots of operations not defined at all

This treeishness is represented by the graph edges of the graphs created.


Comparison with Linear Priority Number Approaches
-------------------------------------------------

Typical for priority number approaches is the assignment of some real number 
to each class, giving the priority.  The methods of the class with the
higher priority will be called.

This approach can be seen as a transitive, linear binary relation.

The linearity imposes some limitations, aside from the fact that the real 
numbers must be chosen somehow, implying arbitrary conventions.  For instance, 
when two classes have higher priority than e.g. ``C``, it isn't clear 
what the priority between this two classes is::

    |        /-------->  A
    |       /
    |      C
    |       \
    |        \----->  B

When A decides to implement operations with B, the priority numbers may have 
to be adjusted, this can cause trouble and may not even be solvable without 
affecting third packages relying on the current configuration.

With Priop, the egde A-B stays undefined as long as there is no matching
edge, and the edge can be defined in either way.


Comparison with Native Python Operator Overloading
--------------------------------------------------

In native Python, a class can define binary operators.  They can be in a
forward and reverse mode.  (In-place operators are just another operator with
another semantic, though in-place operators can be derived from the normal 
ones.)  An operator may return ``NotImplemented`` if the operation is not supported.

This approach is based on the assumtion, that each operand can decide if its
implementation is sufficient or not.  In fact, the implementation is deemed 
sufficient if it exists.  But there may exist a *better* implementation, 
especially in the second operand.  There is no way to decide which 
implementation suits better based only on the fact of their existence, what
is the only information contained in the return value of the overloaded 
operator.

It seems that operands can only tell if they have an idea how to handle the
other operand, but they have no means of comparing different implementations.

Priop implements such a comparison by the assumtion, that modules are 
imported from bottom to top.  This means, that edges defined with higher-level
classes will be defined later, and thus have higher precedence than low-level
edges.
