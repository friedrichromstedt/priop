"""A module defining a Priop for use as ufunc in numpy."""

import numpy
import priop.core

#
# Define the ufunc class ...
#

# We cannot derive from ``numpy.ufunc``:
#   type 'numpy.ufunc' is not an acceptable base type
class ufunc:
    """An ``numpy.ufunc``, exhibiting the desired functionality.  The 
    ``UfuncPriop`` contains five ``Priop`` graphs:
    
    *   normal call() (``.direct_priop``).
    *   ``reduce()`` call (``.reduce_priop``).
    *   ``accumulate()`` call (``.accumulate_priop``).
    *   ``outer()`` call (``.outer_priop``).
    
    Use the given attributes to add edges to the graphs."""
    
    def __init__(self, name):
        """*name* will be ``.__name__``.  The other numpy ``ufunc`` 
        attributes are not supported."""

        self.__name__ = name

        self.direct_priop = priop.core.Priop()
        self.reduce_priop = priop.core.Priop()
        self.accumulate_priop = priop.core.Priop()
        self.outer_priop = priop.core.Priop()

    def add_ufunc(self, ufunc, classes, take=None):
        """Adds the ``ufunc``'s *ufunc* methods to the different graphs.  The
        graph edges will be created directly using *classes*, i.e., no reverse
        graph edges are added.  *take* is handed over to the ``GraphEdge``
        constructor."""

        self.direct_priop.add(priop.core.GraphEdge(
            classes=classes, function=ufunc, take=take))
        self.reduce_priop.add(priop.core.GraphEdge(
            classes=classes, function=ufunc.reduce, take=take))
        self.accumulate_priop.add(priop.core.GraphEdge(
            classes=classes, function=ufunc.accumulate, take=take))
        self.outer_priop.add(priop.core.GraphEdge(
            classes=classes, function=ufunc.outer, take=take))

    def __call__(self, *args, **kwargs):
        """Calls ``.direct_call`` with *args* and *kwargs*."""

        return self.direct_priop(*args, **kwargs)

    def reduce(self, *args, **kwargs):
        """Calls ``.reduce`` with *args* and *kwargs*."""

        return self.reduce_priop(*args, **kwargs)

    def accumulate(self, *args, **kwargs):
        """Calls ``.accumulate`` with *args* and *kwargs*."""

        return self.accumulate_priop(*args, **kwargs)

    def outer(self, *args, **kwargs):
        """Calls ``.outer`` with *args* and *kwargs*."""

        return self.outer_priop(*args, **kwargs)

#
# Define the ``ufunc`` instances to be used with numpy ...
#
# We can only define ufuncs for those operations supported by 
# ``numpy.set_numeric_ops()``.
#

original = numpy.set_numeric_ops()

absolute = ufunc(name='absolute')
absolute.add_ufunc(ufunc=original['absolute'], 
    classes=(None, None))

add = ufunc(name='add')
add.add_ufunc(ufunc=original['add'],
    classes=(None, None))

bitwise_and = ufunc(name='bitwise_and')
bitwise_and.add_ufunc(ufunc=original['bitwise_and'],
    classes=(None, None))

bitwise_or = ufunc(name='bitwise_or')
bitwise_or.add_ufunc(ufunc=original['bitwise_or'],
    classes=(None, None))

bitwise_xor = ufunc(name='bitwise_xor')
bitwise_xor.add_ufunc(ufunc=original['bitwise_xor'],
    classes=(None, None))

ceil = ufunc(name='ceil')
ceil.add_ufunc(ufunc=original['ceil'],
    classes=(None, None))

conjugate = ufunc(name='conjugate')
conjugate.add_ufunc(ufunc=original['conjugate'],
    classes=(None, None))

divide = ufunc(name='divide')
divide.add_ufunc(ufunc=original['divide'],
    classes=(None, None))

equal = ufunc(name='equal')
equal.add_ufunc(ufunc=original['equal'],
    classes=(None, None))

