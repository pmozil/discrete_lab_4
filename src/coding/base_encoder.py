"""
The base encoder/decoder module

It contains the ABC for the encoder class
"""

from abc import ABC, abstractmethod
from collections.abc import Sequence


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


class BaseCompressor(ABC):
    """
    The base compressor class
    """

    @property
    @abstractmethod
    def data(self) -> Sequence:
        """
        Get the encoder's stored data (decoded)

        Returns:
            Sequence - The decoded data
        """
        ...

    @data.setter
    @abstractmethod
    def data(self, data: Sequence):
        """
        Setter for the stored data
        """
        ...
