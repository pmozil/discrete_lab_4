"""
The lz77 encoder/decoder module
"""
from collections.abc import Sequence
from typing import Any
from base_encoder import BaseDecoder, BaseEncoder


class LZ7Encoder(BaseEncoder):
    """
    The lz77 Encoder
    """

    def __init__(self, buffer_len: int = 128):
        """
        The init for the lz77 encoder
        """
        self._buffer_len = buffer_len
        self._buffer = []

    def longest_sequence(self, stream: Sequence) -> tuple[int, int]:
        """
        Get longest sequence from the buffer
        """
        cur_len: int = 1
        match: bool = False
        buf_idx = 0
        result_idx = 0
        while (buf_idx + cur_len) < (len(self._buffer)):
            if [ch for ch in stream[:cur_len]] == self._buffer[buf_idx : (buf_idx + cur_len)]:
                match = True
                result_idx = buf_idx
                if (
                    [ch for ch in stream[: cur_len + 1]]
                    == self._buffer[buf_idx : (buf_idx + cur_len + 1)]
                ):
                    cur_len += 1
                else:
                    buf_idx += 1
            else:
                buf_idx += 1
        return (result_idx, cur_len) if match else (0, 0)

    def encode(self, stream: Sequence) -> Sequence:
        """
        Encode the given stream

        Args:
            stream: Sequence - the stream of data

        Returns:
            Sequence - the encoded data
        """
        self._buffer = []
        encoded_stream: Sequence[tuple[int, int, Any]] = []
        while stream:
            compression_info: tuple[int, int] = self.longest_sequence(stream)
            if compression_info[1] > 0:
                dist = compression_info[0] - len(self._buffer)
                step = compression_info[1]
                char = stream[step: step+1]
            else:
                dist = 0
                step = 0
                char = stream[0]
            encoded_stream.append((dist, step, char))
            self._buffer += stream[: step + 1]
            min_index = len(self._buffer) - self._buffer_len - 1 \
                if len(self._buffer) > self._buffer_len\
                else 0
            self._buffer = self._buffer[min_index:]
            stream = stream[step + 1 :]
        return encoded_stream


class LZ77Decoder(BaseDecoder):
    """
    The LZ77 decoder class
    """

    @staticmethod
    def decode(encoded_stream: Sequence[tuple[int, int, str]]) -> Sequence:
        """
        Decode the LZ77-compressed stream
        """
        decoded_stream = []
        for idx, step, char in encoded_stream:
            decoded_stream += decoded_stream[idx:][:step] + [char]

        return decoded_stream

enc = LZ7Encoder(5)
string = "aaabcaab"
res = enc.encode(string)
print(res)
dec = LZ77Decoder()
print(dec.decode(res))