floor = ufunc(name='floor')
floor.add_ufunc(ufunc=original['floor'],
    classes=(None, None))

floor_divide = ufunc(name='floor_divide')
floor_divide.add_ufunc(ufunc=original['floor_divide'],
    classes=(None, None))

greater = ufunc(name='greater')
greater.add_ufunc(ufunc=original['greater'],
    classes=(None, None))

greater_equal = ufunc(name='greater_equal')
greater_equal.add_ufunc(ufunc=original['greater_equal'],
    classes=(None, None))

invert = ufunc(name='invert')
invert.add_ufunc(ufunc=original['invert'],
    classes=(None, None))

left_shift = ufunc(name='left_shift')
left_shift.add_ufunc(ufunc=original['left_shift'],
    classes=(None, None))

less = ufunc(name='less')
less.add_ufunc(ufunc=original['less'],
    classes=(None, None))

less_equal = ufunc(name='less_equal')
less_equal.add_ufunc(ufunc=original['less_equal'],
    classes=(None, None))

logical_and = ufunc(name='logical_and')
logical_and.add_ufunc(ufunc=original['logical_and'],
    classes=(None, None))

logical_or = ufunc(name='logical_or')
logical_or.add_ufunc(ufunc=original['logical_or'],
    classes=(None, None))

maximum = ufunc(name='maximum')
maximum.add_ufunc(ufunc=original['maximum'],
    classes=(None, None))

minimum = ufunc(name='minimum')
minimum.add_ufunc(ufunc=original['minimum'],
    classes=(None, None))

multiply = ufunc(name='multiply')
multiply.add_ufunc(ufunc=original['multiply'],
    classes=(None, None))

negative = ufunc(name='negative')
negative.add_ufunc(ufunc=original['negative'],
    classes=(None, None))

not_equal = ufunc(name='not_equal')
not_equal.add_ufunc(ufunc=original['not_equal'],
    classes=(None, None))

ones_like = ufunc(name='ones_like')
ones_like.add_ufunc(ufunc=original['ones_like'],
    classes=(None, None))

power = ufunc(name='power')
power.add_ufunc(ufunc=original['power'],
    classes=(None, None))

reciprocal = ufunc(name='reciprocal')
reciprocal.add_ufunc(ufunc=original['reciprocal'],
    classes=(None, None))

remainder = ufunc(name='remainder')
remainder.add_ufunc(ufunc=original['remainder'],
    classes=(None, None))

right_shift = ufunc(name='right_shift')
right_shift.add_ufunc(ufunc=original['right_shift'],
    classes=(None, None))

rint = ufunc(name='rint')
rint.add_ufunc(ufunc=original['rint'],
    classes=(None, None))

sqrt = ufunc(name='sqrt')
sqrt.add_ufunc(ufunc=original['sqrt'],
    classes=(None, None))

square = ufunc(name='square')
square.add_ufunc(ufunc=original['square'],
    classes=(None, None))

subtract = ufunc(name='subtract')
subtract.add_ufunc(ufunc=original['subtract'],
    classes=(None, None))

true_divide = ufunc(name='true_divide')
true_divide.add_ufunc(ufunc=original['true_divide'],
    classes=(None, None))

numpy.set_numeric_ops(absolute=absolute, add=add, bitwise_and=bitwise_and,
    bitwise_or=bitwise_or, bitwise_xor=bitwise_xor, ceil=ceil,
    conjugate=conjugate, divide=divide, equal=equal, floor=floor, 
    floor_divide=floor_divide, greater=greater, greater_equal=greater_equal,
    invert=invert, left_shift=left_shift, less=less, less_equal=less_equal,
    logical_and=logical_and, logical_or=logical_or, maximum=maximum,
    minimum=minimum, multiply=multiply, negative=negative,
    not_equal=not_equal, ones_like=ones_like, power=power, 
    reciprocal=reciprocal, remainder=remainder, right_shift=right_shift,
    rint=rint, sqrt=sqrt, square=square, subtract=subtract, 
    true_divide=true_divide)
