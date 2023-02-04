from textx import metamodel_from_str, textx_isinstance

#pip install textx

MSetGrammar= r'''
MSetModel:
    MSets+=MSet
;

MSet:
     C=CountedMOrPOrMOrP | A=Counted | B=Value | '[' MSets*=MSet ']' 
;

Value: value=INT;

Counted[noskipws]: count=Count 'x' MSet=MSet;

Count: /\-?\d+/;

CountedMOrPOrMOrP: CountedMOrP|CaretOrMOrP|MOrP;

CountedMOrP[noskipws]: count=Count C=CaretOrMOrP;

CaretOrMOrP[noskipws]: CaretExpr | MOrP;

Poly: 'α';

Multi[noskipws]: 'α' M=INT;

MOrP: Multi | Poly;

CaretExpr[noskipws]: A=MOrP '^' B=INT;

'''

mm = metamodel_from_str(MSetGrammar)

def mset_from_str(value=""):
    model = mm.model_from_str(value)
    return mset_from_model(model)

def mset_from_model(model):
    #print(f"m:{model}")
    if textx_isinstance(model,mm['MSetModel']):
        for k in model.MSets:
            return mset_from_model(k)
    elif textx_isinstance(model,mm['MSet']):
        if not model.A is None:
            return mset_from_model(model.A)
        if not model.B is None:
            return mset_from_model(model.B)
        if not model.C is None:
            return mset_from_model(model.C)
        cur = MSet()
        for k in model.MSets:
            cur.append(mset_from_model(k))
        return cur
    elif textx_isinstance(model,mm['Value']):
        cur = MSet()
        for n in range(model.value):
            cur.append(MSet())
        return cur
    elif textx_isinstance(model,mm['Counted']):
        l = []
        for n in range(int(model.count)):
            l.append(mset_from_model(model.MSet))
        return l
    elif textx_isinstance(model,mm['CountedMOrP']):
        c = mset_from_model(model.C)
        #print(f"C = {model.C}, c={c}, c*x={c*int(model.count)}")
        return c*int(model.count)
    elif textx_isinstance(model,mm['Poly']) or model == 'α':
        return MSet(MSet(MSet()))
    elif textx_isinstance(model,mm['Multi']):
        #print(f"M={model.M} {MSet(MSet(MSet()))} ^ {MSet(model.M)} = {(MSet(MSet(MSet()))^MSet(str(model.M)))}")
        return MSet(MSet(MSet(MSet()))^int(model.M))
    elif textx_isinstance(model,mm['CaretExpr']):
        a = mset_from_model(model.A)
        b = int(model.B)
        #print (f"a^b: a{C(a)} b{C(b)} a^b{C(a^b)}")
        return a^int(b)
    else:
        print(f"unknown model: {model}")
        return mset_from_model(model.MSets)

def MS(value=""):
    return mset_from_str(value)

class MSet:
    # N.J.Wildberger Multisets - a tree structure representing
    # a multiset/bag/box that can contain multisets
    # with understanding of the interaction of multisets of empty multisets
    # and Wildberger's Multiset based arithmetic and Natural numbers

    def __init__(self, value=None):
        self.root = dict()
        self.raw = []
        # count is ignored on the root MSet - trees, not forests
        self._count = 1
        self.depth = 0        
        self.val = ""
        self.sub = 0
        self.sup = 0
        if value != None:
            if isinstance(value,MSet):
                self.append(value)
            elif isinstance(value,list):
                self.append(value)
            elif isinstance(value,str):
                self.append(MS(value))

    def append(self, value=""):
        if isinstance(value,MSet):
#            print ("appending: ",repr(self),repr(value),repr(self.raw))
            for n in range(0,value.count()):
                self.raw.append(value)
            if value.depth+1 > self.depth:
                self.depth = value.depth+1
 #           print (repr(self),repr(value),repr(self.raw))
            c = value.canonical()
            if c in self.root:
                self.root[c]+=value.count()
            else:
                self.root[c]=value.count()
        elif isinstance(value,list):
            for k in value:
                self.append(k)

    def parse(self, value=""):
        pass

    def canonical(self):
        if len(self.root.items()) == 0:
            return '0' # [] == 0
        has_non_emptymset_or_nonmset = False
        m = ['[']
        num = 0
        for k,v in self.root.items():
            #print("k,v",k,v)
            if k != '[]' and k != '0':
                has_non_emptymset_or_nonmset = True
            num+=v
            try:
                if v > 1:
                    m.append(str(v))
                    m.append('x')
            except:
                pass
            try:
                m.append(k)
                m.append(' ')
            except:
                m.append(str(k))
                m.append(' ')
        m.append(']')
        if has_non_emptymset_or_nonmset == False:
            # [ 0 0 0 0 ] - count zeroes - natural number
            return str(num)
        return ''.join(m).replace(' ]',']')

    def __repr__(self):
        return self.canonical()

    def __str__(self,level=0):
        if level > 50:
            return "recursion too deep."
        m = ['[']
