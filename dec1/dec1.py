sequence = [x.strip() for x in open('puzzle_input', 'r').read().strip().split('\n') if x]

mod = 100
dial = 50
pw = 0
new_dial = dial
for cmd in sequence:
    dir = cmd[0]
    num = int(cmd[1:])
    if dir == 'L':
        clicks_to_next_zero = dial or mod
        dial = (dial - num) % mod
    else:
        clicks_to_next_zero = mod - dial
        dial = (dial + num) % mod

    if num >= clicks_to_next_zero:
        pw += (num - clicks_to_next_zero) // mod + 1

print("password:", pw)
