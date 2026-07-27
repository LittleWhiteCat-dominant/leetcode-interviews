def compress(chars: list[str]) -> int:
    if not chars:
        return 0

    read, write = 0, 0
    n = len(chars)

    while read < n:
        char = chars[read]
        group_start = read

        while read < n and chars[read] == char:
            read += 1
        
        group_count = read - group_start
        chars[write] = char
        write += 1

        if group_count > 1:
            for digit in str(group_count):
                chars[write] = digit
                write += 1
        
    return write

