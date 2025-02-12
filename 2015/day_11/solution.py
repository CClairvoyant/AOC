import re

from utils_anviks import stopwatch


def is_valid(password: str):
    if 'i' in password or 'o' in password or 'l' in password:
        return False

    for i in range(2, len(password)):
        middle = ord(password[i - 1])
        if ord(password[i - 2]) == middle - 1 and ord(password[i]) == middle + 1:
            break
    else:
        return False

    return bool(re.search(r'(\w)\1.*(\w)\2', password))


def increment_string(s):
    s_list = list(s)
    i = len(s_list) - 1

    while i >= 0:
        if s_list[i] == 'z':
            s_list[i] = 'a'
            i -= 1
        else:
            s_list[i] = chr(ord(s_list[i]) + 1)
            break

    return ''.join(s_list)


@stopwatch
def solve(password: str):
    while not is_valid(password):
        password = increment_string(password)
    return password


if __name__ == '__main__':
    pass_0 = 'hepxcrrq'
    pass_1 = solve(pass_0)
    pass_2 = solve(increment_string(pass_1))
    print(pass_1)  # hepxxyzz   | 0.36 seconds
    print(pass_2)  # heqaabcc   | 0.93 seconds

