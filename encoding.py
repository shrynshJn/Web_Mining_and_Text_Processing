import math
def unary_encoding(num):
    return "0"*(num-1) + "1"

def dec2bin(num):
    binary = ""
    if (num == 0):
         return "0"
    while(num!=0):
        binary += str(num%2)
        num =  int(num/2)
    return binary[::-1]

def bin2dec(binary):
    num = 0
    binary = binary[::-1]
    for i in range(len(binary)):
        num += (int(binary[i]) << i)
    return num

def remainder_encoding(r, b):
    i = math.floor(math.log(b, 2))
    d = 2**(i+1) - b
    if (r >= d):
        binary = dec2bin(r + d)
        if (len(binary) < i + 1):
            binary = "0"*(i + 1 - len(binary)) + binary
        return binary
    else: 
        binary = dec2bin(r)
        if (len(binary) < i):
            binary = "0"*(i  - len(binary))  + binary
        return binary

def elias_gamma_encoding(num):
    binary = dec2bin(num)
    pretext = "0"*(len(binary) - 1)
    return pretext+binary

def elias_gamma_decoding(gamma):
    k = gamma.find("1")
    binary = gamma[k:2*k + 1]
    return bin2dec(binary)

def elias_detla_encoding(num):
    if(num == 0):
        return -1
    gamma = elias_gamma_encoding(1 + math.floor(math.log(num, 2)))
    binary = dec2bin(num)
    return gamma + binary[1:]

def elias_delta_decoding(delta):
    if(delta == -1):
        return 0
    l = delta.find("1")
    m_binary = delta[l: 2*l + 1]
    m = bin2dec(m_binary)
    num_binary = "1" + delta[2*l + 1: 2*l + 1 + m]
    return (bin2dec(num_binary))
    
def golomb_encoding(num, b):
    q = int(num/b)
    part1 = unary_encoding(q + 1)
    r = num - q*b
    part2 = remainder_encoding(r, b)
    return part1 + part2
    
def golomb_decoding(golomb, b):
    q = golomb.find("1")
    i = math.floor(math.log(b,2))
    d = 2**(i+1) - b
    rem = golomb[q + 1:]
    if (len(rem) == i):
        r = bin2dec(golomb[q + 1:])
    else:
        r = bin2dec(golomb[q + 1:]) - d
    return q*b + r
for i in range(1, 11):
    print(golomb_decoding(golomb_encoding(i, 3),3), golomb_decoding(golomb_encoding(i, 10),10))
    