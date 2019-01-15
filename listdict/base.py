# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
import typing as t

__ALL__ = ["Pair", "ListDict", "append", "mk", "iter", "getone"]

Pair = t.Tuple[t.Any, t.Any]
ListDict = t.Dict[t.Any, t.MutableSequence]


class MultipleValues(Exception):
    pass


def append(dct: ListDict, key, value):
    """you have a dictionary of lists. append a value to the list of
    key.
    """
    dct.setdefault(key, []).append(value)


def mk(data: t.Iterable, *parsers, idx=0) -> ListDict:
    """take an iterable of key-value pairs and construct a dictionary
    of lists of the values. calls itself recursively on the values
    ``recurse`` number of times.
    """
    dct = {}
    for key, value in map(parsers[idx], data):
        if idx < len(parsers) - 1:
            value = mk(value, *parsers, idx=idx + 1)
        append(dct, key, value)
    return dct


def iter(dct: ListDict, depth=0):
    """you have a dictionary of lists. Get tuples of key and value for
    each value in each list. values will be recursively unpacked as ListDicts
    ``recurse`` number of times.
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
