import math
import functools
import logging
from bits.exceptions import BitError


_logger = logging.getLogger('bits')
_logger.setLevel(50)
_handler = logging.StreamHandler()
_formatter = logging.Formatter('')
_handler.setLevel(logging.DEBUG)
_handler.setFormatter(_formatter)
_logger.addHandler(_handler)
_logger.debug('Starting')


def log(func):
    """Any time a function with this decoration is called
    it will automatically be logged at DEBUG level
    """

    @functools.wraps(func)
    def log_function(*args, **kwargs):
        message = func.__name__ + '('
        for count, arg in enumerate(args):
            message += str(arg)
            if count > 1:
                message += ', '
        for count, key in enumerate(kwargs):
            if args:
                message += ', '
            message += '{}={}'.format(key,kwargs[key])
            if count > 1:
                message += ', '
        message += ')'

        _logger.debug(message)
        return func(*args, **kwargs)
    return log_function


def sign_bit(val: int) -> int:
    """Get the sign bit from a value

    Args:
        val (int): value to extract sign bit from

    Returns:
        int: 1 if value is negative, otherwise 0
    """

    return 1 if val < 0 else 0

def min_bits(val: int) -> int:
    """Get the minimum number of bits needed to represent a value

    Args:
        val (int): value to test

    Returns:
        int: number of bits
    """

    bits = val.bit_length() + sign_bit(val)
    _logger.debug(f"Minimum of {bits} bits")
    return bits

def min_bytes(val: int) -> int:
    """Get the minimum number of bytes needed to represent a value

    Args:
        val (int): value to test

    Returns:
        int: number of bytes
    """

    bits = min_bits(val)
    nbytes = math.ceil(bits / 8) # Rounds up
    _logger.debug(f"Minimum of {nbytes} bytes")
    return nbytes

def max_uvalue(nbits: int = None, nbytes: int = None) -> int:
    """Get the largest unsigned value that can by represented by n bits

    Args:
        nbits (int, optional): number of bits. Defaults to None.
        nbytes (int, optional): number of bytes. Defaults to None.

    Raises:
        BitError: incompatible bit and byte numbers

    Returns:
        int: largest value
    """

    if nbytes != None and nbits != None:
        if nbytes * 8 != nbits:
            raise BitError(f"Incompatible bytes ({nbytes}) and nbits ({nbits})")
        bits = nbits
    elif nbytes != None:
        bits = nbytes * 8
    elif nbits != None:
        bits = nbits
    else:
        raise BitError(f"max_uvalue requires at least one argument")

    return (1 << bits) - 1

def max_svalue(nbits: int = None, nbytes: int = None) -> int:
    """Get the largest signed value that can by represented by n bits

    Args:
        nbits (int, optional): number of bits. Defaults to None.
        nbytes (int, optional): number of bytes. Defaults to None.

    Raises:
        BitError: incompatible bit and byte numbers

    Returns:
        int: largest value
    """

    if nbytes != None and nbits != None:
        if nbytes * 8 != nbits:
            raise BitError(f"Incompatible bytes ({nbytes}) and nbits ({nbits})")
        bits = nbits
    elif nbytes != None:
        bits = nbytes * 8
    elif nbits != None:
        bits = nbits
    else:
        raise BitError(f"max_svalue requires at least one argument")

    return (1 << bits-1) - 1


@log
def uint(val: int, nbytes: int = None, nbits: int = None) -> int:
    """Convert value to unsigned int

    Args:
        val (int): value to convert
        bytes (int, optional): number of bytes (at least 1)
        nbits (int, optional): number of bits (at least 1)

    Raises:
        BitError: invalid number of bits

    Returns:
        int: result of conversion
    """

    if nbytes != None  and nbits != None:
        if nbytes * 8 != nbits:
            raise BitError(f"Incompatible bytes ({nbytes}) and nbits ({nbits})")
    elif nbytes != None:
        if nbytes < 1:
            raise BitError('Unsigned integer must have at least one byte')
        elif nbytes < min_bytes(val):
            raise BitError(f'{val} can not fit in {nbytes} byte{"s" if nbytes > 1 else ""}')
        nbits = nbytes * 8
    elif nbits != None:
        if nbits < 1:
            raise BitError('Unsigned integer must have at least one bit')
        elif nbits < min_bits(val):
            raise BitError(f'{val} can not fit in {nbits} bit{"s" if nbits > 1 else ""}')
    else:
        nbits = min_bytes(val) * 8
        _logger.debug(f"Defaulting to {nbits} bits")   

    if val < 0:
        val = (1 << nbits) + val

    _logger.debug(f'uint({val}, {nbits}): {val:0{nbits}b} ({val})')
    return val

@log
def sint(val: int, nbytes: int = None, nbits: int = None) -> int:
    """Convert value to signed int

    Args:
        val (int): value to convert
        bytes (int, optional): number of bytes (at least 1)
        nbits (int, optional): number of bits (at least 2)

    Raises:
        BitError: invalid number of bits

    Returns:
        int: result of conversion
    """

    if nbytes != None and nbits != None:
        if nbytes * 8 != nbits:
            raise BitError(f"Incompatible bytes ({nbytes}) and nbits ({nbits})")
    elif nbytes != None:
        if nbytes < 1:
            raise BitError('Signed integer must have at least one byte')
        nbits = nbytes * 8
    elif nbits != None:
        if nbits < 2:
            raise BitError('Signed integer must have at least two bits')
    else:
        nbits = min_bytes(val) * 8
        _logger.debug(f"Defaulting to {nbits} bits")

    if val >> (nbits - 1) == 1:
        val = val - (1 << nbits)


    _logger.debug(f'sint({val}, {nbits}): {val}')
    return val

def get_bits(val: int, bit: int, end: int = None, length: int = None):
    if length != None and end != None:
        if length != end-bit:
            raise BitError(f"Incompatible length {length} and end {end}")
        num_bits = length
    elif length != None:
        num_bits = length
    elif end != None:
        num_bits = end - bit
    else:
        num_bits = 1

    mask = (1 << num_bits) - 1
    ret = (val >> bit) & mask

    _logger.debug(f'sint({val}, {bit}, {end}, {length}): {ret}')
    return ret