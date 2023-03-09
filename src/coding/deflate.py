"""
The deflate encoder/decoder module
"""
from collections.abc import Sequence
from typing import Any

from base_encoder import BaseCompressor, BaseDecoder, BaseEncoder
from huffmann import HuffmannDecoder, HuffmannEncoder
from lz77 import LZ77Decoder, LZ77Encoder


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

    def __init__(self, buf_size: int = 128):
        """Init for the encoder"""
        self._huffmann = HuffmannEncoder()
        self._lz77 = LZ77Encoder(buf_size)

    def encode(self, stream: Sequence) -> list[int]:
        """Encode the stream"""
        result = self._huffmann.encode(self._lz77.encode(stream))
        self.alphabet = self._huffmann.alphabet
        del self._huffmann.alphabet
        return result


class DeflateDecoder(BaseDecoder):
    """
    The decoder for the deflate class
    """

    def __init__(self):
        """Init for the decoder"""
        self._huffmann = HuffmannDecoder()
        self._lz77 = LZ77Decoder()

    def decode(
        self, encoded_stream: list[int], alphabet: dict[int, Any]
    ) -> Sequence:
        """Decode the stream"""
        return self._lz77.decode(
            self._huffmann.decode(encoded_stream, alphabet)
        )


class DeflateCompressor:
    """The compressor class"""

    def __init__(self, buf_size: int = 128):
        """Init for the class"""
        self._encoder = DeflateEncoder(buf_size)
        self._decoder = DeflateDecoder()
        self._data: list[int] = []
        self.alphabet: dict[int, Any] = {}

    @property
    def data(self) -> Sequence:
        """Get the data"""
        return self._decoder.decode(self._data, self.alphabet)

    @data.setter
    def data(self, data: Sequence):
        """Encode the data"""
        self._data = self._encoder.encode(data)
        self.alphabet = self._encoder.alphabet
