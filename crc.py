#!/usr/bin/env python3

import zlib

def crc32(data, init=0):
    return zlib.crc32(data, init ^ 0xffffffff) ^ 0xffffffff

POLY = 0xedb88320
UNPOLY = ((POLY&0x7fffffff)<<1)+1

def crc32_1bit(bit, init=0):
    init ^= bit
    if init & 1 == 1:
        return (init >> 1) ^ POLY
    else:
        return init >> 1

def crc32_combine_1(crc1, crc2, len2):
    return crc32(b"\x00" * len2, crc1) ^ crc2

X = 1<<32

def compute_zero_operator_matrix():
    return [crc32_1bit(0, 1<<shift) for shift in range(32)] + [X]

def compute_one_operator_matrix():
    mflip = [1<<shift for shift in range(32)] + [X+1]
    return matrix_mul(compute_zero_operator_matrix(), mflip)

def identity_matrix():
    return [1<<shift for shift in range(33)]

def compute_single_byte_operator_matrix(b):
    factors = [compute_zero_operator_matrix(), compute_one_operator_matrix()]
    m = identity_matrix()
    for shift in range(8):
        m = matrix_mul(m, factors[(b>>(7-shift))&1])
    return m

def matrix_mul_vector(m, v):
    r = 0
    for shift in range(len(m)):
        if (v>>shift) & 1 == 1:
            r ^= m[shift]
    return r

def matrix_mul(a, b):
    assert len(a) == len(b)
    return [matrix_mul_vector(a, v) for v in b]

def matrix_square(m):
    return matrix_mul(m, m)

def print_matrix(m):
    print("[", end="")
    for n, row in enumerate(m):
        if n != 0:
            print(" ", end="")
        print("{:09x}".format(row), end="")
        if n != len(m)-1:
            print()
    print("]")

m0 = compute_zero_operator_matrix()
m1 = compute_one_operator_matrix()
print_matrix(m0)
print_matrix(m1)
print("{:09x}".format(matrix_mul_vector(m0, X+0)))
print("{:09x}".format(crc32_1bit(0, 0)))
print("{:09x}".format(matrix_mul_vector(m1, X+0)))
print("{:09x}".format(crc32_1bit(1, 0)))
print("{:09x}".format(matrix_mul_vector(m0, X+POLY)))
print("{:09x}".format(crc32_1bit(0, POLY)))
print("{:09x}".format(matrix_mul_vector(m1, X+POLY)))
print("{:09x}".format(crc32_1bit(1, POLY)))
print("{:09x}".format(matrix_mul_vector(m0, X+UNPOLY)))
print("{:09x}".format(crc32_1bit(0, UNPOLY)))
print("{:09x}".format(matrix_mul_vector(m1, X+UNPOLY)))
print("{:09x}".format(crc32_1bit(1, UNPOLY)))

print()
print("{:09x}".format(matrix_mul_vector(m0, X+123)))
print("{:09x}".format(crc32_1bit(0, 123)))
print("{:09x}".format(matrix_mul_vector(matrix_square(m0), X+123)))
print("{:09x}".format(crc32_1bit(0, crc32_1bit(0, 123))))
print("{:09x}".format(matrix_mul_vector(matrix_square(matrix_square(m0)), X+123)))
print("{:09x}".format(crc32_1bit(0, crc32_1bit(0, crc32_1bit(0, crc32_1bit(0, 123))))))

print()
print("{:09x}".format(matrix_mul_vector(m1, X+200)))
print("{:09x}".format(crc32_1bit(1, 200)))
print("{:09x}".format(matrix_mul_vector(matrix_square(m1), X+200)))
print("{:09x}".format(crc32_1bit(1, crc32_1bit(1, X+200))))
print("{:09x}".format(matrix_mul_vector(matrix_square(matrix_square(m1)), X+200)))
print("{:09x}".format(crc32_1bit(1, crc32_1bit(1, crc32_1bit(1, crc32_1bit(1, 200))))))

