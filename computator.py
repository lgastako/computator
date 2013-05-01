import inspect
import types

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

def _execute_computation(func, vals, all_names):
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
    return func(*args)

def _func_to_graph(func):
    return {func.__name__: func}

def computate(computation, **input_set):
    if isinstance(computation, types.FunctionType):
        return _computate_defnk(computation, input_set)
    else:
        return _computate_graph(computation, input_set)

def _computate_defnk(defnk, input_set):
    graph = _func_to_graph(defnk)
    result = _computate_graph(graph, input_set)
    return result[defnk.__name__]

def _computate_graph(graph, input_set):
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
                done[name] = _execute_computation(func, available, all_names)
                break
            except NotReady:
                pass
        else:
            raise Deadlock
    return done
