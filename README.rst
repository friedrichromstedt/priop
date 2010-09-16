Rationale
---------

Priops is a package for defining priority of methods of different classes for operators.  It can be applied to unary, binary, ternary, and higher operators in general.

Priops is a pun on the contraction of ``priority`` and ``operators``, and is pronounced Pri-ops.

Priops provides numpy ufuncs, exhibiting the Priop functionality.


How it works
------------

Priops defines for an operator ``priop`` taking N arguments a list::
    
    priop.list = [((class1, class2, ..., classN), function), ...] .

For each element, the tuple ``(class1, class2, ...)`` defines the classes to act on, and the ``function`` defines the function to use to evaluate the ``priop`` on objects of this classes.  

``priop`` is a callable object, and once called, it will check which of its ``(class1, class2, ..., classN)`` items matches and has highest precendence.  The items added last have highest precedence.  A tuple ``(class1, class2, ..., classN)`` matches an object tuple ``(obj1, obj2, ..., objN)`` if ``obj1`` is an instance of ``class1``, and ``obj2`` is an instance of ``class2``, and so on for all *N* objects.

Once the matching entry has been found, the corresponding ``function`` is called, with the objects as parameters.  Especially, the ``function`` may be a method of ``class1``, and will be called as ``class1.method([self=]obj1, obj2, ..., objN)``.  In this case, this means the bound method of ``obj1`` from class ``class1`` will be called: ``obj1.method(obj2, ..., objN)``.  (This analogy only holds assumed that the class of ``obj1`` did not overload the ``method``, when it's a subclass of ``class1``.)


Example
-------

We take here the addition of objects.  We go into the numpy context, where this package arises from.  numpy defines the class ``ndarray``, which will treat non-ndarray objects as scalars.  Assume we have a class ``undarray`` (actually I have), which is an ndimensional array, but not a subclass of ``ndarray`` (for some sensible reason).

Calling now::
    
    a + ua

where ``a`` is a ``ndarray`` and ``ua`` is an ``undarray``, adds the ``ua`` as a numpy-scalar to each element of ``a``.  Intended is the same behaviour as in::
    
    ua + a

where ``ua`` recognises the ndarray ``a`` properly and adds it to its elements element-wise.

Solving this problem with Priops, means to create an priop ``add``::

    add = priops.Priop()

and populate it with the appropriate pairs of known-working combinations::
    
    add.define(undarray, ndarray, undarray.__add__)
    add.define(ndarray, undarray, undarray.__radd__, take=(1, 0))

The first line defines the ordinary ``ua.__add__(a)`` emulation.

The second line defines that when the first operator is a ``ndarray`` ``a``, and the second an ``undarray`` ``ua``, ``undarray.__radd__(ua, a)`` shall be called.  Without the ``take`` argument, ``undarray.__radd__(a, ua)`` would be called instead.

The ``take`` argument specifies which arguments to take from the operands in which order.  ``take=(4, 2)`` would, for an operand list ``args``, result in ``*(args[4], args[2])`` being handed over to the ``function``.


Implications
------------

The basis of priops are relational graphs.  Each edge (or triangle, for ternary relations, etc.) has a direction, i.e., the pairs comprising the relation are ordered.

Thus it is possible to create a circle in the relation graph, in the simplest case this is implemented when ``priop(A, B)`` calls ``A.op(B)`` and ``priop(B, A)`` calls ``B.op(A)`` in turn.  In this case we have two ordered pairs ``(A, B)`` and ``(B, A)``, comprising the smallest circle::

   .    /-->--\
   .   /       \
   .  A         B
   .   \       /
   .    \--<--/

Also, relations are in general not transitive, meaning if there is an edge ``(A, B)`` and an edge ``(B, C)``, the egde ``(A, C)`` isn't necessarily defined.


Comparison with priority approaches
-----------------------------------

Typical for priority approaches is the assignment of some real number to each class, giving the priority.  Those classes' methods will be called whose priority is higher.

This approach can be seen as a transitive, linear binary relation.

The linearity imposes some limitations, aside from the fact that the real numbers must be chosen somehow, implying arbitrary conventions.  For instance, when two classes have higher priority than e.g. ``ndarray``, it isn't clear what the priority between this two classes is::

    .        /-------->  A
    .       /
    .  ndarray
    .       \
    .        \----->  B

When one class decides to implement operations with the other, the priority numbers may have to be adjusted, this can cause trouble and may not even be solvable without affecting third-party packages relying on the current configuration.