#        m.append(str(self.raw))
        for v in self.raw:
            #print(v.__repr__())
            m.append(v.__str__(level+1))
        m.append(']')
        return ''.join(m)
        
    def count(self):
        return self._count

    def set_count(self, value):
        self._count = value

    def __add__(self, value):
        if isinstance(value, MSet):
            cur = MSet()
            cur.append(self.raw)
            cur.append(value.raw)
            return cur
        elif isinstance(value, int):
            return self.__add__(MS(str(value)))
        else:
            return self.__add__(MS(str(value)))

    def __radd__(self, value):
        if isinstance(value, MSet):
            cur = MSet()
            cur.append(self.raw)
            cur.append(value.raw)
            return cur
        elif isinstance(value, int):
            return self.__add__(MS(str(value)))
        else:
            return self.__add__(MS(str(value)))

    def __mul__(self, value):
        if isinstance(value, MSet):
            cur = MSet()
            for a in self.raw:
                for b in value.raw:
                    cur.append(a+b)
            return cur
        elif isinstance(value, int):
            return self.__mul__(MS(str(value)))
        else:
            return self.__mul__(MS(str(value)))

    def __rmul__(self, value):
        return self.__mul__(value)

    def __pow__(self, value):
        if isinstance(value, MSet):
            cur = MSet()
            for a in self.raw:
                for b in value.raw:
                    cur.append(a*b)
            return cur
        elif isinstance(value, int):
            return self.__pow__(MSet(MS(str(value))))
        else:
            return self.__pow__(MSet(MS(str(value))))

    def __xor__(self, value):
        # This is the ^ caret operator in Python
        if isinstance(value, MSet):
            cur = MSet()
            for a in self.raw:
                for b in value.raw:
                    cur.append(a*b)
            return cur
        elif isinstance(value, int):
            return self.__pow__(MSet(MS(str(value))))
        else:
            return self.__pow__(MSet(MS(str(value))))

    def pure(self):
        for a in self.raw:
            if isinstance(a,MSet):
                if not a.pure():
                    return False
            else:
                return False
        return True

    def Z(self):
        if self.pure():
            return MSet()
        else:
            raise Exception("Impure MSet")

    def N(self):
        if self.pure():
            cur = MSet()
            for a in self.raw:
                cur.append(a.Z())
            return cur
        else:
            raise Exception("Impure MSet")
        
    def P(self):
        if self.pure():
            cur = MSet()
            for a in self.raw:
                cur.append(a.N())
            return cur
        else:
            raise Exception("Impure MSet")

    def M(self):
        if self.pure():
            cur = MSet()
            for a in self.raw:
                cur.append(a.P())
            return cur
        else:
            raise Exception("Impure MSet")

# Canonical - shorthand to get canonical formatting        
def C(value):
    if isinstance(value,MSet):
        return value.canonical()
    else:
        return str(value)

# Format Base - same as Str()
def FB(value):
    return str(value)

# Format Zero - show [] as 0
def FZ(value):
    return str(value).replace("[]","0")

# Format Natural - show Natural numbers
def FN(value):
    if isinstance(value,MSet):
        s = "["
        if len(value.raw) == 0:
            return "0"
        if value.depth==1:
            return str(len(value.raw))
        for M in value.raw:
            s += FN(M) + ' '
        s += ']'
        return s.replace(' ]',']')
    else:
        return str(value)

α = MSet(MSet(MSet()))

if __name__=="__main__":    
    z = MSet()
    n = MSet(MSet())
    #α = MSet(MSet(MSet()))
    
    B = MS("[[2 [4]] [0 1 1] [[0][2]]]")
    print(f"B={C(B)}")
    print(f"Z(B)={C(B.Z())}")
    print(f"N(B)={C(B.N())}")
    print(f"P(B)={C(B.P())}")
    print(f"M(B)={C(B.M())}")
    
    A = MS("[[1 2] 4]")
    B = MS("[0 [0 3]]")
    print(f"A={C(A)} B={C(B)} A^B={C(A^B)}")

    A = MS("[[1 [2]] [3]]")
    B = MS("[2 [1 3]]")
    print(f"A={C(A)} B={C(B)} A^B={C(A^B)}")
    print(f"N(A)^N(B)={C(A.N()^B.N())}")
    print(f"N(A^B)={C((A^B).N())}")
    print(f"P(A)^P(B)={C(A.P()^B.P())}")
    print(f"P(A^B)={C((A^B).P())}")
    print(f"M(A)^M(B)={C(A.M()^B.M())}")
    print(f"M(A^B)={C((A^B).M())}")

    print(f'2α1 = {C(MS("2xα1"))} = {C(MS("2α1"))}')
    print(f'3 + α1 + 4α1^2 + α1^5 = ')
    print(C(MS("3")+MS("α1")+MS("4α1^2")+MS("α1^5")))
    print(f'3 + α + 4α^2 + α^5 = ')
    print(C(MS("3")+MS("α")+MS("4α^2")+MS("α^5")))

    print("α1 + 3α2 + α3 = ")
    print(C(MS("α1")+MS("3α2")+MS("α3")))

    print("α0α1^2 + α2^3α4 + 2α5^3")
    print(C(MS("α0")*MS("α1^2") + MS("α2^3")*MS("α4") + MS("2α5^3")))

    print("[[1 5] [0 3 3]] x [2 [1 1 1]]")
    print(C(MS("[[1 5] [0 3 3]]")*MS("[2 [1 1 1]]")))
    print("(α1α5+α0α3^2) x (α0^2+α1^3)")
    print(C((MS("α1")*MS("α5")+MS("α0")*MS("α3^2"))*(MS("α0^2")+MS("α1^3"))))

