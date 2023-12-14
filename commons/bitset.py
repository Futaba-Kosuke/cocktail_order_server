from dataclasses import dataclass
from typing import List

special_elements: List[str] = ["HOT", "SNOW_STYLE"]


@dataclass
class Bitset:
    bitset: List[str]

    def decimal_to_list(self, decimal: int) -> List[str]:
        tmp_decimal: int = decimal
        result: List[str] = []
        for elem in reversed(self.bitset):
            index = self.bitset.index(elem)
            if tmp_decimal >= 2**index:
                tmp_decimal -= 2**index
                result.append(elem)
        result.reverse()
        return result

    def list_to_decimal(self, list: List[str]) -> int:
        tmp_list: List[str] = list
        result: int = 0
        for elem in tmp_list:
            if elem in self.bitset:
                result += 2 ** self.bitset.index(elem)
        return result
