#!/usr/bin/env python
# coding:utf-8

__baseTable = ['q', 'j', 'h', 'w', 'g', '8',
               't', 'i', 'p', 'n', 'k', 'c',
               'd', 'f', 'b', 'x', '6', 'r',
               '9', 'v', '3', '4', 'u', 'a',
               '2', 'e', '7', 'y', 'm', 's',
               'z', '5']


def encode(value):
	num = int(value)
	mid = []
	base = len(__baseTable)
	while True:
		if num == 0: break
		num, rem = divmod(num, base)
		mid.append(__baseTable[rem])

	return ''.join([str(x) for x in mid[::-1]])


def decode(value):
	array = list(str(value).lower())
	array.reverse()
	result = 0L
	base = len(__baseTable)
	for i, x in enumerate(array):
		result += __baseTable.index(x) * (base ** i)

	return result


if __name__ == '__main__':
	from random import randrange

	for test in range(1, 10):
		v = randrange(100000000000, 999999999999)
		enc = encode(v)
		print "Number:%i, Encode: %s, Decode: %i" % (v, enc, decode(enc))

	for test in range(1, 10):
		v = randrange(1, 9999)
		enc = encode(v)
		print "Number:%i, Encode: %s, Decode: %i" % (v, enc, decode(enc))
