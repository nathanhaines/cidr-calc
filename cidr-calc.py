#!/usr/bin/python3

# Copyright (c) 2018 by Steve Litt
# Expat License: https://directory.fsf.org/wiki/License:Expat
#  
#  Permission is hereby granted, free of charge, to any person
#  obtaining a copy of this software and associated
#  documentation files (the "Software"), to deal in the Software
#  without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense,
#  and/or sell copies of the Software, and to permit persons to
#  whom the Software is furnished to do so, subject to the
#  following conditions:
#  
#  The above copyright notice and this permission notice shall
#  be included in all copies or substantial portions of the
#  Software.
#  
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY
#  KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
#  WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR
#  PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL THE AUTHORS
#  OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR
#  OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
#  OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
#  SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE. 

# CIDR CALCULATOR VERSION 1.0

import sys
import string

def usage():
    print('USAGE: cidr-calc  ipaddr/maskbits',
            file=sys.stderr)
    print(' EXAMPLE: cidr-calc  192.168.100.128/28',
            file=sys.stderr)


def maskbits2netmaskstring(mbits):
    bign = 256**4  - 2**(32-mbits)
    arr = bigint2octet_arr(bign)
    return '{}.{}.{}.{}'.format(
            arr[0],
            arr[1],
            arr[2],
            arr[3],
            )


def octet_arr2bigint(arr):
    accum = 0
    for ss in range(0,4):
        accum = accum + (arr[3-ss] * 256**(ss))
    return(accum)


def bigint2octet_arr(bigint):
    divisor = 256
    arr=[0,0,0,0]
    ss=3
    while bigint > 0:
        remainder = bigint % divisor
        bigint -= remainder
        bigint /= divisor
        bigint = int(bigint)
        arr[ss] = remainder
        ss -= 1
    return arr


def octet_arr2string(numarr):
    st='{}.{}.{}.{}'.format(
            numarr[0],
            numarr[1],
            numarr[2],
            numarr[3])
    return st

def main():
    if len(sys.argv) != 2:
        print('\nWrong number of arguments.',
                file=sys.stderr)
        usage()
        sys.exit(1)

    specparts = sys.argv[1].split('/')
    if len(specparts) != 2:
        st='\nMalformed specification ({})'
        print(st.format(sys.argv[1]), file=sys.stderr)
        usage()
        sys.exit(1)

    # PARSE THE ARGUMENT
    ipstring = specparts[0]
    try:
        maskbits = int(specparts[1])
    except:
        st='\nMask bits must be integer, not "{}"'
        print(st.format(specparts[1], file=sys.stderr))
        usage()
        sys.exit(1)
    chunkexp = 32 - maskbits
    chunksize = 2**chunkexp

    # CONVERT ARG'S IP ADDRESS TO ARRAY OF 4 OCTET INTS
    octets = ipstring.split('.')
    if len(octets) > 4:
        st='\nToo many dots in IP address ({}).'
        print(st.format(ipstring, file=sys.stderr))
        usage()
        sys.exit(1)
    ss=0
    for st in octets:
        try:
            octets[ss] = int(st)
        except:
            st='\nIP address ({}) not numeric.'
            print(st.format(ipstring, file=sys.stderr))
            usage()
            sys.exit(1)
        ss += 1

    # CONVERT ARRAY OF 4 OCTETS TO AN INTEGER
    bignum = octet_arr2bigint(octets)
    
    # CALCULATE OUTPUT VALUES
    remainder = bignum % chunksize
    bignum_lowest = bignum - remainder
    bignum_highest = bignum_lowest + (chunksize - 1)
    octet_arr_lowest = bigint2octet_arr(bignum_lowest)
    octet_arr_highest = bigint2octet_arr(bignum_highest)
    ipstring_lowest = octet_arr2string(octet_arr_lowest)
    ipstring_highest = octet_arr2string(octet_arr_highest)

    # PRINT THE INFORMATION
    st='\nOriginal ip spec      : {}'
    print(st.format(sys.argv[1]))
    st = 'CIDR Network Notation : {}/{}'
    print(st.format(ipstring_lowest, maskbits))
    st = 'Netmask               : {}'
    print(st.format(maskbits2netmaskstring(maskbits)))
    st='IP range              : {} - {}'
    st=st.format(octet_arr2string(octet_arr_lowest),
            octet_arr2string(octet_arr_highest))
    print(st)
    st= 'Chunk size            : {} (2^{}) consecutive IPs'
    print(st.format(str(chunksize), str(chunkexp)))
    print('')

    
if __name__ == '__main__':
    main()
