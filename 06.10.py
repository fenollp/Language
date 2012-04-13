#/usr/bin/env python3
# -*- coding: utf-8 -*-

# 2011.06.10th try

def gen_from_regex( regex ):
	lim = 5
	for i in range(0, len(regex)+1):
		c = regex[i]
		if c is '?':
			