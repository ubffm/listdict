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


def addrow(dct: ListDict, row: t.Sequence):
    """add a row to a listdict recursively. The last item is the value,
    and the rest are keys.
    """
    for i in range(len(row)-2):
        key = row[i]
        lst = dct.setdefault(key, [])
        dct = {}
        lst.append(dct)
    dct.setdefault(row[-2], []).append(row[-1])


def fromrows(rows: t.Iterable[t.Sequence]):
    """creates a listdict from rows using listdict.addrow"""
    dct = {}
    for row in rows:
        addrow(dct, row)
    return dct


def mk(pairs: t.Iterable[Pair], recurse=0) -> ListDict:
    """take an iterable of key-value pairs and construct a dictionary
    of lists of the values. calls itself recursively on the values
    ``recurse`` number of times.
    """
    dct = {}
    for key, value in pairs:
        if recurse > 0:
            value = mk(value, recurse - 1)
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
