import inspect
import types
import time

from functools import partial

class NotReady(Exception):
    pass

class Deadlock(Exception):
    pass

def _get_defaults(func):
    argspec = inspect.getargspec(func)
    def_values = argspec.defaults
    if def_values:
        def_names = argspec.args[-len(def_values):]
        return dict(zip(def_names, def_values))
    else:
        return {}

def identity_execute(func, args):
    return func(*args)

def profile_execute(func, args):
    start = time.time()
    func(*args)
    end = time.time()
    return end - start

def simple_executor(func, vals, all_names, execute=identity_execute):
    names = inspect.getargspec(func).args
    defaults = _get_defaults(func)
    all_names = all_names | defaults.viewkeys()
    args = []
    for name in names:
        if name not in all_names:
            raise KeyError(name)
        if name in vals:
            args.append(vals[name])
        elif name in defaults:
            args.append(defaults[name])
        else:
            raise NotReady
    return execute(func, args)

profiling_executor = partial(simple_executor, execute=profile_execute)

def _func_to_graph(func):
    return {func.__name__: func}

def computate(computation, input_set=None, executor=None, **kwargs):
    if input_set is None:
        input_set = kwargs
    else:
        for k, v in kwargs.iteritems():
            if k not in input_set:
                input_set[k] = v
    if executor is None:
        executor = simple_executor
    if isinstance(computation, types.FunctionType):
        return _computate_defnk(computation, input_set, executor)
    else:
        return _computate_graph(computation, input_set, executor)

def _computate_defnk(defnk, input_set, executor):
    graph = _func_to_graph(defnk)
    result = _computate_graph(graph, input_set, executor)
    return result[defnk.__name__]

def _computate_graph(graph, input_set, executor):
    graph_names = graph.viewkeys()
    input_names = input_set.viewkeys()
    all_names = graph_names | input_names
    done = {}
    while done.viewkeys() != graph.viewkeys():
        remaining = graph_names - done.viewkeys()
        for name in remaining:
            func = graph[name]
            available = dict(done.items() + input_set.items())
            try:
                done[name] = executor(func, available, all_names)
                break
            except NotReady:
                pass
        else:
            raise Deadlock
    return done

def input_schema(graph):
    arg_stats = set()
    for name, func in graph.iteritems():
        argspec = inspect.getargspec(func)
        arg_names = argspec.args
        if argspec.defaults:
            arg_stats |= frozenset([(name, True) for name in arg_names[:num_optional]] +
                                   [(name, False) for name in arg_names[-num_optional:]])
        else:
            arg_stats |= frozenset([(name, True) for name in arg_names])
    schema = {}
    for name, required in list(arg_stats):   
        if name not in graph:
            if required:
                schema[name] = True
            elif (name, True) not in arg_stats:
                schema[name] = False
    return schema

def output_schema(graph):
    return dict(zip(graph.viewkeys(), [True] * len(graph)))
