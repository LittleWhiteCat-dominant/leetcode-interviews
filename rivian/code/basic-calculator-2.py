def calculate(s: str) -> int:
    stack = []
    current_number = 0
    operator = "+"

    for i, item in enumerate(s):

        if item.isdigit():
            current_number = current_number * 10 + int(item)
        
        if item in "+-*/" or i == len(s) - 1:
            if operator == "+":
                stack.append(current_number)
            elif operator == "-":
                stack.append(-current_number)
            elif operator == "*":
                stack.append(stack.pop()*current_number)
            elif operator == "/":
                last_item = stack.pop()
                stack.append(int(last_item/current_number))
        
            operator = item
            current_number = 0
        
    return sum(stack)

