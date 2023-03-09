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

    def encode(self, stream: Sequence) -> list[tuple[int, int]]:
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
        result = [""]
        for symbol in stream[::-1]:
            # result.append(self.alphabet[symbol])
            code = self.alphabet[symbol]
            # result[-1] = (result[-1] << code.bit_length()) | code
            result[-1] = code + result[-1]
            if len(result[-1]) >= 3600:
                result.append("")
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
        self, node: HuffmannTree | str, code: str = "0"
    ) -> dict[Any, str]:
        """
        Create an encoding for the given huffmann tree
        """
        if not isinstance(node, HuffmannTree):
            return {node: code}
        result = {}
        result.update(self.encoding_from_tree(node.left, code + "0"))
        result.update(self.encoding_from_tree(node.right, code + "1"))
        return result


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
