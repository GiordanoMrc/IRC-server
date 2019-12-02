import random
from Crypto.Util import number

#calcula phi de euler
def phi(p,q):
    phi = (p - 1) * (q - 1)
    return phi

#Calcula GCD
def computeGCD(x, y):

   while(y):
       x, y = y, x % y

   return x

#Calcula o inverso
def multiplicative_inverse(a, b):
    x = 0
    y = 1
    lx = 1
    ly = 0
    oa = a  # Remember original a/b to remove
    ob = b  # negative values from return results
    while b != 0:
        q = a // b
        (a, b) = (b, a % b)
        (x, lx) = ((lx - (q * x)), x)
        (y, ly) = ((ly - (q * y)), y)
    if lx < 0:
        lx += ob  # If neg wrap modulo orignal b
    if ly < 0:
        ly += oa  # If neg wrap modulo orignal a
    # return a , lx, ly  # Return only positive values
    return lx

    if ly < 0:
        ly += oa  # If neg wrap modulo orignal a
    # return a , lx, ly  # Return only positive values
    return lx

#gera o conjunto de chaves privada e publixa
def gera_chaves():

    n_length = 256
    primeNum1 = number.getPrime(n_length)
    primeNum2 = number.getPrime(n_length)
    n = primeNum1 * primeNum2

    phii = phi(primeNum1, primeNum2)

    e = random.randrange(1, phii)
    g = computeGCD(e, phii)
    while g != 1:
        e = random.randrange(1, phii)
        g = computeGCD(e, phii)

    d = multiplicative_inverse(e,phii)

    public_key = (e, n)
    private_key = (d, n)

    return[public_key,private_key]


##Converte de String para decimal
def converte_to_decimal(s):
    nchars = len(s)
    return sum(ord(s[byte])<<8*(nchars-byte-1) for byte in range(nchars))

# Converte decimal para String
def converte_string(x):
    nchars  = 1
    n_antigo = 1
    while 1:
        variable = ''.join(chr((x>>8*(nchars-byte-1))&0xFF) for byte in range(nchars))
        if (variable[0:1] == '\x00'):
            break
        else:
            nchars = nchars + 1
    return variable[1:]

#criptografa ou decriptografa X
def crito_decripto(x,chave,n):
    return pow(x,chave, n)
