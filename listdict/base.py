# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
import typing as t

__ALL__ = ["Pair", "ListDict", "append", "mk", "iter", "getone"]

Pair = t.Tuple[t.Any, t.Any]
K = t.TypeVar("K")
V = t.TypeVar("V")
ListDict = t.Dict[K, t.MutableSequence[V]]


class MultipleValues(Exception):
    pass


def append(dct: ListDict[K, V], key: K, value: V):
    """you have a dictionary of lists. append a value to the list of
    key.
    """
    dct.setdefault(key, []).append(value)


def extend(dct: ListDict[K, V], key: K, values: t.Iterable[V]):
    for value in values:
        append(dct, key, value)


def mk(data: t.Iterable[t.Tuple[K, t.Any]], *parsers, idx=0) -> ListDict[K, t.Any]:
    """take an iterable of key-value pairs and construct a dictionary
    of lists of the values. calls itself recursively on the values
    ``recurse`` number of times.
    """
    dct = {}  # type: ListDict[K, t.Any]
    for key, value in map(parsers[idx], data):
        if idx < len(parsers) - 1:
            value = mk(value, *parsers, idx=idx + 1)
        append(dct, key, value)
    return dct


def iter(dct: ListDict[K, t.Any], depth=0) -> t.Iterator[tuple]:
    """you have a dictionary of lists. Get tuples of key and value for
    each value in each list. values will be recursively unpacked as ListDicts
    ``depth`` number of times.
    """
    for key, values in dct.items():
        for value in values:
            if depth > 0:
                try:
                    yield from ((key, *vals) for vals in iter(value, depth - 1))
                except AttributeError:
                    yield key, value
            else:
                yield key, value


def iterpairs(dct: ListDict, depth=0):
    for key, values in dct.items():
        for value in values:
            if depth > 0:
                try:
                    yield (key, list(iterpairs(value, depth - 1)))
                except AttributeError:
                    yield key, value
            else:
                yield (key, value)


def getone(dct: ListDict, key, *subkeys):
    """return one and only one value for a key in a dictionary of lists.
    repeat on the value recusively for all subkeys
    """
    value = dct[key]
    if len(value) != 1:
        raise MultipleValues("key {!r} has {} values".format(key, len(value)))
    if subkeys:
        return getone(value[0], *subkeys)
    else:
        return value[0]
