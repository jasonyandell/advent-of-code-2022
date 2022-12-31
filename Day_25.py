from aoc import read_lines

def add_snafu(a:str,b:str):
    digits = {'1':1,'2':2,'0':0,'-':-1,'=':-2}
    a_digits = [digits[x] for x in a[::-1]]
    b_digits = [digits[x] for x in b[::-1]]
    val_digits = []
    carry = 0
    i = 0
    while carry or i < max(len(a),len(b)):
        a_val = a_digits[i] if i<len(a_digits) else 0
        b_val = b_digits[i] if i<len(b_digits) else 0
        val = a_val + b_val + carry
        carry = 0
        if val > 2:
            carry = 1
            val = val - 5
        elif val < -2:
            carry = -1
            val = val + 5
        val_digits.append(val)
        i += 1

    snafu = {v:k for k,v in digits.items()}
    result = "".join([snafu[n] for n in val_digits][::-1])
    return result

data = read_lines("data/day25.txt")

result = ""
for s in data:
    result = add_snafu(result, s)

print(result)