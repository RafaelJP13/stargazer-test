from decimal import Decimal
from typing import Any, TypeAlias, cast

JSONSafe: TypeAlias = (
    dict[str, "JSONSafe"]
    | list["JSONSafe"]
    | str
    | int
    | float
    | bool
    | None
)

def make_json_safe(obj: Any) -> JSONSafe:
    if isinstance(obj, dict):
        obj_dict = cast(dict[Any, Any], obj)
        return {
            str(k): make_json_safe(v)
            for k, v in obj_dict.items()
        }

    if isinstance(obj, list):
        obj_list = cast(list[Any], obj)
        return [make_json_safe(i) for i in obj_list]

    if isinstance(obj, Decimal):
        return float(obj)

    return obj