ranges = [list(map(int, x.split('-'))) for x in open("puzzle_input", "r").read().strip().split(',')]

def part1():


    """
    idea:
    6: abcabc = abc + abc * 1000 = abc * (1 + 1000)
    4: abab   = ab + ab * 100    = ab * (1 + 100)
    2: aa     = a + a * 10       = a * (1 + 10)
    """
    count = 0
    for lower, upper in ranges:
        for n in range(lower, upper + 1):
            digits = len(str(n))
            if digits % 2 != 0:
                continue
            exp = digits // 2
            mod = 10**exp+1
            if (n % mod) == 0 and n // mod < 10**exp:
                count += n
    print(count)

def part2():
    """
    idea:
    three repeating chars:
        6: abcabc = abc + abc * 1000 = abc * (1 + 1000)
        9: abcabcabc = abc + abc * 1000 + abc * 1_000_000 = abc * (1 + 10**3 + 10**6)
                                                          = abc * sum_{i=0}^{2}(1000**i)
        12: ...
        ...
    two repeating chars:
        4: abab   = ab + ab * 100    = ab * (1 + 100)
        6: ababab = ab + ab * 100 + ab * 10000 = ab * (1 + 10**2 + 10**4)
                                               = ab * (100**0 + 100**1 + 100**2)
                                               = ab * sum_{i=0}^{2}(100**i)
        8: ...
    one repeating char:
        2: aa     = a + a * 10       = a * (1 + 10)
        3: aaa    = a * sum_{i=0}^{2}(10**i)
        ...
    k repeating chars: 
        2 * k: abc...abc... = abc... * ((10**k)**0 + (10**k)**1)
        3 * k: abc...abc...abc... = abc... * ((10**k)**0 + (10**k)**1 + (10**k)**2)

    => for r repetitons for k chars the number must satisfy:
        r * k: abc...abc...abc...... = abc... * sum_{i=0}^{r-1}((10**k)**i)

    Let N be a number with d digits 
        N = a_0a_1a_2...a_d
    The length of a repeating sequence k must be a divisor of d. 
    In other words: k must be in the prime factorisation of d. 
    For example, if a number has 7 digits, then the lengths of repeating sequences that 
    have to be considered are 1 and 7. But 7 can be discarded because then the sequence wouldn't repeat.
    In conclusion: 
        - k must be in the prime factorisation of d.
        - k must be smaller than or equal to d/2, because the sequence has to repeat at least 2 times.
    """


    import time
    time_start = time.time()

    count = 0
    for lower, upper in ranges:
        for id in range(lower, upper + 1):
            d = len(str(id))

            for k in range(1, d//2 + 1):
                if d % k != 0:
                    continue
                r = d // k

                q = sum((10**(k*i) for i in range(0, r)))
                if id % q == 0:
                    count += id
                    break # avoid double counting

    print(count)
    time_end = time.time()
    print(f"elapsed: {time_end - time_start:.3f}s")

def part2_fast():
    import time
    time_start = time.time()

    primes: dict[int, list[int]] = {}
    for i in range(1, 1000):
        primes[i] = []
        for j in range(1, i // 2 + 1):
            if i % j == 0:
                primes[i].append(j)

    count = 0
    for lower, upper in ranges:
        for id in range(lower, upper + 1):
            d = len(str(id))
            for k in primes[d]:
                r = d // k
                q = (1 - 10**(k*r)) // (1-10**k)
                if id % q == 0:
                    count += id
                    break # avoid double counting

    print(count)
    time_end = time.time()
    print(f"elapsed: {time_end - time_start:.3f}s")

def part2_fast_af():
    import time
    time_start = time.time()

    primes: dict[int, list[int]] = {}
    for i in range(1, 1000):
        primes[i] = []
        for j in range(1, i // 2 + 1):
            if i % j == 0:
                primes[i].append(j)
    count = 0
    invalid_ids = set()
    for lower, upper in ranges:
        d_low = len(str(lower))
        d_up = len(str(upper))

        for d in range(d_low, d_up + 1):
            for k in primes[d]:
                # print(d, k)
                r = d // k
                q = (1 - 10**(k*r)) // (1-10**k)
                """
                d = 8
                k = 2
                r = 4
                q = 101

                10 11 12 13 ...
                20 ...
                30 ...
                ...
                90 ... 99
                => 9 * 10 combinations
                id = combination * q

                k = 1 => range(1, 10)
                k = 2 => range(10, 100)
                k = 3 => range(100, 1000)
                ...
                => c in range(10**(k-1), 10**k)
                <=> c = sum_{i=10**(k-1)}^{10**k}(i)
                => count = q * sum_{i=10**(k-1)}^{10**k}(i)

                how to handle edge case?
                    lower bound may not be the lowest possible number for d digits, so we have to adjust our range for c.

                    if the lower bound is for example 10102391, then c = 10 can be skipped, 
                    but if it is 10100000, then we can't skip c = 10.

                    how do we find the smallest c? through a binary search.
                    but lets not do that right now, just test if lower <= c * q <= upper, and skip the rest. 

                further optimizations possible:

                    lower <= c * q
                    <=> lower / q <= c
                    upper >= c * q
                    <=> upper / q >= c
                    => lower / q <= c <= upper / q

                    # [lower; 10**(d_low) - 1]            => c in range(lower / q, (10**(d_low) - 1) / q)
                    # [10**(d_low); 10**(d_low+1) - 1]    => c in ...
                    # ...
                    # [10**(d_up-1), upper]

                    # for c in range(..., ...):
                    #     invalid_ids.add(c * q)

                    then something to filter out the duplicates beforehand...
                    then gauss: sum_{1}^{n}(i) = n*(n-1)/2
                    -> instant calc

                """

                for c in range(max(10**(k-1), lower // q), min(10**k, upper // q + 1)):
                # for c in range(10**(k - 1), 10**k):
                    cq = c * q
                    if lower <= cq and cq <= upper:
                        invalid_ids.add(cq)

    for id in invalid_ids:
        count += id 
    print(count)

    time_end = time.time()
    print(f"elapsed: {time_end - time_start:.3f}s")

    return invalid_ids

# part2()
# part2_fast()
part2_fast_af()
