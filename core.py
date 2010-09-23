"""The module defining the graph.  The graph defines the operations to
execute upon calling the graph with some arguments."""

class Priop:
    """A graph of ``GraphEdges``."""
    
    def __init__(self):
        """Initialises the ``Priop``."""
        
        # Holds ``GraphEdges``.
        self._graph = []

    def add(self, graph_edge):
        """Add ``GraphEdge`` *graph_edge* to the graph.  The *graph_edge* will
        take precedence over previous ``GraphEdges``."""

        self._graph.insert(0, graph_edge)

    def __call__(self, *arguments, **kwargs):
        """Call the ``Priop`` with arguments *arguments*.  The first matching
        ``GraphEdge`` will be called with those arguments, and if no matching
        ``GraphEdge`` is found, NotImplemented will be returned.
        
        *kwargs* will be handed as keyword arguments, and are extra
        arguments."""

        print "arguments = %r" % (arguments,)

        for edge in self._graph:
            if edge.match(arguments):
                return edge(*arguments, **kwargs)

        return NotImplemented


class GraphEdge:
    """A tuple of classes, together with a function to be called on execution
    of the ``GraphEdge``.  Holds also the ``take`` argument, specifying what
    arguments to hand over in what order."""

    def __init__(self, classes, function, take=None):
        """*classes* are the corners of the ``GraphEdge``, *function* is the
        executing function, and *take* = (4, 2) would, on call time with args
        *args*, define to hand over the tupel (args[4], args[2]) as argument
        tuple.
        
        If *take* is None, the tuple given to the call will not be processed
        in any way.
        
        Giving None as a class in *classes* matches everything."""

        self._classes = classes
        self._function = function
        self._take = take

    def match(self, objects):
        """Returns True if the *objects* match the *classes* specification 
        given to ``__init__()``, and False otherwise.  *objects* match if
        ``isinstance(object, class)`` holds for each pair of *object* and
        *class* and if the lengthes of *objects* and of the classes is the
        same."""

        # Check for length mismatch.
        if not len(objects) == len(self._classes):
            return False

        # Check for class mismatch.
        for (object, class_) in zip(objects, self._classes):
            if class_ is not None and not isinstance(object, class_):
                return False

        # No mismatch found => matching.
        return True

    def __call__(self, *args, **kwargs):
        """Call the ``GraphEdge`` with *args* as arguments and *kwargs* as
        keyword arguments.  Does not check for length or match.  Calls the
        function given to ``__init__()`` directly."""

        if self._take is None:
            # Easy way.
            arguments = args
        else:
            # Take what we need.
            arguments = [objects[take] for take in self._take]

        # Call the function.
        return self._function(*arguments, **kwargs)
