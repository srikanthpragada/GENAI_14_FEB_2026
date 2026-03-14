def isprime(num: int) -> bool:
    """Returns True if num is a prime number, False otherwise."""
    if num <= 1:
        return False
    for i in range(2, int(num**0.5) + 1):
        if num % i == 0:
            return False
    return True


def isperfect(num: int) -> bool:
    """Returns True if num is a perfect number, False otherwise."""
    if num < 1:
        return False
    sum_of_divisors = 0
    for i in range(1, num // 2 + 1):
        if num % i == 0:
            sum_of_divisors += i

    return sum_of_divisors == num
