Based on Norman J Wildberger's 'A multiset approach to arithmetic', Math Foundations videos 227, 228, and 229.


```python
from MSetMulti import *
```

An empty MultiSet or MSet is MSet(). MSet's can be nested arbitrarily.


```python
print(MSet())
print(MSet(MSet()))
print(MSet(MSet(MSet())))
print(MSet(MSet([MSet(),MSet(),MSet()])))
```

    []
    [[]]
    [[[]]]
    [[[][][]]]


A utility function MS() is provided which converts textual descriptions of MultiSets into a nested hierarchy of MSets(). Another function C() presents the MSets in a more compact form. Several formatting functions are available that present different views of the same data.

A natural number is a pure MSet() containing that number of empty MSets and this is reflected in the C() and FN() formats.


```python
a = MS("[[][[]][[[]]][[][][]]]")
print(a)
print(C(a))
print(FZ(a))
print(FN(a))
```

    [[][[]][[[]]][[][][]]]
    [0 1 [1] 3]
    [0[0][[0]][000]]
    [0 1 [1] 3]


MSets support basic arithmetic, and the format supports specifying MSets using simply integer counting via 'x'. Note that this is not direct multiplication - 3x0 is 0 0 0, not 0.

Addition of MSets is accomplished by combining their contents. Multiplication is cross-wise addition of all elements. Caret/Exponentiation if cross-wise multiplication of all elements.


```python
a = MS("[[][0][0 0][0 0 0]]")
b = MS("[[][0][2x0][3x0]]")
print(a,b)
print(C(a),C(b))
print(a+b)
print(C(a+b))
print(a*b)
print(FZ(a*b))
print(FN(a*b))
print(C(a*b))
print(a^b)
print(FZ(a^b))
print(FN(a^b))
print(C(a^b))
```

    [[][[]][[][]][[][][]]] [[][[]][[][]][[][][]]]
    [0 1 2 3] [0 1 2 3]
    [[][[]][[][]][[][][]][][[]][[][]][[][][]]]
    [2x0 2x1 2x2 2x3]
    [[][[]][[][]][[][][]][[]][[][]][[][][]][[][][][]][[][]][[][][]][[][][][]][[][][][][]][[][][]][[][][][]][[][][][][]][[][][][][][]]]
    [0[0][00][000][0][00][000][0000][00][000][0000][00000][000][0000][00000][000000]]
    [0 1 2 3 1 2 3 4 2 3 4 5 3 4 5 6]
    [0 2x1 3x2 4x3 3x4 2x5 6]
    [[][][][][][[]][[][]][[][][]][][[][]][[][][][]][[][][][][][]][][[][][]][[][][][][][]][[][][][][][][][][]]]
    [00000[0][00][000]0[00][0000][000000]0[000][000000][000000000]]
    [0 0 0 0 0 1 2 3 0 2 4 6 0 3 6 9]
    [7x0 1 2x2 2x3 4 2x6 9]


Alpha is defined as an element in the parser, and can be defined as a variable:


```python
?? = MSet(MSet(MSet()))
print(??+??,2*??,3*??)
print(FN(??+??),FN(2*??),FN(3*??))
print(??^2)
print(C(??^2))
print(f"??^3={C(??^3)}")
```

    [[[]][[]]] [[[]][[]]] [[[]][[]][[]]]
    [1 1] [1 1] [1 1 1]
    [[[][]]]
    [2]
    ??^3=[3]


The parser understands alpha notation, with the caveat that there is no easy way to achieve super and sub-scripts in Python. Therefore, a trailing integer is taken as the alpha subscript, and caret notation is used for the superscript/exponentiation. The use of an actual variable alpha assigned the appropriate value allows computations to be entered directly in Python, but note that the order of the output may be altered, as no sorting is done.


```python
?? = MSet(MSet(MSet()))
print(2+??)
print(??+2)
a = 2+(3*??)+(??^2)+(4*??^3)
b = MS("2") + MS("3??") + MS("??^2") + MS("4??^3")
print(C(a),C(b))

print("??0??1^2 + ??2^3??4 + 2??5^3")
print(MS("??0")*MS("??1^2") + MS("??2^3")*MS("??4") + MS("2??5^3"))
print(FZ(MS("??0")*MS("??1^2") + MS("??2^3")*MS("??4") + MS("2??5^3")))
print(FN(MS("??0")*MS("??1^2") + MS("??2^3")*MS("??4") + MS("2??5^3")))
print(C(MS("??0")*MS("??1^2") + MS("??2^3")*MS("??4") + MS("2??5^3")))

```

    [[[]][][]]
    [[[]][][]]
    [3x1 2x0 2 4x3] [2x0 3x1 2 4x3]
    ??0??1^2 + ??2^3??4 + 2??5^3
    [[[][[]][[]]][[[][]][[][]][[][]][[][][][]]][[[][][][][]][[][][][][]][[][][][][]]][[[][][][][]][[][][][][]][[][][][][]]]]
    [[0[0][0]][[00][00][00][0000]][[00000][00000][00000]][[00000][00000][00000]]]
    [[0 1 1] [2 2 2 4] [5 5 5] [5 5 5]]
    [[0 2x1] [3x2 4] 2x[3x5]]

