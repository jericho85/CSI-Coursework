# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""


x = 123.456789

# To print X as a 16 digit number with 8 decimal places:
print('{0:16.8f}'.format(x),"\n")

y = 17
print('{0:4.2f} {1:04d}'.format(x,7),"\n")

z = 'spam'

print('{}'.format(z),"\n")

print('I like {0}, {1} and {other}.\n'.\
      format('spam','eggs',other='bacon'))

print(z.rjust(20))

#%%

'''
print('spec'.format(list of items))
spec: 
    quoted string
    may contain free text
    contains background formatted code:
        {n:dT}
        n = item number or name in list
        d = size code
        T = the type code
'''

print('{0:4d} {1:8d}'.format(10,20))

#%%

print('{0:4.2f} {1:8.4f}'.format(10.12345,20.98765))

#%%

print('{last:16s} {first:8s}'.format(first='monty',last='python'))

#%%

import sys

def printf(format,*args):
    sys.stdout.write(format % args)

printf('%4d %8d', 10,20)
print()

printf('%4.2f %8.4f \n', 10.12345, 20.98765)

printf('%8s %16s', 'monty','python')











