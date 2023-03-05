"""
The deflate encoder/decoder module
"""
from collections.abc import Sequence
from typing import Any

from base_encoder import BaseCompressor, BaseDecoder, BaseEncoder
from huffmann import HuffmannCompressor
from lz77 import LZ77Compressor


class DeflateEncoder(BaseEncoder):
    """
    The deflate encoder class

    This is bonkers. Am not putting multiple symbols into one byte, not in python.
    This is a demonstration of what deflate should look like, but with proper tools
    it'd be twice, if not thrice as effective. I, however, am too lazy to implement an
    array that writes data withon concern for byte boundaries, on instread of
    +==========+==========+
    | 10101001 | 10100000 |
    +==========+==========+
         |       |    /\
                       |
                    the message stops here, we have 3 symbols in 2 bytes
    We have this
    +==========+==========+==========+
    | 10100000 | 10011000 | 01000000 |
    +==========+==========+==========+
    /\
    |
    bug bad array
    (And it gets waay worse). Maybe, if I DID implement gzip fully, I'd have played around
    with this, but in this specific case, storing messages in bytes is fine.
    """

    ...