print()
print("{:09x}".format(matrix_mul_vector(m1, X+2)))
print("{:09x}".format(crc32_1bit(1, 2)))
print("{:09x}".format(matrix_mul_vector(matrix_square(m1), X+2)))
print("{:09x}".format(crc32_1bit(1, crc32_1bit(1, X+2))))
print("{:09x}".format(matrix_mul_vector(matrix_square(matrix_square(m1)), X+2)))
print("{:09x}".format(crc32_1bit(1, crc32_1bit(1, crc32_1bit(1, crc32_1bit(1, X+2))))))

print()
print("{:09x}".format(matrix_mul_vector(m0, X+1)))
print("{:09x}".format(crc32(b"\x80", 0)))
print("{:09x}".format(matrix_mul_vector(matrix_square(m0), X+1)))
print("{:09x}".format(crc32(b"\x40", 0)))
print("{:09x}".format(matrix_mul_vector(matrix_square(matrix_square(m0)), X+1)))
print("{:09x}".format(crc32(b"\x10", 0)))
print("{:09x}".format(matrix_mul_vector(matrix_square(matrix_square(matrix_square(m0))), X+1)))
print("{:09x}".format(crc32(b"\x01", 0)))
print("{:09x}".format(matrix_mul_vector(matrix_square(matrix_square(matrix_square(matrix_square(m0)))), X+1)))
print("{:09x}".format(crc32(b"\x01\x00", 0)))
print("{:09x}".format(matrix_mul_vector(matrix_square(matrix_square(matrix_square(matrix_square(matrix_square(m0))))), X+1)))
print("{:09x}".format(crc32(b"\x01\x00\x00\x00", 0)))

print()
print("{:09x}".format(matrix_mul_vector(m1, X)))
print("{:09x}".format(crc32(b"\x80", 0)))
print("{:09x}".format(matrix_mul_vector(matrix_square(m1), X)))
print("{:09x}".format(crc32(b"\xc0", 0)))
print("{:09x}".format(matrix_mul_vector(matrix_square(matrix_square(m1)), X)))
print("{:09x}".format(crc32(b"\xf0", 0)))
print("{:09x}".format(matrix_mul_vector(matrix_mul(m1, matrix_square(matrix_square(m1))), X)))
print("{:09x}".format(crc32(b"\xf8", 0)))
print("{:09x}".format(matrix_mul_vector(matrix_mul(m1, matrix_mul(m1, matrix_square(matrix_square(m1)))), X)))
print("{:09x}".format(crc32(b"\xfc", 0)))
print("{:09x}".format(matrix_mul_vector(matrix_mul(m1, matrix_mul(m1, matrix_mul(m1, matrix_square(matrix_square(m1))))), X)))
print("{:09x}".format(crc32(b"\xfe", 0)))
print("{:09x}".format(matrix_mul_vector(matrix_mul(m1, matrix_mul(m1, matrix_mul(m1, matrix_mul(m1, matrix_square(matrix_square(m1)))))), X)))
print("{:09x}".format(crc32(b"\xff", 0)))
print("{:09x}".format(matrix_mul_vector(matrix_square(matrix_square(matrix_square(m1))), X)))
print("{:09x}".format(crc32(b"\xff", 0)))
print("{:09x}".format(matrix_mul_vector(matrix_square(matrix_square(matrix_square(matrix_square(m1)))), X)))
print("{:09x}".format(crc32(b"\xff\xff", 0)))
print("{:09x}".format(matrix_mul_vector(matrix_square(matrix_square(matrix_square(matrix_square(matrix_square(m1))))), X)))
print("{:09x}".format(crc32(b"\xff\xff\xff\xff", 0)))

print()
MA = compute_single_byte_operator_matrix(ord(b"A"))
print_matrix(MA)
print("{:09x}".format(matrix_mul_vector(MA, X+0)))
print("{:09x}".format(crc32(b"A", 0)))
