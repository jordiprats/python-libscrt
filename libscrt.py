from Crypto.Cipher import Blowfish
import argparse
import codecs
import six
import sys
import re

def decrypt(password):
    c1_code = '5F B0 45 A2 94 17 D9 16 C6 C6 A2 FF 06 41 82 B7'.replace(' ','')
    c2_code = '24 A6 3D DE 5B D3 B3 82 9C 7E 06 F4 08 16 AA 07'.replace(' ','')

    c1 = Blowfish.new(codecs.decode(c1_code, 'hex'), Blowfish.MODE_CBC, '\x00'*8)
    c2 = Blowfish.new(codecs.decode(c2_code, 'hex'), Blowfish.MODE_CBC, '\x00'*8)
    padded = c1.decrypt(c2.decrypt(codecs.decode(password, 'hex'))[4:-4])
    
    p = bytes()
    while padded[:2] != b'\x00\x00' :
        p += padded[:2]
        padded = padded[2:]
    return codecs.decode(p, 'UTF-16')

def hostname(f):
    x = open(f).read().replace('\x00', '')
    REGEX_HOSTNAME = re.compile(six.u(r'S:"Hostname"=([^\r\n]*)'))
    m = REGEX_HOSTNAME.search(x)
    if m:
        return m.group(1)
    return ''

def password(f):
    x = open(f).read().replace('\x00', '')
    REGEX_PASWORD = re.compile(six.u(r'S:"Password"=u([0-9a-f]+)'))
    m = REGEX_PASWORD.search(x)
    if m:
        return decrypt(m.group(1))
    return ''

def port(f):
    x = open(f).read().replace('\x00', '')
    REGEX_PORT = re.compile(six.u(r'D:"\[SSH2\] Port"=([0-9a-f]{8})'))
    m = REGEX_PORT.search(x)
    if m:
        return '%d'%(int(m.group(1), 16))
    return ''

def username(f):
    x = open(f).read().replace('\x00', '')
    REGEX_USERNAME = re.compile(six.u(r'S:"Username"=([^\r\n]*)'))
    m = REGEX_USERNAME.search(x)
    if m:
        return m.group(1)
    return ''

if __name__ == '__main__':

    file_list = sys.argv
    file_list.pop(0) 

    for file in file_list:
        print('ssh -p '+port(file)+' '+username(file)+'@'+hostname(file)+' #'+password(file))
