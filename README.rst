listdict
========

.. contents::

Many libraries use data formats in the MARC tradition. At the time of
this writting, the Frankfurt Universtity Library uses Pica+, but this is
also a MARC-style format, though the field names are entirely different.

MARC data is organized into fields, and each field contains subfields.
Fields can be repeated within the record, and likewise subfields can be
repeated in the field. This data is quite natural to present in XML, but
is less intuitive to model in JSON, which is a bit annoying, since JSON
data is much simpler to model in most dynamic programming languages,
which typically provide native mapping and dynamic array
types–e.g. objects and arrays in JavaScript or dictionaries and lists in
Python.

The consensus (in our office) is that the way to deal with this in
Python is using a dictionary of lists of dictionaries of lists of
values.

That is, the record is a dictionary of lists of fields, and each field
is a dictionary of lists of subfields.

Say we have a recored like this (and we have):

::

   002@ ƒ0Aauc
   003O ƒaOCoLCƒ0180456939
   004A ƒ0965-411-010-5
   007A ƒaHEBƒ0018270948
   010@ ƒaheb
   011@ ƒa1991ƒn1991
   013H ƒ0z
   015@ ƒ00
   021A ƒT01ƒULatnƒa@Mā anāšîm lô ʿôśîm bišvîl ahavāƒhIttî Nāwe
   021A ƒT01ƒUHebrƒaמה אנשים לא עושים בשביל אהבהƒhאתי נוה
   028A ƒ9162803451ƒ8Nāwe, Ittî [Tnx]
   033A ƒpTēl-ĀvîvƒnʿEqed
   034D ƒa48 S.
   037A ƒaÜbers. d. Hauptsacht.: Was Menschen nicht für Liebe machen
   046L ƒaIn hebr. Schr
   046M ƒaGedichte
   047A ƒrOriginalschrift durch autom. Retrokonversion
   101@ ƒa3
   101B ƒ005-08-16ƒt11:16:21.000
   145S/06 ƒa760
   145Z/01 ƒaZ-sl
   145Z/02 ƒa907 900 M 0659 e Nāwe, I.
   208@/01 ƒa07-11-91ƒbhAa
   201B/01 ƒ027-01-02ƒt14:55:37.677
   203@/01 ƒ0025989448
   209A/01 ƒa84.708.40ƒf000ƒduƒh84 708 40ƒx00
   209G/01 ƒa84708402ƒx00
   247C/01 ƒ9102598258ƒ8601000-3 <30>Frankfurt, Universitätsbibliothek J. C. Senckenberg, Zentralbibliothek (ZB)

According to the above logic, it should be represented in like this:

.. code:: ipython3

    record = {'002@': [{'0': ['Aauc']}],
     '003O': [{'0': ['180456939'], 'a': ['OCoLC']}],
     '004A': [{'0': ['965-411-010-5']}],
     '007A': [{'0': ['018270948'], 'a': ['HEB']}],
     '010@': [{'a': ['heb']}],
     '011@': [{'a': ['1991'], 'n': ['1991']}],
     '013H': [{'0': ['z']}],
     '015@': [{'0': ['0']}],
     '021A': [{'T': ['01'],
               'U': ['Latn'],
               'a': ['@Mā anāšîm lô ʿôśîm bišvîl ahavā'],
               'h': ['Ittî Nāwe']},
              {'T': ['01'],
               'U': ['Hebr'],
               'a': ['מה אנשים לא עושים בשביל אהבה'],
               'h': ['אתי נוה']}],
     '028A': [{'8': ['Nāwe, Ittî [Tnx]'], '9': ['162803451']}],
     '033A': [{'n': ['ʿEqed'], 'p': ['Tēl-Āvîv']}],
     '034D': [{'a': ['48 S.']}],
     '037A': [{'a': ['Übers. d. Hauptsacht.: Was Menschen nicht für Liebe machen']}],
     '046L': [{'a': ['In hebr. Schr']}],
     '046M': [{'a': ['Gedichte']}],
     '047A': [{'r': ['Originalschrift durch autom. Retrokonversion']}],
     '101@': [{'a': ['3']}],
     '101B': [{'0': ['05-08-16'], 't': ['11:16:21.000']}],
     '145S/06': [{'a': ['760']}],
     '145Z/01': [{'a': ['Z-sl']}],
     '145Z/02': [{'a': ['907 900 M 0659 e Nāwe, I.']}],
     '201B/01': [{'0': ['27-01-02'], 't': ['14:55:37.677']}],
     '203@/01': [{'0': ['025989448']}],
     '208@/01': [{'a': ['07-11-91'], 'b': ['hAa']}],
     '209A/01': [{'a': ['84.708.40'],
                  'd': ['u'],
                  'f': ['000'],
                  'h': ['84 708 40'],
                  'x': ['00']}],
     '209G/01': [{'a': ['84708402'], 'x': ['00']}],
     '247C/01': [{'8': ['601000-3 <30>Frankfurt, Universitätsbibliothek J. C. Senckenberg, Zentralbibliothek (ZB)'],
                  '9': ['102598258']}]}

