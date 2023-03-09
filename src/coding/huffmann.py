"""
The Huffmann encoder/decoder module
"""
from collections import Counter
from collections.abc import Sequence
from concurrent.futures import ThreadPoolExecutor
from functools import partial
from typing import Any

from base_encoder import BaseCompressor, BaseDecoder, BaseEncoder


class HuffmannTree:
    """
    The Huffmann Tree node
    """

    def __init__(self, left: "HuffmannTree | str", right: "HuffmannTree | str"):
        self.left = left
        self.right = right


class HuffmannEncoder(BaseEncoder):
    """
    The Huffmann tree class

    Methods:
        encode(stream: Sequence) -> Sequence: encodes the stream with Huffmann Code
    """

    def encode(self, stream: Sequence) -> list[int]:
        """
        Encode the given stream

        Args:
            stream: Sequence - the stream of data

        Returns:
            Sequence - the encoded data
        """
        nodes: list[tuple[Any, float]] = sorted(
            dict(Counter(stream)).items(), key=lambda x: x[1]
        )
        tree: HuffmannTree = self.make_tree(nodes)
        self.alphabet: dict = self.encoding_from_tree(tree)
        # result = bytearray()
        result = [0]
        for symbol in stream[::-1]:
            # result.append(self.alphabet[symbol])
            code = self.alphabet[symbol]
            result[-1] = (result[-1] << code.bit_length()) | code
            if result[-1].bit_length() >= 3600:
                result.append(0)
        self.alphabet = {val: key for key, val in self.alphabet.items()}
        # return bytes(result)
        return result[::-1]

    @staticmethod
    def make_tree(nodes: list[tuple[Any, float]]) -> HuffmannTree:
        """
        Make a huffmann tree from
        """
        while len(nodes) > 1:
            (sym_1, freq_1) = nodes[0]
            (sym_2, freq_2) = nodes[1]
            nodes = nodes[2:]
            node = HuffmannTree(sym_1, sym_2)
            nodes.append((node, freq_1 + freq_2))
        return nodes[0][0]

    def encoding_from_tree(
        self, node: HuffmannTree | str, code: int = 1
    ) -> dict[Any, int]:
        """
        Create an encoding for the given huffmann tree
        """
        if not isinstance(node, HuffmannTree):
            return {node: code}
        result = {}
        result.update(self.encoding_from_tree(node.left, code << 1 | 1))
        result.update(self.encoding_from_tree(node.right, code << 1))
        return result


class HuffmannDecoder(BaseDecoder):
    """
    The class for the huffmann decoder

    Methods:
        decode(encoded_stream: Sequence, alphabet: dict[Any, str]) -> Sequence: decode the Huffmann code
    """

    def decode(self, encoded_stream: list[int], alphabet: dict[int, Any]):
        """
        Decode the Huffmann code
        """
        # result = []
        # while encoded_stream:
        #     for code, symbol in alphabet.items():
        #         if encoded_stream[0] == code:
        #             result.append(symbol)
        #             encoded_stream = encoded_stream[1:]
        #             break
        #     else:
        #         break

        result = []
        with ThreadPoolExecutor(max_workers=10) as executor:
            substrings = executor.map(
                partial(self.decode_symbol, alphabet), encoded_stream
            )
        for substring in substrings:
            result.extend(substring)
        return result

    @staticmethod
    def decode_symbol(alphabet: dict[int, Any], i: int) -> list[Any]:
        result = []
        while i != 0:
            for code, symbol in alphabet.items():
                if (i & ((1 << code.bit_length()) - 1)) == code:
                    i = i >> (code.bit_length())
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
        self._data: list[int] = []

    @property
    def data(self) -> Sequence:
        """
        Getter for the data
        """
        return self._decoder.decode(self._data, self._encoder.alphabet)

    @data.setter
    def data(self, stream: Sequence):
        """
        Setter for the data
        """
        self._data = self._encoder.encode(stream)
