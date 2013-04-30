import inspect

class NotReady(Exception):
    pass

class Deadlock(Exception):
    pass

def computate_func(f, vals, all_names):
    names = inspect.getargspec(f)[0]
    args = []
    for name in names:
        if name not in all_names:
            raise KeyError(name)
        if name not in vals:
            raise NotReady
        args.append(vals[name])
    return f(*args)

def computate(graph, **done):
    all_names = frozenset(graph.keys() + done.keys())
    while len(done) < len(graph):
        done_names = frozenset(done.keys())
        remaining = all_names - done_names
        for name in remaining:
            f = graph[name]
            try:
                done[name] = computate_func(
                    f, done, all_names)
            except NotReady:
                pass
        if len(done) == len(done_names):
            raise Deadlock
    return done
