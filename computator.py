import inspect

class NotReady(Exception):
    pass

class Deadlock(Exception):
    pass

def computate_func(func, vals, all_names):
    names = inspect.getargspec(func)[0]
    args = []
    for name in names:
        if name not in all_names:
            raise KeyError(name)
        if name not in vals:
            raise NotReady
        args.append(vals[name])
    return func(*args)

def computate(graph, **input_set):
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
                done[name] = computate_func(func, available, all_names)
            except NotReady:
                pass
        #ilf  blah
        #raise Deadlock
    return done
