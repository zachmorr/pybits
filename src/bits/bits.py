from bits.helpers import *
from bits.exceptions import BitError

"""
https://docs.python.org/3/reference/datamodel.html#special-method-names

TODO
__bytes__
__bool__
__int__

Optional
__format__
__hash__
__dir__
"""



class Bits():

    """ Properties """
    _value: int = None

    @property
    def value(self) -> int:
        return self._value

    @value.setter
    def value(self, new_value: int):
        if not isinstance(new_value, int):
            raise TypeError(f'Invalid value type {type(new_value)}')
        if min_bits(new_value) > self.nbits:
            raise BitError(f'{new_value} will not fit in {self.nbits} bits')

        self._value = new_value


    _nbits: int = None

    @property
    def nbits(self) -> int:
        return self._nbits

    @nbits.setter
    def nbits(self, new_value: int):
        if not isinstance(new_value, int):
            raise TypeError(f'Invalid nbits type {type(new_value)}')
        if new_value < min_bits(self.value):
            raise BitError(f'{new_value} is too few bits to fit {self.value}')

        self._nbits = new_value

        

    """ Initializaiton """
    def __init__(self, value:int , nbytes: int = None, nbits: int = None):
        
        # Set value
        if not isinstance(value, int):
            raise TypeError(f'Invalid type {type(value)}')

        self._value = value

        # Check that nbits is valid, or set nbits if it is not given
        if nbytes != None and nbits != None:
            if nbits != nbytes * 8:
                raise BitError(f"Incompatible nbytes ({nbytes}) and nbits ({nbits})")
            self.nbits = nbits
        elif nbits != None:
            self.nbits = nbits
        elif nbytes != None:
            self.nbits = nbytes * 8
        elif value > 0:
            self.nbits = min_bits(value)
        elif value < 0:
            self.nbits = min_bytes(value) * 8
        else:
            raise BitError("Error while calculating number of bits")



    """ Comparison Operations """
    def __lt__(self, other) -> bool:
        return self.value < other
    
    def __le__(self, other) -> bool:
        return self.value <= other
    
    def __eq__(self, other) -> bool:
        return self.value == other
    
    def __ne__(self, other) -> bool:
        return self.value != other
    
    def __gt__(self, other) -> bool:
        return self.value > other
    
    def __ge__(self, other) -> bool:
        return self.value >= other
    


    """ Math Operations """
    def __add__(self, other):
        return Bits(self.value + other)
    
    def __sub__(self, other):
        return Bits(self.value - other)
    
    def __mul__(self, other):
        return Bits(self.value * other)

    def __matmul__(self, other):
        raise NotImplementedError
    
    def __truediv__(self, other):
        return Bits(self.value / other)
    
    def __floordiv__(self, other):
        return Bits(self.value // other)
    
    def __mod__(self, other):
        return Bits(self.value % other)
    
    def __divmod__(self, other):
        raise NotImplementedError
    
    def __pow__(self, other):
        return Bits(self.value ** other)
    
    def __lshift__(self, other):
        return Bits(self.value << other)
    
    def __rshift__(self, other):
        return Bits(self.value >> other)
    
    def __and__(self, other):
        return Bits(self.value & other)
    
    def __xor__(self, other):
        return Bits(self.value ^ other)
    
    def __or__(self, other):
        return Bits(self.value | other)
    
    def __radd__(self, other):
        raise NotImplementedError
    
    def __rsub__(self, other):
        raise NotImplementedError
    
    def __rmul__(self, other):
        raise NotImplementedError

    def __rmatmul__(self, other):
        raise NotImplementedError
    
    def __rtruediv__(self, other):
        raise NotImplementedError
    
    def __rfloordiv__(self, other):
        raise NotImplementedError
    
    def __rmod__(self, other):
        raise NotImplementedError
    
    def __rdivmod__(self, other):
        raise NotImplementedError
    
    def __rpow__(self, other):
        raise NotImplementedError
    
    def __rlshift__(self, other):
        raise NotImplementedError
    
    def __rrshift__(self, other):
        raise NotImplementedError
    
    def __rand__(self, other):
        raise NotImplementedError
    
    def __rxor__(self, other):
        raise NotImplementedError
    
    def __ror__(self, other):
        raise NotImplementedError
    
    def __iadd__(self, other):
        raise NotImplementedError
    
    def __isub__(self, other):
        raise NotImplementedError
    
    def __imul__(self, other):
        raise NotImplementedError

    def __imatmul__(self, other):
        raise NotImplementedError
    
    def __itruediv__(self, other):
        raise NotImplementedError
    
    def __ifloordiv__(self, other):
        raise NotImplementedError
    
    def __imod__(self, other):
        raise NotImplementedError
    
    def __ipow__(self, other):
        raise NotImplementedError
    
    def __ilshift__(self, other):
        raise NotImplementedError
    
    def __irshift__(self, other):
        raise NotImplementedError
    
    def __iand__(self, other):
        raise NotImplementedError
    
    def __ixor__(self, other):
        raise NotImplementedError
    
    def __ior__(self, other):
        raise NotImplementedError
    
    def __neg__(self):
        raise NotImplementedError
    
    def __pos__(self):
        raise NotImplementedError
    
    def __abs__(self):
        raise NotImplementedError
    
    def __invert__(self):
        raise NotImplementedError
    
    def __index__(self):
        raise NotImplementedError
    
    def __round__(self):
        raise NotImplementedError
    
    def __trunc__(self):
        raise NotImplementedError
    
    def __floor__(self):
        raise NotImplementedError
    
    def __ceil__(self):
        raise NotImplementedError
    


    """ Sequence Operations """
    def __len__(self):
        raise NotImplementedError
    
    def __getitem__(self, key):
        raise NotImplementedError
    
    def __setitem__(self, key, value):
        raise NotImplementedError
    
    def __iter__(self):
        raise NotImplementedError
    
    def __reversed__(self):
        raise NotImplementedError
    
    def __contains__(self, item):
        raise NotImplementedError
    


    """ Print Operations """

    def __str__(self):
        return f'0b{uint(self.value, nbits=self.nbits):0{self.nbits}b}'


    def __repr__(self):
        return f'Bits(0b{uint(self.value, nbits=self.nbits):0{self.nbits}b})'