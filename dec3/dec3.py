banks = [x for x in open("puzzle_input", "r").read().strip().split("\n")]

def part1():
    count = 0
    for bank in banks:
        left = 0
        right = len(bank) - 1
        left_start = left
        right_start = right

        left_n = int(bank[left])
        right_n = int(bank[right])

        for i, n in enumerate(map(int, iter(bank[left_start + 1 : right_start]))):
            if left_n == 9:
                break
            if n > left_n:
                left = i + left_start + 1
                left_n = n

        left_start = left
        for i, n in enumerate(map(int, iter(reversed(bank[left_start + 1 : right_start])))):
            if right_n == 9:
                break
            if n > right_n:
                right = right_start - i - 1
                right_n = n

        count += (left_n * 10 + right_n)

    print(count)

def part2():
    count  = 0
    for bank in banks:

        bank_start_idx = 0

        batteries = []

        batteries_needed = 12
        batteries_to_consider = len(bank) - batteries_needed + 1

        while batteries_needed > 0:
            best_joltage = int(bank[bank_start_idx])
            batteries_to_consider = len(bank) - bank_start_idx - batteries_needed + 1
            for i in range(bank_start_idx, bank_start_idx + batteries_to_consider):
                joltage = int(bank[i])
                if joltage > best_joltage:
                    bank_start_idx = i
                    best_joltage = joltage
            batteries.append(best_joltage)
            batteries_needed -= 1
            bank_start_idx += 1
        
        total_joltage = 0
        for b in batteries:
            total_joltage = total_joltage * 10 + b
        count += total_joltage
    print(count)

part2()
