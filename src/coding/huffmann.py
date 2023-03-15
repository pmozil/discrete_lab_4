"""
The Huffmann encoder/decoder module
"""
import heapq
from collections import Counter
from collections.abc import Sequence
from concurrent.futures import ThreadPoolExecutor
from functools import partial
from typing import Any

from base_encoder import BaseCompressor, BaseDecoder, BaseEncoder


class HuffmannEncoder(BaseEncoder):
    """
    The Huffmann tree class

    Methods:
        encode(stream: Sequence) -> Sequence: encodes the stream with Huffmann Code
    """

    def encode(self, stream: Sequence) -> list[tuple[int, int]]:
        """
        Encode the given stream

        Args:
            stream: Sequence - the stream of data

        Returns:
            Sequence - the encoded data
        """
        self.alphabet: dict = self.make_alphabet(Counter(stream))
        # result = bytearray()
        result = [""]
        for symbol in stream[::-1]:
            # result.append(self.alphabet[symbol])
            code = self.alphabet[symbol]
            # result[-1] = (result[-1] << code.bit_length()) | code
            if len(result[-1]) + len(code) > 1024:
                result[-1] = result[-1]
                result.append("")
            result[-1] = code + result[-1]
        self.alphabet = {
            val.encode("utf-8"): key for key, val in self.alphabet.items()
        }
        res = []
        for x in result:
            i = 0
            while i < len(x) - 1 and x[i] == "0":
                i += 1
            res.append((i, int(x, base=2)))
        return res[::-1]

    @staticmethod
    def make_alphabet(counter: dict[Any, int]) -> dict[str, Any]:
        """
        Make the alphabet from the given frequencies
        """
        result = {}
        freq_tree = [[freq, [symbol, ""]] for symbol, freq in counter.items()]
        heapq.heapify(freq_tree)
        while len(freq_tree) > 1:
            low = heapq.heappop(freq_tree)

            high = heapq.heappop(freq_tree)
            for val in low[1:]:
                val[1] = "0" + val[1]

            for val in high[1:]:
                val[1] = "1" + val[1]

            heapq.heappush(freq_tree, [low[0] + high[0]] + low[1:] + high[1:])
        return dict(tuple(x) for x in freq_tree[0][1:])


class HuffmannDecoder(BaseDecoder):
    """
    The class for the huffmann decoder

    Methods:
        decode(encoded_stream: Sequence, alphabet: dict[Any, str]) -> Sequence: decode the Huffmann code
    """

    def decode(self, encoded_stream: list[str], alp: dict[bytes, Any]):
        """
        Decode the Huffmann code
        """
        result = []
        alphabet = {val.decode("utf-8"): key for val, key in alp.items()}
        with ThreadPoolExecutor(max_workers=10) as executor:
            substrings = executor.map(
                partial(self.decode_symbol, alphabet), encoded_stream
            )
        for substring in substrings:
            result.extend(substring)
        return result

    @staticmethod
    def decode_symbol(alphabet: dict[str, Any], i: str) -> list[Any]:
        result = []
        while i:
            for code, symbol in alphabet.items():
                if i.startswith(code):
                    i = i[len(code) :]
                    result.append(symbol)
                    break
        return result


class HuffmannCompressor(BaseCompressor):
    """
    The compressor for the huffmann code

    Attributes:
        data: Sequence - the compressed data
    """

    def __init__(self):
        """
        The init method for HuffmannCompressor
        """
        self._encoder = HuffmannEncoder()
        self._decoder = HuffmannDecoder()
        self._data: list[tuple[int, int]] = []

    @property
    def data(self) -> Sequence:
        """
        Getter for the data
        """
        return self._decoder.decode(
            ["0" * x[0] + bin(x[1])[2:] for x in self._data],
            self._encoder.alphabet,
        )

    @data.setter
    def data(self, stream: Sequence):
        """
        Setter for the data
        """
        self._data = self._encoder.encode(stream)
