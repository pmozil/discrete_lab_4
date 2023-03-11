'''
Lempel-Ziv-Welch algorithm.
Here you can find 3 classes:
    LZWEncoder, LZWDecoder & LZWCompressor

Each of them responsible for encoding and decoding respectively.

Made by Dmytro Khamula & Petro Mozil.
'''

from typing import List
from base_encoder import BaseCompressor, BaseDecoder, BaseEncoder

class LZWEncoder(BaseEncoder):
    '''
    Class of encoding data

    Attributes:
        _data: data to be encoded.
        _dict: dictionary which script uses for encoding.
        You can use default dictionary which represents first 256 ASCII symbols
        or you can specify your own with particular code.

    Methods:
        encode(): main function for encoding data.
        There are two arguments by default which shouldn't be changed.
    '''
    def __init__(self, _dict: dict = {chr(k): k for k in range(256)}) -> None:
        '''
        (self, str, dict) -> None

        Initialization function for class LZWEncoder
        '''
        self._dict = _dict
        self._num = len(_dict)

    def encode(self, data, elem: str = '', encoded_data: List = []) -> List[int]:
        '''
        (self, str, List) -> List

        Main function for encoding data.
        Returns:
            A list of integers which represent encoded data.
        '''
        for char in data:
            new_code = elem + char
            if new_code in self._dict:
                elem = new_code
            else:
                encoded_data.append(self._dict[elem])
                self._dict[new_code] = self._num
                self._num += 1
                elem = char

        if elem:
            encoded_data.append(self._dict[elem])

        return encoded_data


class LZWDecoder(BaseDecoder):
    '''
    Class of decoding data

    Attributes:
        _data: data to be decoded.
        _dict: dictionary which script uses for decoding.
        You can use default dictionary which represents first 256 ASCII symbols
        or you can specify your own with particular code.

    Methods:
        decode(): main function for decoding data.
        There are two arguments by default which shouldn't be changed.
    '''
    def __init__(self, _dict: dict = {k: chr(k) for k in range(256)}) -> None:
        '''
        (self, str, dict) -> None

        Initialization function for class LZWDecoder
        '''
        self._dict = _dict
        self._num = len(_dict)


    def decode(self, data, elem: str = '', decoded_data: List = []) -> str:
        '''
        (self, str, List) -> List

        Main function for encoding data.
        Returns:
            A string which represent decoded data.
        '''
        for code in data:
            if code in self._dict:
                entry = self._dict[code]
                decoded_data.append(entry)
                if elem:
                    self._dict[self._num] = elem + entry[0]
                    self._num += 1
                elem = entry
            else:
                entry = elem + elem[0]
                decoded_data.append(entry)
                self._dict[self._num] = entry
                self._num += 1
                elem = entry[-1]

        return ''.join(decoded_data)


class LZWCompressor(BaseCompressor):
    '''
    LZW Compressor
    '''
    def __init__(self) -> None:
        '''
        (self) -> None

        Initialization function for LZWCompressor
        '''
        self._encoder = LZWEncoder()
        self._decoder = LZWDecoder()
        self._data = []

    @property
    def data(self):
        '''
        Getter for the stored data

        Returns:
            Sequence - the decoded data
        '''
        return self._decoder.decode(self._data)

    @data.setter
    def data(self, data):
        '''
        Setter for the stored data
        '''
        self._data = self._encoder.encode(data = data)



if __name__ == '__main__':

    import sys

    text = 'AAAABCAABAABCD'
    lzw = LZWCompressor()
    lzw.data = text
    print(sys.getsizeof(lzw._data))
    print(sys.getsizeof(text))