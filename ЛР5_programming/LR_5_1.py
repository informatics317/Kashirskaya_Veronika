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
    text = text.replace(" ", "").replace("-", "").replace(",", ".").lower()
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

for id, el in small_dict.items():
    res2_b_id = []

    for b_id, b_el in big_dict.items():
        dist = levenstein(el, b_el)

        if dist == 0:
            res1.append((el, b_id))
            break

        elif 1 <= dist <= 3:
            if b_id not in res2_b_id:
                res2_b_id.append(b_id)

        elif 3 < dist <= 5:
            if b_id not in res2_b_id:
                res2_b_id.append(b_id)

    if res2_b_id != []:
        res2.append((el, res2_b_id))

print(res1)
print(res2)
