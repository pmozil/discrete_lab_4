"""
The lz77 encoder/decoder module
"""
from collections.abc import Sequence
from typing import Any

from base_encoder import BaseCompressor, BaseDecoder, BaseEncoder


class LZ77Encoder(BaseEncoder):
    """
    The lz77 Encoder

    Methods:
        encode(stream: Sequence) -> Sequence: encodes the stream with lz77
    """

    def __init__(self, buffer_len: int = 128):
        """
        The init for the lz77 encoder
        """
        self._buffer_len = buffer_len
        self._buffer = []

    def _longest_sequence(self, stream: Sequence) -> tuple[int, int]:
        """
        Get longest sequence from the buffer
        """
        cur_len: int = 1
        match: bool = False
        buf_idx = 0
        result_idx = 0
        while (buf_idx + cur_len) < (len(self._buffer)):
            if [ch for ch in stream[:cur_len]] == self._buffer[
                buf_idx : (buf_idx + cur_len)
            ]:
                match = True
                result_idx = buf_idx
                if [ch for ch in stream[: cur_len + 1]] == self._buffer[
                    buf_idx : (buf_idx + cur_len + 1)
                ]:
                    cur_len += 1
                else:
                    buf_idx += 1
            else:
                buf_idx += 1
        return (result_idx, cur_len) if match and cur_len >= 3 else (0, 0)

    def encode(self, stream: Sequence) -> Sequence:
        """
        Encode the given stream

        Args:
            stream: Sequence - the stream of data

        Returns:
            Sequence - the encoded data
        """
        self._buffer = []
        encoded_stream: Sequence[tuple[int, int] | Any] = []
        while stream:
            compression_info: tuple[int, int] = self._longest_sequence(stream)
            if compression_info[1] > 0:
                dist = compression_info[0] - len(self._buffer)
                step = compression_info[1]
                encoded_stream.append((dist, step))
            else:
                step = 1
                symbol = stream[0]
                encoded_stream.append(symbol)
            self._buffer += stream[:step]
            min_index = (
                len(self._buffer) - self._buffer_len - 1
                if len(self._buffer) > self._buffer_len
                else 0
            )
            self._buffer = self._buffer[min_index:]
            stream = stream[step:]
        return encoded_stream


class LZ77Decoder(BaseDecoder):
    """
    The LZ77 decoder class

    Methods:
        decode(encoded_stream: Sequence) -> Sequence: decode the lz77 code
    """

    @staticmethod
    def decode(encoded_stream: Sequence[tuple[int, int, str]]) -> Sequence:
        """
        Decode the LZ77-compressed stream
        """
        decoded_stream = []
        for symbol in encoded_stream:
            if isinstance(symbol, tuple):
                for ch in decoded_stream[symbol[0] :][: symbol[1]]:
                    decoded_stream += [ch]
            else:
                decoded_stream.append(symbol)

        return decoded_stream


class LZ77Compressor(BaseCompressor):
    """
    The lz77 compressor

    Attributes:
        data - the data thet the compress stores.
            It is stored compressed and it is decoded on using the property
    """

    def __init__(self, buffer_len: int = 128):
        """
        Init method for the LZ77Compressor
        """
        self._encoder = LZ77Encoder(buffer_len)
        self._decoder = LZ77Decoder()
        self._data = []

    @property
    def data(self) -> Sequence:
        """
        Getter for the stored data

        Returns:
            Sequence - the decoded data
        """
        return self._decoder.decode(self._data)

    @data.setter
    def data(self, data: Sequence):
        """
        Setter for the stored data
        """
        self._data = self._encoder.encode(data)


# import sys

# lz77 = LZ77Compressor(5)
# string = "AAAABCAABAABCD"
# lz77.data = string
# print(sys.getsizeof(lz77._data))
# print(sys.getsizeof(string))
