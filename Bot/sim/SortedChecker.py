def get_digit(number, n):
    return number // (10**n) % 10

def check_sorted(number):
    past_digit = -1
    for i in reversed(range(len(str(number)))):
        cur_digit = get_digit(number, i)
        if past_digit > cur_digit:
            return False
        past_digit = cur_digit
    return True

sorted_count = 0
for ten_k in range(6):
    for k in range(6):
        for hund in range(6):
            for ten in range(6):
                for one in range(6):
                    num = ten_k * 10000 \
                          + k * 1000 \
                          + hund * 100 \
                          + ten * 10 \
                          + one * 1
                    if check_sorted(num):
                        sorted_count += 1

print(sorted_count)
