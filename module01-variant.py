#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import hashlib
import json
import random
import sys
import unicodedata
from typing import List, Dict, Tuple

DOUBLE_TAIL = "(double arr[], long long int n);"
INDEX_TAIL = "(Index arr[], long long int n);"
VOID = "void"
DOUBLE = "double"

ALGO_SORTS = ["bubble_sort", "insertion_sort", "selection_sort"]
SCORE_FUNCS = [
    "minimum",
    "maximum",
    "average",
    "median",
    "sum",
    "product",
    "geometric",
    "harmonic",
]

COMMON_STRUCTS = [
    "struct Index { long long int index; double value; };",
    "struct Product { std::string name; double prices[100]; };",
    "struct ScoredProduct { std::string name; double score; };",
]

COMMON_PROTOS = [
    "int main();",
    "void read_data(Product[] products, long long int n, long long int k);",
    "ScoredProduct convert_product(Product p, long long int k);",
]


def normalize_fio(fio: str) -> str:
    s = unicodedata.normalize("NFC", fio).strip().lower()
    return "".join(ch for ch in s if ch.isalpha())


def pick_two(rng: random.Random, items: List[str]) -> Tuple[str, str]:
    return rng.choice(items), rng.choice(items)


def generate_libs_on_the_fly(
    sort1: str, sort2: str, score1: str, score2: str, rng: random.Random
) -> List:
    # Все функции, которые распределяем по библиотекам
    funcs = ["read_data", "convert_product", sort1, sort2, score1, score2]
    # Если сортировки/оценки совпадают, оставляем только уникальные имена функций,
    # чтобы не дублировать одну и ту же функцию в разных библиотеках
    funcs = list(dict.fromkeys(funcs))

    # Кол-во библиотек: от 2 до 4 (не больше числа функций)
    total = rng.randrange(2, min(4, len(funcs)))

    # Разбивка на total непустых групп
    shuffled = funcs[:]
    rng.shuffle(shuffled)
    groups = [[] for _ in range(total)]
    for i in range(total):
        groups[i].append(shuffled[i])
    for f in shuffled[total:]:
        groups[rng.randrange(total)].append(f)

    # Типы библиотек: static (.a) или dynamic (.so)
    types = [rng.choice(["static", "dynamic"]) for _ in range(total)]

    if "static" not in types:
        idx = rng.randrange(total)
        types[idx] = "static"

    if "dynamic" not in types:
        idx = rng.randrange(total)
        types[idx] = "dynamic"

    # Сформируем метаданные библиотек
    libs = []
    for i in range(total):
        fns = sorted(groups[i])
        ext = ".a" if types[i] == "static" else ".so"
        filename = "lib" + "-".join(fns) + ext
        libs.append({"type": types[i], "functions": fns, "filename": filename})

    return libs


