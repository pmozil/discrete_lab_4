import pickle
from typing import Any


class BytesIO:
    """
    The IO class for writing and decoding data.
    Only writte to make deflate look like deflate.
    """

    @staticmethod
    def write_data_to_file(fname: str, info: list[tuple[int, int]]):
        """
        Write a huffmann-encoded thing into a file. Why?
        Probably because I hate myself
        """
        result = bytes()
        with open(fname, "wb") as out:
            for prefix, elem in info:
                result += prefix.to_bytes(2, "little") + elem.to_bytes(
                    128, "little"
                )
            out.write(result)

    @staticmethod
    def write_dict_to_file(fname: str, alp: dict[bytes, Any]):
        """
        Yeah, i made this a different file, AND with pickle. so what?
        """
        with open(fname, "wb") as out:
            pickle.dump(alp, out)

    @staticmethod
    def read_dict_from_file(fname: str) -> dict[bytes, Any]:
        """
        Yeah, i made this a different file, AND with pickle. so what?
        """
        with open(fname, "rb") as out:
            return pickle.load(out)

    @staticmethod
    def read_data_from_file(fname: str) -> list[tuple[int, int]]:
        result = []
        with open(fname, "rb") as inp:
            while info := inp.read(130):
                result.append(
                    (
                        int.from_bytes(info[:2], "little"),
                        int.from_bytes(info[2:], "little"),
                    )
                )

        return result

    @staticmethod
    def read_to_int_list(fname: str, byte_len: int = 1) -> list[int]:
        result = []
        with open(fname, "rb") as inp:
            while info := inp.read(byte_len):
                result.append(int.from_bytes(info, "little"))

        return result

    @staticmethod
    def write_ints_to_file(fname: str, info: list[int], byte_len: int = 1):
        """
        Write a huffmann-encoded thing into a file. Why?
        Probably because I hate myself
        """
        result = bytes()
        with open(fname, "wb") as out:
            for prefix in info:
                result += prefix.to_bytes(byte_len, "little")
            out.write(result)
