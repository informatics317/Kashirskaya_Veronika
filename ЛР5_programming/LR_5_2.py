big_list = [
    "avag78_sdh",
    "s_khbwbi",
    "kshvbkjb34",
    "32jn kndd",
    "wewjhjksd",
    "wefbwjhbkjkj",
    "ewwef",
    "dcs777scd",
    "wscd88.sdc",
    "kjshapix",
    "oppzxcc2299"
]

small_list = [
    "ewef",
    "s_khb",
    "dcs777scd",
    "wscd88,sdc",
    "kjsha pix",
    "52jn hlkuttndd",
    "oppzxcc229"
]


def normalize(text):
    text = text.replace(" ", "")
    text = text.replace("-", "")
    text = text.replace("_", "")
    text = text.replace(",", ".")
    text = text.replace(";", ".")
    text = text.replace(":", ".")
    text = text.replace("/", ".")
    text = text.lower()
    return text


def levenstein(str_1, str_2):
    n, m = len(str_1), len(str_2)
    if n > m:
        str_1, str_2 = str_2, str_1
        n, m = m, n

    current_row = range(n + 1)
    for i in range(1, m + 1):
        previous_row, current_row = current_row, [i] + [0] * n
        for j in range(1, n + 1):
            add, delete, change = previous_row[j] + 1, current_row[j - 1] + 1, previous_row[j - 1]
            if str_1[j - 1] != str_2[i - 1]:
                change += 1
            current_row[j] = min(add, delete, change)

    return current_row[n]


big_dict = {i: normalize(el) for i, el in enumerate(big_list)}
small_dict = {i: normalize(el) for i, el in enumerate(small_list)}

res1 = []
res2 = []
res3 = []
not_found = []

for id, el in small_dict.items():
    matches = []

    for b_id, b_el in big_dict.items():
        dist = levenstein(el, b_el)

        if dist == 0:
            matches.append(('exact', b_id, dist))
        elif 1 <= dist <= 3:
            matches.append(('close', b_id, dist))
        elif 4 <= dist <= 5:
            matches.append(('distant', b_id, dist))

    if matches:
        exact_matches = [m for m in matches if m[0] == 'exact']
        close_matches = [m for m in matches if m[0] == 'close']
        distant_matches = [m for m in matches if m[0] == 'distant']

        if exact_matches:
            for match in exact_matches:
                res1.append((el, match[1], match[2]))

        if close_matches:
            res2.append((el, [(m[1], m[2]) for m in close_matches]))

        if distant_matches:
            res3.append((el, [(m[1], m[2]) for m in distant_matches]))
    else:
        not_found.append((el, id))

print("ТОЧНЫЕ СОВПАДЕНИЯ (dist = 0):")
for item in res1:
    print(f"  '{item[0]}' → big_list[{item[1]}] (расстояние: {item[2]})")

print("БЛИЗКИЕ СОВПАДЕНИЯ (1 ≤ dist ≤ 3):")
for item in res2:
    print(f"  '{item[0]}' → {[(idx, dist) for idx, dist in item[1]]}")

print("ОТДАЛЕННЫЕ СОВПАДЕНИЯ (4 ≤ dist ≤ 5):")
for item in res3:
    print(f"  '{item[0]}' → {[(idx, dist) for idx, dist in item[1]]}")

print("НЕ НАЙДЕНО (dist > 5):")
for item in not_found:
    print(f"  '{item[0]}' (исходный индекс: {item[1]})")
