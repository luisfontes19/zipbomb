#!/usr/bin/env python3

import sys
import zlib

POLY = 0xedb88320
POLYLONG = (POLY<<1)|1
print(hex(POLYLONG))

def crc32_1bit(bit, init=0):
    init &= 0xffffffff
    init ^= bit
    if init & 1 == 1:
        return (init >> 1) ^ POLY
    else:
        return init >> 1

def crc32(data, init=0):
    return zlib.crc32(data, init ^ 0xffffffff) ^ 0xffffffff

def crc32_combine_1(crc1, crc2, len2):
    return crc32(b"\x00" * len2, crc1) ^ crc2

X = 1<<32

def compute_zero_operator_matrix():
    m = [crc32_1bit(0, (1<<shift)&0xffffffff) for shift in range(33)]
    m[32] |= X
    return m

def compute_one_operator_matrix():
    m = [crc32_1bit(1, (1<<shift)&0xffffffff) for shift in range(33)]
    m[32] |= X
    return m

def identity_matrix():
    return [1<<shift for shift in range(33)]

def compute_single_byte_operator_matrix(b):
    factors = [compute_zero_operator_matrix(), compute_one_operator_matrix()]
    m = identity_matrix()
    for shift in range(8):
        m = matrix_mul(m, factors[(b>>shift)&1])
    return m

def matrix_mul_vector(m, v):
    v |= X
#    v &= 0xffffffff
#    if v == 0:
#        v = X
    r = 0
    for shift in range(len(m)):
        if (v>>shift) & 1 == 1:
            r ^= m[shift]
    return r

def matrix_mul(a, b):
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

print()
m0 = compute_zero_operator_matrix()
print_matrix(m0)
print("{:09x}".format(matrix_mul_vector(m0, 123)))
print("{:09x}".format(crc32_1bit(0, 123)))
print("{:09x}".format(matrix_mul_vector(matrix_square(m0), 123)))
print("{:09x}".format(crc32_1bit(0, crc32_1bit(0, 123))))
print("{:09x}".format(matrix_mul_vector(matrix_square(matrix_square(m0)), 123)))
print("{:09x}".format(crc32_1bit(0, crc32_1bit(0, crc32_1bit(0, crc32_1bit(0, 123))))))

print()
m1 = compute_one_operator_matrix()
print_matrix(m1)
print("{:09x}".format(matrix_mul_vector(m1, X)))
print("{:09x}".format(crc32_1bit(1, 0)))
print("{:09x}".format(matrix_mul_vector(matrix_square(m1), X)))
print("{:09x}".format(crc32_1bit(1, crc32_1bit(1, 0))))
print("{:09x}".format(matrix_mul_vector(matrix_square(matrix_square(m1)), X)))
print("{:09x}".format(crc32_1bit(1, crc32_1bit(1, crc32_1bit(1, crc32_1bit(1, 0))))))

print()
print("{:09x}".format(matrix_mul_vector(matrix_square(matrix_square(matrix_square(m0))), X//2)))
print("{:09x}".format(crc32(b"\x00", X//2)))

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
# print("{:09x}".format(matrix_mul_vector(matrix_mul(m1, matrix_square(matrix_square(m1))), X)))
# print("{:09x}".format(crc32(b"\xf8", 0)))
# print("{:09x}".format(matrix_mul_vector(matrix_mul(m1, matrix_mul(m1, matrix_square(matrix_square(m1)))), X)))
# print("{:09x}".format(crc32(b"\xfc", 0)))
# print("{:09x}".format(matrix_mul_vector(matrix_mul(m1, matrix_mul(m1, matrix_mul(m1, matrix_square(matrix_square(m1))))), X)))
# print("{:09x}".format(crc32(b"\xfe", 0)))
# print("{:09x}".format(matrix_mul_vector(matrix_mul(m1, matrix_mul(m1, matrix_mul(m1, matrix_mul(m1, matrix_square(matrix_square(m1)))))), X)))
# print("{:09x}".format(crc32(b"\xff", 0)))
print("{:09x}".format(matrix_mul_vector(matrix_square(matrix_square(matrix_square(m1))), X)))
print("{:09x}".format(crc32(b"\xff", 0)))
print("{:09x}".format(matrix_mul_vector(matrix_square(matrix_square(matrix_square(matrix_square(m1)))), X)))
print("{:09x}".format(crc32(b"\xff\xff", 0)))
print("{:09x}".format(matrix_mul_vector(matrix_square(matrix_square(matrix_square(matrix_square(matrix_square(m1))))), X)))
print("{:09x}".format(crc32(b"\xff\xff\xff\xff", 0)))

print()
print_matrix(matrix_mul(m1, matrix_mul(m1, matrix_mul(m1, matrix_square(matrix_square(m1))))))
print_matrix(matrix_mul(m1, matrix_mul(m1, matrix_mul(m1, matrix_mul(m1, matrix_square(matrix_square(m1)))))))

# print()
# M0 = matrix_square(matrix_square(matrix_square(m0)))
# print_matrix(M0)
# print("{:08x}".format(matrix_mul_vector(M0, 1)))
# print("{:08x}".format(crc32(b"\x00", 1)))
# 
# MA = compute_single_byte_operator_matrix(ord(b"A"))
# print_matrix(MA)
# print("{:08x}".format(matrix_mul_vector(MA, 1)))
# print("{:08x}".format(crc32(b"A", 1)))
