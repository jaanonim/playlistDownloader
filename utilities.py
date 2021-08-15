MAX_THREDS = 10


def split_list(alist, wanted_parts=1):
    length = len(alist)
    return [
        alist[i * length // wanted_parts : (i + 1) * length // wanted_parts]
        for i in range(wanted_parts)
    ]


def calculate_amount_of_threads(list_len):
    a = (int)(list_len / 10)
    if a > MAX_THREDS:
        return MAX_THREDS
    if a < 1:
        return 1
    return a
