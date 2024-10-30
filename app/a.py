# create a function that resolve the following problem:
# Give a string of parenthesis (e.g. "(()(())))", find the amount of substitutions or movements to make the string balanced.

def balance_parenthesis(s: str) -> int:
    """
    Given a string of parenthesis, find the amount of substitutions or movements to make the string balanced.

    Args:
        s: string of parenthesis

    Returns:
        int: amount of substitutions or movements to make the string balanced.
    """
    # if the string is empty, return 0
    if not s:
        return 0

    # if the string has an odd length, return -1
    if len(s) % 2 != 0:
        return -1

    # if the string has an even length, check if it is balanced
    stack = []

    for c in s:
        if c == '(':
            stack.append(c)
        else:
            if stack and stack[-1] == '(':
                stack.pop()
            else:
                stack.append(c)

    # if the stack is empty, return 0
    if not stack:
        return 0

    # if the stack is not empty, return the length of the stack divided by 2
    return len(stack) // 2