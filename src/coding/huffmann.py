"""
The Huffmann encoder/decoder module
"""
from collections import Counter
from collections.abc import Sequence
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

    def encode(self, stream: Sequence) -> Sequence:
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
        result = ""
        for symbol in stream:
            result += self.alphabet[symbol]
        self.alphabet = {val: key for key, val in self.alphabet.items()}
        return result

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
        self, node: HuffmannTree | str, code=""
    ) -> dict[Any, str]:
        """
        Create an encoding for the given huffmann tree
        """
        if isinstance(node, str):
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

    @staticmethod
    def decode(encoded_stream: Sequence, alphabet: dict[str, Any]):
        """
        Decode the Huffmann code
        """
        result = []
        while encoded_stream:
            for code, symbol in alphabet.items():
                if encoded_stream[: len(code)] == code:
                    result.append(symbol)
                    encoded_stream = encoded_stream[len(code) :]
                    break
            else:
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
        self._data = []

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
