import inspect

class NotReady(Exception):
    pass

class Deadlock(Exception):
    pass

def computate_func(f, vals):
    names = inspect.getargspec(f)[0]
    args = []
    for name in names:
        if name not in vals:
            raise NotReady
        args.append(vals[name])
    return f(*args)

def computate(graph, **done):
    while len(done) < len(graph):
        unfinished = frozenset(graph.keys()) - frozenset(done.keys())
        for name in unfinished:
            f = graph[name]
            try:
                done[name] = computate_func(f, done)
            except NotReady:
                pass
        if len(frozenset(graph.keys()) - frozenset(done.keys())) == len(unfinished):
            raise Deadlock
    return done
