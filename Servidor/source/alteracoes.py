import gmpy2
from Crypto.Util import number

n_length = 2048

primeNum = number.getPrime(n_length)

n = gmpy2.next_prime(primeNum)