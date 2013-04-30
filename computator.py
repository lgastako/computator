"""An attempt at something like prismatic's Graph in python."""

import inspect

GRAPH = {
    "n": lambda xs: len(xs),
    "m": lambda xs, n: sum(xs) / n,
    "m2": lambda xs, n: sum([x * x for x in xs]),
    "v": lambda m, m2: m2 - (m * m)
}

class NotReady(Exception):
    pass

class Deadlock(Exception):
    pass

def execute_func(f, vals):
    names = inspect.getargspec(f)[0]
    args = []
    for name in names:
        if name not in vals:
            raise NotReady
        args.append(vals[name])
    return f(*args)
        
def execute(graph, **done):
    while len(done) < len(graph):
        unfinished = frozenset(graph.keys()) - frozenset(done.keys())
        for name in unfinished:
            f = graph[name]
            try:
                done[name] = execute_func(f, done)
            except NotReady:
                pass
        if len(frozenset(graph.keys()) - frozenset(done.keys())) == len(unfinished):
            raise Deadlock
    return done

def main():
    print execute(GRAPH, xs=[1, 2, 3, 6])

if __name__ == "__main__":
    main()