# Helper to pick an odd Y within [y_min, y_max]
def rand_odd_in_range(rng: random.Random, y_min: int, y_max: int) -> int:
    if y_min > y_max:
        raise ValueError("Некорректный диапазон Y: y_min > y_max")

    # Выберем произвольное и скорректируем
    y = rng.randint(y_min, y_max)
    return 2 * (y // 2) + 1


def make_proto(result, name, tail):
    return f"{result} {name}{tail}"


def compute_variant(fio: str, x_min=2, x_max=33, y_min=2, y_max=21) -> Dict:
    norm = normalize_fio(fio)
    if not norm:
        raise ValueError("Пустое ФИО после нормализации. Введите корректные ФИО.")

    digest = hashlib.sha256(norm.encode("utf-8")).hexdigest()
    seed64 = int(digest[:16], 16)
    rng = random.Random(seed64)

    # Разрешаем совпадения (с выбором с возвращением)
    sort1, sort2 = pick_two(rng, ALGO_SORTS)
    score1, score2 = pick_two(rng, SCORE_FUNCS)

    if rng.uniform(0, 1) > 0.5 and sort1 != sort2 and score1 != score2:
        if rng.choice([1, 2]) == 1:
            sort2 = sort1
        else:
            score2 = score1

    X = rng.randint(x_min, x_max)
    Y = rand_odd_in_range(rng, y_min, y_max)

    libs = generate_libs_on_the_fly(sort1, sort2, score1, score2, rng)

    chosen_protos = {
        "sorts": [
            make_proto(VOID, sort1, INDEX_TAIL),
            make_proto(VOID, sort2, INDEX_TAIL),
        ][: 1 + (sort1 != sort2)],
        "scores": [
            make_proto(DOUBLE, score1, DOUBLE_TAIL),
            make_proto(DOUBLE, score2, DOUBLE_TAIL),
        ][: 1 + (score1 != score2)],
        "structs": COMMON_STRUCTS,
        "common": COMMON_PROTOS,
    }

    return {
        "fio": fio,
        "normalized_key": norm,
        # ID варианта как целое число из первых 8 hex-символов
        "variant_id": int(digest[:8], 16),
        "sorts": {"first": sort1, "second": sort2},
        "scores": {"first": score1, "second": score2},
        "X": X,
        "Y": Y,
        "libraries": libs,
        "prototypes": chosen_protos,
    }


def print_pretty(v: Dict):
    print(f"ID варианта: {v["variant_id"]}\n")

    # Уникальные алгоритмы сортировки с корректной формой заголовка
    unique_sorts = list(dict.fromkeys([v["sorts"]["first"], v["sorts"]["second"]]))
    if len(unique_sorts) == 1:
        print("Алгоритм сортировки:")
        print(f"  - {unique_sorts[0]}\n")
    else:
        print("Алгоритмы сортировки:")
        for i, s in enumerate(unique_sorts, 1):
            print(f"  {i}) {s}")
        print()

    # Уникальные функции оценки с корректной формой заголовка
    unique_scores = list(dict.fromkeys([v["scores"]["first"], v["scores"]["second"]]))
    if len(unique_scores) == 1:
        print("Функция оценки:")
        print(f"  - {unique_scores[0]}\n")
    else:
        print("Функции оценки:")
        for i, s in enumerate(unique_scores, 1):
            print(f"  {i}) {s}")
        print()

    print(f"X (цены после сортировки): {v["X"]}")
    print(f"Y (товары после сортировки): {v["Y"]}\n")

    print(f"Единицы компиляции, всего: {len(v["libraries"])}")
    for i, lib in enumerate(v["libraries"], 1):
        print(f"  [{i}] {lib["type"]}: {lib["filename"]}")
        print(f"      функции: {", ".join(lib["functions"])}")
    print()

    # По требованию: не печатать зависимости модулей и порядок линковки

    # Разделяем вывод структур и сигнатур функций
    structs = v["prototypes"]["structs"]
    common_funcs = v["prototypes"]["common"]

    print("Структуры:")
    for p in structs:
        print(f"  {p}")
    print()

    print("Сигнатуры (общие):")
    for p in common_funcs:
        print(f"  {p}")
    print()

    # Вариантные сигнатуры: сортировки и оценки, без дубликатов, в исходном порядке
    variant_sigs = list(
        dict.fromkeys(v["prototypes"]["sorts"] + v["prototypes"]["scores"])
    )
    print("Сигнатуры (прочие):")
    for p in variant_sigs:
        print(f"  {p}")
    print()


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    as_json = any(a == "--json" for a in sys.argv[1:])

    if args:
        fio = " ".join(args).strip()
    else:
        fio = input("Введите ФИО: ").strip()

    try:
        variant = compute_variant(fio)
    except ValueError as e:
        print(f"Ошибка: {e}", file=sys.stderr)
        sys.exit(1)

    if as_json:
        print(json.dumps(variant, ensure_ascii=False, indent=2))
    else:
        print_pretty(variant)


if __name__ == "__main__":
    main()
