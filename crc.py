#!/usr/bin/env python3

import zlib

POLY = 0xedb88320

def crc32_1bit(bit, init=0):
    init ^= bit
    # init = init & 0xffffffff
    if init & 1 == 1:
        return (init >> 1) ^ POLY
    else:
        return init >> 1

def crc32(data, init=0):
    return zlib.crc32(data, init ^ 0xffffffff) ^ 0xffffffff

def crc32_combine_1(crc1, crc2, len2):
    return crc32(b"\x00" * len2, crc1) ^ crc2

def identity_matrix():
    return [1<<shift for shift in range(33)]

X = 1<<32

def compute_zero_operator_matrix():
    return [crc32_1bit(0, 1<<shift) for shift in range(33)]

def compute_one_operator_matrix():
    return [crc32_1bit(1, 1<<shift) for shift in range(33)]

def compute_single_byte_operator_matrix(b):
    factors = [compute_zero_operator_matrix(), compute_one_operator_matrix()]
    m = identity_matrix()
    for shift in range(8):
        m = matrix_mul(m, factors[(b>>shift)&1])
    return m

def matrix_mul_vector(m, v):
    r = 0
    for shift in range(len(m)):
        if (v>>shift) & 1:
            r ^= m[shift]
    return r

def matrix_mul(a, b):
    return [matrix_mul_vector(a, v) for v in b]

def matrix_square(m):
    return matrix_mul(m, m)

print("{:08x}".format(int("".join(reversed("10100010001001110010000010101010")), 2)))
print("{:08x}".format(crc32_1bit(0, 1)))
print("{:08x}".format(crc32_1bit(1, 1)))
print("{:08x}".format(crc32(b"\x00\x00\x00\x01")))
print("{:08x}".format(crc32(b"\x01")))
print("{:08x}".format(int("".join(reversed("011010010000110011100000111011100")), 2)))
print("{:08x}".format(crc32(b"\x01\x00")))
print("{:08x}".format(int("".join(reversed("100000101000110011011000100110000")), 2)))
print("{:08x}".format(crc32(b"\x01\x00\x00\x00")))
print("{:08x}".format(int("".join(reversed("110100010001001110010000010101010")), 2)))

print()

print("{:08x}".format(crc32(b"\x00" * 100)))
print("{:08x}".format(crc32(b"\x01" + b"\x00" * 100)))
print("{:08x}".format(crc32_combine_1(crc32(b"\x01"), crc32(b"\x00" * 100), 100)))

print()

def print_matrix(m):
    print("[", end="")
    for n, row in enumerate(m):
        if n != 0:
            print(" ", end="")
        print("{:08x}".format(row), end="")
        if n != len(m)-1:
            print()
    print("]")

print()
m0 = compute_zero_operator_matrix()
print_matrix(m0)
print("{:08x}".format(matrix_mul_vector(m0, 123)))
print("{:08x}".format(crc32_1bit(0, 123)))

print()
m1 = compute_one_operator_matrix()
print_matrix(m1)
print("{:08x}".format(matrix_mul_vector(m1, 0)))
print("{:08x}".format(matrix_mul_vector(m1, X+0)))
print("{:08x}".format(crc32_1bit(1, 0)))
print("{:08x}".format(matrix_mul_vector(matrix_square(m1), X+0)))
print("{:08x}".format(crc32_1bit(1, crc32_1bit(1, 0))))
print("{:08x}".format(matrix_mul_vector(matrix_square(matrix_square(m1)), X+0)))
print("{:08x}".format(crc32_1bit(1, crc32_1bit(1, crc32_1bit(1, crc32_1bit(1, 0))))))

print()
print("{:08x}".format(matrix_mul_vector(matrix_square(matrix_square(matrix_square(m0))), X+1)))
print("{:08x}".format(crc32(b"\x00", 1)))
print()
print("{:08x}".format(matrix_mul_vector(matrix_square(matrix_square(matrix_square(m1))), X)))
print("{:08x}".format(crc32(b"\xff", 0)))

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
