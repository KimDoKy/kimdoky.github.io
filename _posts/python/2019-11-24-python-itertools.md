---
layout: post
section-type: post
title: Python - itertools (효율적인 반복을 위한 함수)
category: python
tags: [ 'python' ]
---

# itertools (효율적인 반복을 위한 함수)

알고리즘 문제를 풀다보면 머릿속에 있는 것을 구현하다가 시간을 많이 소비하게 된다.  
문제를 모두 푼 다음 다른 사람의 답안을 보게 되면 간단히 구현해 둔 코드들을 발견하게 되고,  
그 중 많이 보이는 것이 `itertools`이다.  

[itertools 공식문서 / 3.7.5](https://docs.python.org/ko/3.7/library/itertools.html)에 친절히 잘 나와 있지만, 아직 한글화 작업은 진행되지 않았고, 그 와중에 3.8 버전이 나왔다.  

아직은 3.8 버전을 도입한 회사들이 드물거라는 가정하에 3.7.5 버전의 itertools 문서를 살펴본다.

(누군가에게 도움이 되기 위한 포스팅이 아니라, 그냥 내가 문서를 보았다...라는 정도의 포스팅이다.)

### 무한 반복자

Iterator | Arguments | Results | Example
---|---|---|---
[`count()`](https://docs.python.org/ko/3.7/library/itertools.html#itertools.count) | start, [step] | start, start+step, start+2*setp, ...|`count(10)` -> `10 11 12 13 14 ...`
[`cycle()`](https://docs.python.org/ko/3.7/library/itertools.html#itertools.cycle) | p | p0, p1, ...plast, p0, p1, ... | `cycle('ABCD')` -> `A B C D A B C D ...`
[`repeat()`](https://docs.python.org/ko/3.7/library/itertools.html#itertools.repeat) | elem [,n] | elem, elem, elem, ...<br>무한 반복, 혹은 최대 n번 | `repeat(10, 3)` -> `10 10 10`

### 가장 짧은 입력 시퀀스에서 종료되는 반복자

Iterator | Arguments | Results | Example
---|---|---|---
[`accumulate()`](https://docs.python.org/ko/3.7/library/itertools.html#itertools.accumulate) | p [,func] | p0, p0+p1, p0+p1+p2, ... | `accumulate([1,2,3,4,5])` -> `1 3 6 10 15`
[`chain()`](https://docs.python.org/ko/3.7/library/itertools.html#itertools.chain) | p, q, ... | p0, p1, ... plast, p0, p1, ... | `chain('ABC', 'DEF')` -> `A B C D E F`
[`chain.from_iterable()`](https://docs.python.org/ko/3.7/library/itertools.html#itertools.chain.from_iterable) | iterable | p0, p1, ... plast, p0, p1, ... | `chain.from_iterable(['ABC','DEF'])` -> `A B C D E F`
[`compress()`](https://docs.python.org/ko/3.7/library/itertools.html#itertools.compress) | data, seletors | (d[0] if s[0]), (d[1] if s[1]), ... | `compress('ABCDEF', [1,0,1,0,1,1])` -> `A C E F`
[`dropwhile()`](https://docs.python.org/ko/3.7/library/itertools.html#itertools.dropwhile) | pred, seq | pred가 실패할때 시작되는 seq[n], seq[n+1] | `dropwhile(lambda x: x<5, [1,4,6,4,1])` -> `6 4 1`
[`filterfalse()`](https://docs.python.org/ko/3.7/library/itertools.html#itertools.filterfalse) | pred, seq | pred(elem)가 false인 seq의 element | `filterfalse(lambda x: x%2, range(10))` -> `0 2 4 6 8`
[`groupby()`](https://docs.python.org/ko/3.7/library/itertools.html#itertools.groupby) | iterable[,key] | key(v)의 값으로 그룹화된 하위 반복자 |
[`islice()`](https://docs.python.org/ko/3.7/library/itertools.html#itertools.islice) | seq, [start,] stop [,step] | seq의 요소 [start:stop:step] | `islice('ABCDEFG', 2, None)` -> `C D E F G`
[`starmap()`](https://docs.python.org/ko/3.7/library/itertools.html#itertools.starmap) | func, seq | func(*seq[0]), func(*seq[1]),... | `starmap(pow, [(2,5), (3,2), (10,3)])` -> `32 9 1000`
[`takewhile()`](https://docs.python.org/ko/3.7/library/itertools.html#itertools.takewhile) | pred, seq | seq[0], seq[1], pred가 실패할때까지 | `takewhile(lambda x: x<5, [1,4,6,4,1])` -> `1 4`
[`tee()`](https://docs.python.org/ko/3.7/library/itertools.html#itertools.tee) | it, n | it1, it2, ... 하나의 반복자를 n으로 나눔 |
[`zip_longest()`](https://docs.python.org/ko/3.7/library/itertools.html#itertools.zip_longest) | p, q, ...| (p[0], q[0]), (p[1], q[1]), ... | `zip_longest('ABCD', 'xy', fillvalue='-')` -> `Ax By C- D-`

### 조합 반복자

Iterator | Arguments | Results | Example
---|---|---|---
[`product()`](https://docs.python.org/ko/3.7/library/itertools.html#itertools.product) | p, q, ...<br>[repeat=1] | 중첩된 for 루프와 동등한 cartesian product(무얼 말하는지 모르겠음) | `product('ABCD', repeat=2)` -> `AA AB AC AD BA BB BC .... DA DB DC DD`
[`permutations()`](https://docs.python.org/ko/3.7/library/itertools.html#itertools.permutations) | p[, r] | r-length tuples, 가능한 모든 순서, 반복되는 요소 없음 | `permutations('ABCD', 2)` -> `AB AC AD BA BC BD CA CB CD DA DB DC`
[`combinations()`](https://docs.python.org/ko/3.7/library/itertools.html#itertools.combinations) | p, r | r길이의 조합의 모든 경우의 수 | `combinations('ABCD', 2)` -> `AB AC AD BC BD CD`
[`combinations_with_replacement()`](https://docs.python.org/ko/3.7/library/itertools.html#itertools.combinations_with_replacement) | p, r | r-length tuples, 정렬되어 있음, 반복되는 요소 있음 | `combinations_with_replacement('ABCD', 2)` -> `AA AB AC AD BB BC BD CC CD DD`

### Itertools 레시피

```python
def take(n, iterable):
    "Return first n items of the iterable as a list"
    return list(islice(iterable, n))

def prepend(value, iterator):
    "Prepend a single value in front of an iterator"
    # prepend(1, [2, 3, 4]) -> 1 2 3 4
    return chain([value], iterator)

def tabulate(function, start=0):
    "Return function(0), function(1), ..."
    return map(function, count(start))

def tail(n, iterable):
    "Return an iterator over the last n items"
    # tail(3, 'ABCDEFG') --> E F G
    return iter(collections.deque(iterable, maxlen=n))

def consume(iterator, n=None):
    "Advance the iterator n-steps ahead. If n is None, consume entirely."
    # Use functions that consume iterators at C speed.
    if n is None:
        # feed the entire iterator into a zero-length deque
        collections.deque(iterator, maxlen=0)
    else:
        # advance to the empty slice starting at position n
        next(islice(iterator, n, n), None)

def nth(iterable, n, default=None):
    "Returns the nth item or a default value"
    return next(islice(iterable, n, None), default)

def all_equal(iterable):
    "Returns True if all the elements are equal to each other"
    g = groupby(iterable)
    return next(g, True) and not next(g, False)

def quantify(iterable, pred=bool):
    "Count how many times the predicate is true"
    return sum(map(pred, iterable))

def padnone(iterable):
    """Returns the sequence elements and then returns None indefinitely.

    Useful for emulating the behavior of the built-in map() function.
    """
    return chain(iterable, repeat(None))

def ncycles(iterable, n):
    "Returns the sequence elements n times"
    return chain.from_iterable(repeat(tuple(iterable), n))

def dotproduct(vec1, vec2):
    return sum(map(operator.mul, vec1, vec2))

def flatten(listOfLists):
    "Flatten one level of nesting"
    return chain.from_iterable(listOfLists)

def repeatfunc(func, times=None, *args):
    """Repeat calls to func with specified arguments.

    Example:  repeatfunc(random.random)
    """
    if times is None:
        return starmap(func, repeat(args))
    return starmap(func, repeat(args, times))

def pairwise(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)

def grouper(iterable, n, fillvalue=None):
    "Collect data into fixed-length chunks or blocks"
    # grouper('ABCDEFG', 3, 'x') --> ABC DEF Gxx"
    args = [iter(iterable)] * n
    return zip_longest(*args, fillvalue=fillvalue)

def roundrobin(*iterables):
    "roundrobin('ABC', 'D', 'EF') --> A D E B F C"
    # Recipe credited to George Sakkis
    num_active = len(iterables)
    nexts = cycle(iter(it).__next__ for it in iterables)
    while num_active:
        try:
            for next in nexts:
                yield next()
        except StopIteration:
            # Remove the iterator we just exhausted from the cycle.
            num_active -= 1
            nexts = cycle(islice(nexts, num_active))

def partition(pred, iterable):
    'Use a predicate to partition entries into false entries and true entries'
    # partition(is_odd, range(10)) --> 0 2 4 6 8   and  1 3 5 7 9
    t1, t2 = tee(iterable)
    return filterfalse(pred, t1), filter(pred, t2)

def powerset(iterable):
    "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s)+1))

def unique_everseen(iterable, key=None):
    "List unique elements, preserving order. Remember all elements ever seen."
    # unique_everseen('AAAABBBCCDAABBB') --> A B C D
    # unique_everseen('ABBCcAD', str.lower) --> A B C D
    seen = set()
    seen_add = seen.add
    if key is None:
        for element in filterfalse(seen.__contains__, iterable):
            seen_add(element)
            yield element
    else:
        for element in iterable:
            k = key(element)
            if k not in seen:
                seen_add(k)
                yield element

def unique_justseen(iterable, key=None):
    "List unique elements, preserving order. Remember only the element just seen."
    # unique_justseen('AAAABBBCCDAABBB') --> A B C D A B
    # unique_justseen('ABBCcAD', str.lower) --> A B C A D
    return map(next, map(itemgetter(1), groupby(iterable, key)))

def iter_except(func, exception, first=None):
    """ Call a function repeatedly until an exception is raised.

    Converts a call-until-exception interface to an iterator interface.
    Like builtins.iter(func, sentinel) but uses an exception instead
    of a sentinel to end the loop.

    Examples:
        iter_except(functools.partial(heappop, h), IndexError)   # priority queue iterator
        iter_except(d.popitem, KeyError)                         # non-blocking dict iterator
        iter_except(d.popleft, IndexError)                       # non-blocking deque iterator
        iter_except(q.get_nowait, Queue.Empty)                   # loop over a producer Queue
        iter_except(s.pop, KeyError)                             # non-blocking set iterator

    """
    try:
        if first is not None:
            yield first()            # For database APIs needing an initial cast to db.first()
        while True:
            yield func()
    except exception:
        pass

def first_true(iterable, default=False, pred=None):
    """Returns the first true value in the iterable.

    If no true value is found, returns *default*

    If *pred* is not None, returns the first item
    for which pred(item) is true.

    """
    # first_true([a,b,c], x) --> a or b or c or x
    # first_true([a,b], x, f) --> a if f(a) else b if f(b) else x
    return next(filter(pred, iterable), default)

def random_product(*args, repeat=1):
    "Random selection from itertools.product(*args, **kwds)"
    pools = [tuple(pool) for pool in args] * repeat
    return tuple(random.choice(pool) for pool in pools)

def random_permutation(iterable, r=None):
    "Random selection from itertools.permutations(iterable, r)"
    pool = tuple(iterable)
    r = len(pool) if r is None else r
    return tuple(random.sample(pool, r))

def random_combination(iterable, r):
    "Random selection from itertools.combinations(iterable, r)"
    pool = tuple(iterable)
    n = len(pool)
    indices = sorted(random.sample(range(n), r))
    return tuple(pool[i] for i in indices)

def random_combination_with_replacement(iterable, r):
    "Random selection from itertools.combinations_with_replacement(iterable, r)"
    pool = tuple(iterable)
    n = len(pool)
    indices = sorted(random.randrange(n) for i in range(r))
    return tuple(pool[i] for i in indices)

def nth_combination(iterable, r, index):
    'Equivalent to list(combinations(iterable, r))[index]'
    pool = tuple(iterable)
    n = len(pool)
    if r < 0 or r > n:
        raise ValueError
    c = 1
    k = min(r, n-r)
    for i in range(1, k+1):
        c = c * (n - k + i) // i
    if index < 0:
        index += c
    if index < 0 or index >= c:
        raise IndexError
    result = []
    while r:
        c, n, r = c*r//n, n-1, r-1
        while index >= c:
            index -= c
            c, n = c*(n-r)//n, n-1
        result.append(pool[-1-n])
    return tuple(result)
```
