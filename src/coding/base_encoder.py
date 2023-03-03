"""
The base encoder/decoder module

It contains the ABC for the encoder class
"""

from collections.abc import Sequence
from abc import ABC, abstractmethod

class BaseEncoder(ABC):
    """
    The encoder abstract base class.
    """
    @abstractmethod
    def encode(self, stream: Sequence) -> Sequence:
        """
        Encode the data and store it in the class

        Args:
            stream: str - the data to encode
        Returns:
            str - the encoded data
        """
        ...

class BaseDecoder(ABC):
    """
    The decoder abstract base class
    """
    @staticmethod
    @abstractmethod
    def decode(stream: Sequence) -> Sequence:
        """
        Decode the data

        Args:
            stream: the encoded data
        Returns:
            str - the decoded data
        """
        ...

class BaseCompressor(ABC):
    """
    The base compressor class
    """
    @abstractmethod
    def encode(self, stream: Sequence) -> Sequence:
        """
        Encode the data and store it in the class

        Args:
            stream: str - the data to encode
        Returns:
            str - the encoded data
        """
        ...

    @abstractmethod
    def decode(self, stream: Sequence) -> Sequence:
        """
        Decode the data

        Args:
            stream: the encoded data
        Returns:
            str - the decoded data
        """
        ...

    @property
    @abstractmethod
    def value(self) -> Sequence:
        """
        Get the encoder's stored data (decoded)

        Returns:
            str - The decoded data
        """
        ...
