from collections import defaultdict
from typing import Any, Callable

# Different functions for sorting characteristics by different names.
sort_function = defaultdict(
    lambda: lambda x: x.value,
    {
        "fraction": lambda x: float(x.value.replace(",", ".").split(" ")[0]),
        "strength": lambda x: str(len(x.value)) + x.value,
        "frost_resistance": lambda x: str(len(x.value)) + x.value,
        "particles_content": lambda x: int(x.value),
    },
)


def get_sort_key_function_by_characteristic_name(
    characteristic_name: str,
) -> Callable[[Any], Any]:
    return sort_function[characteristic_name]