You may rightly ask, "why do you need all those lists that only have one
item? well, normally you don’t. However, sometimes the have more than
one item. Them’s the breaks.

.. code:: ipython3

    record["021A"]




.. parsed-literal::

    [{'T': ['01'],
      'U': ['Latn'],
      'a': ['@Mā anāšîm lô ʿôśîm bišvîl ahavā'],
      'h': ['Ittî Nāwe']},
     {'T': ['01'],
      'U': ['Hebr'],
      'a': ['מה אנשים לא עושים בשביל אהבה'],
      'h': ['אתי נוה']}]



Two main titles. One in Hebrew letters and one in Romanized Hebrew.
Though I don’t believe there are any in this example, the same
shenanigans can occur in some subfields.

``listdict`` simply provides a few functions for working with these
kinds of data structures, though it supports nesting them to arbitrary
depths.

listdict.iter
-------------

.. code:: ipython3

    import listdict
    
    # lets deal with fewer fields
    record = {key: record[key] for key in ("003O", "021A", "028A")}
    
    for field in listdict.iter(record):
        print(field)


.. parsed-literal::

    ('003O', {'0': ['180456939'], 'a': ['OCoLC']})
    ('021A', {'T': ['01'], 'U': ['Latn'], 'a': ['@Mā anāšîm lô ʿôśîm bišvîl ahavā'], 'h': ['Ittî Nāwe']})
    ('021A', {'T': ['01'], 'U': ['Hebr'], 'a': ['מה אנשים לא עושים בשביל אהבה'], 'h': ['אתי נוה']})
    ('028A', {'8': ['Nāwe, Ittî [Tnx]'], '9': ['162803451']})


As you see, each repeated field gets it’s own line. To flatten the data
further, you could use two loops:

.. code:: ipython3

    for fieldname, subfields in listdict.iter(record):
        for subfname, value in listdict.iter(subfields):
            print((fieldname, subfname, value))


.. parsed-literal::

    ('003O', '0', '180456939')
    ('003O', 'a', 'OCoLC')
    ('021A', 'T', '01')
    ('021A', 'U', 'Latn')
    ('021A', 'a', '@Mā anāšîm lô ʿôśîm bišvîl ahavā')
    ('021A', 'h', 'Ittî Nāwe')
    ('021A', 'T', '01')
    ('021A', 'U', 'Hebr')
    ('021A', 'a', 'מה אנשים לא עושים בשביל אהבה')
    ('021A', 'h', 'אתי נוה')
    ('028A', '8', 'Nāwe, Ittî [Tnx]')
    ('028A', '9', '162803451')


However, this is such a normal pattern that it’s included in the
``iter`` function:

.. code:: ipython3

    for subfield in listdict.iter(record, depth=1):
        print(subfield)


.. parsed-literal::

    ('003O', '0', '180456939')
    ('003O', 'a', 'OCoLC')
    ('021A', 'T', '01')
    ('021A', 'U', 'Latn')
    ('021A', 'a', '@Mā anāšîm lô ʿôśîm bišvîl ahavā')
    ('021A', 'h', 'Ittî Nāwe')
    ('021A', 'T', '01')
    ('021A', 'U', 'Hebr')
    ('021A', 'a', 'מה אנשים לא עושים בשביל אהבה')
    ('021A', 'h', 'אתי נוה')
    ('028A', '8', 'Nāwe, Ittî [Tnx]')
    ('028A', '9', '162803451')


``depth=1`` means that the it’s a listdict of listdicts, and you want to
flatten both levels. You can nest them arbitrarility deep, but you need
to tell ``iter`` how deep to go. ``1`` should be as deep as you ever
need for MARC-style records.

listdict.getone
---------------

Because most of the lists in these data structures are only one item
long, it may be useful to avoid dealing with the list if you already
know that a certain key has only one value.

.. code:: ipython3

    listdict.getone(record, "028A")




.. parsed-literal::

    {'8': ['Nāwe, Ittî [Tnx]'], '9': ['162803451']}



This also supports arbitrary nesting.

.. code:: ipython3

    listdict.getone(record, "028A", "8")




.. parsed-literal::

    'Nāwe, Ittî [Tnx]'



However, any list on the way to the target has more than one item, this
method throws an error:

.. code:: ipython3

    listdict.getone(record, "021A")


::


    ---------------------------------------------------------------------------

    MultipleValues                            Traceback (most recent call last)

    <ipython-input-11-f6d1dc8c3a9f> in <module>
    ----> 1 listdict.getone(record, "021A")
    

    ~/src/py/listdict/listdict/base.py in getone(dct, key, *subkeys)
         73     """return one and only one value for a key in a dictionary of lists.
         74     repeat on the value recusively for all subkeys
    ---> 75     """
         76     value = dct[key]
         77     if len(value) != 1:


    MultipleValues: key '021A' has 2 values

