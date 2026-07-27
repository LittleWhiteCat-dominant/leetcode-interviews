def remove_occurrences(s: str, part: str) -> str:
    result = []
    part_len = len(part)

    last_char = part[len(part) - 1]

    for char in s:
        result.append(char)

        if len(result) >= part_len and char == last_char:
            if "".join(result[-part_len: ]) == part:
                del result[-part_len:]

    return "".join(result)