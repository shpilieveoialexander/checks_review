import re
from typing import TYPE_CHECKING, Final, List, Optional, Tuple

from sqlalchemy import asc, desc, func, inspect
from sqlalchemy.exc import ArgumentError

if TYPE_CHECKING:
    from starlette.datastructures import QueryParams

LHS_REXEG: Final[str] = r"\[(\w+)\]"

OPERATORS = {
    "is_null": lambda f: f.is_(None),
    "is_not_null": lambda f: f.isnot(None),
    "eq": lambda f, a: f == a,
    "ne": lambda f, a: f != a,
    "gt": lambda f, a: f > a,
    "lt": lambda f, a: f < a,
    "ge": lambda f, a: f >= a,
    "le": lambda f, a: f <= a,
    "like": lambda f, a: f.like(f"%{a}%"),
    "ilike": lambda f, a: f.ilike(f"%{a}%"),
    "not_ilike": lambda f, a: ~f.ilike(f"%{a}%"),
    "in": lambda f, a: f.in_(a),
    "not_in": lambda f, a: ~f.in_(a),
    "any": lambda f, a: f.any(a),
    "not_any": lambda f, a: func.not_(f.any(a)),
}

ORDER_OPERATORS = {
    "asc": lambda f: asc(f),
    "desc": lambda f: desc(f),
}


def parse_lsh(key: str) -> Tuple[str, ...]:
    coinc = re.search(LHS_REXEG, key)
    if not coinc:
        return key, "eq"
    key = key.replace(coinc.group(0), "")
    fn = "".join(w for w in coinc.group(0) if w.isalnum())
    return key, fn


def remap_query_params(query_params):
    recn = [(*parse_lsh(key), value) for key, value in query_params.multi_items()]
    return recn


def _get_valid_field_names(model) -> List[str]:
    inspect_mapper = inspect(model)
    columns = inspect_mapper.columns
    column_names = columns.keys()
    return column_names


def _prepare_filter(model, base_query, query_params):
    lsh_params = remap_query_params(query_params)
    avalible_columns = _get_valid_field_names(model)
    for key, fn, value in lsh_params:
        if key == "order_by":
            field, func = parse_lsh(value)
            if func not in ORDER_OPERATORS:
                continue
            function = ORDER_OPERATORS[func]
            if field not in avalible_columns:
                continue
            field = getattr(model, field)
            base_query = base_query.order_by(function(field))
        if fn not in OPERATORS:
            continue
        function = OPERATORS[fn]
        if key not in avalible_columns:
            continue
        field = getattr(model, key)
        base_query = base_query.filter(function(field, value))

    return base_query


def filter_sqlaclhemy_model(model, base_query, query_params):
    try:
        return _prepare_filter(model, base_query, query_params)
    except (AttributeError, ArgumentError):
        return base_query


def apply_search(
    model,
    base_query,
    query_params: Optional["QueryParams"] = None,
):
    return filter_sqlaclhemy_model(model, base_query, query_params)
