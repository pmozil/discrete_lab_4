"""
The deflate encoder/decoder module
"""
from collections.abc import Sequence
from typing import Any

from base_encoder import BaseCompressor, BaseDecoder, BaseEncoder
from huffmann import HuffmannCompressor
from lz77 import LZ77Compressor
