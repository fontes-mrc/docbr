from time import perf_counter_ns
from typing import (
    Callable,
    List,
)

import validate_docbr as vbr
from prettytable import PrettyTable
from pyarrow.parquet import read_table

import docbr as dbr
from docbr import doctypes as dt


def perf_timer(f: Callable, args: tuple) -> str:
    def format_elapsed_time(time_ns: int) -> str:
        unit_list = ["ns", "µs", "ms", "s"]
        divisors = [1, 1000, 1000000, 1000000000]
        for i in range(len(divisors)):
            if time_ns < divisors[i] * 1000 or i == len(divisors) - 1:
                return f"{time_ns / divisors[i]:.2f} {unit_list[i]}"
        return "0.00 ns"

    times = []
    for _ in range(10):
        start = perf_counter_ns()
        f(*args)
        end = perf_counter_ns()
        times.append(end - start)

    return format_elapsed_time(min(times))


def get_function(key: str) -> dict:
    if key == "CPF":
        return {
            "validate_docbr": vbr.CPF().validate_list,
            "docbr": dbr.validate,
            "docbr_doctype": dt.CPF,
        }

    elif key == "CNPJ":
        return {
            "validate_docbr": vbr.CNPJ().validate_list,
            "docbr": dbr.validate,
            "docbr_doctype": dt.CNPJ,
        }

    elif key == "CNH":
        return {
            "validate_docbr": vbr.CNH().validate_list,
            "docbr": dbr.validate,
            "docbr_doctype": dt.CNH,
        }

    elif key == "PIS":
        return {
            "validate_docbr": vbr.PIS().validate_list,
            "docbr": dbr.validate,
            "docbr_doctype": dt.PIS,
        }

    elif key == "TE":
        return {
            "validate_docbr": vbr.TituloEleitoral().validate_list,
            "docbr": dbr.validate,
            "docbr_doctype": dt.T_ELEITOR,
        }

    elif key == "RENAVAM":
        return {
            "validate_docbr": vbr.RENAVAM().validate_list,
            "docbr": dbr.validate,
            "docbr_doctype": dt.RENAVAM,
        }

    else:
        raise ValueError(f"Invalid key: {key}")


def run_tests(key: str, values: List[str], masked: bool = False) -> dict:
    funcs = get_function(key)

    print(f"Running {key} against validate_docbr")
    i1 = perf_timer(funcs["validate_docbr"], (values,))

    print(f"Running {key} against docbr")
    i2 = perf_timer(funcs["docbr"], (values, funcs["docbr_doctype"], False))

    print(f"Running {key} against docbr - lazy")
    i3 = perf_timer(funcs["docbr"], (values, funcs["docbr_doctype"], True))

    return {
        "doctype": f"{key} - {'masked' if masked else 'unmasked'}",
        "validate_docbr": i1,
        "docbr": i2,
        "docbr_lazy": i3,
    }


# parquet with 1.000.000 valid and masked documents of each type
masked_data: dict = read_table("benchmark/masked.parquet").to_pydict()
masked_keys: list = list(masked_data.keys())

# parquet with 1.000.000 valid and unmasked documents of each type
unmasked_data: dict = read_table("benchmark/unmasked.parquet").to_pydict()
unmasked_keys: list = list(unmasked_data.keys())

results: list = []

for key in unmasked_keys:
    if key == "CNS":  # CNS is not yet implemented by docbr
        continue
    values = unmasked_data[key]
    result = run_tests(key, values, masked=False)
    results.append(result)
    print(result)

for key in masked_keys:
    if key == "CNS":  # CNS is not yet implemented by docbr
        continue
    values = masked_data[key]
    result = run_tests(key, values, masked=True)
    results.append(result)
    print(result)

print("\n\n")

table = PrettyTable()
table.field_names = ["doctype", "validate_docbr", "docbr", "docbr - lazy"]
for result in results:
    table.add_row(
        [
            result["doctype"],
            result["validate_docbr"],
            result["docbr"],
            result["docbr_lazy"],
        ]
    )

print(table)
