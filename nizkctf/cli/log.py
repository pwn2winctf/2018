# -*- encoding: utf-8 -*-

def info(s):
    print('\033[93m[*]\033[00m %s'%(s))

def success(s):
    print('\033[92m[+]\033[00m %s'%(s))

def fail(s):
    print('\033[91m[!]\033[00m %s'%(s))
