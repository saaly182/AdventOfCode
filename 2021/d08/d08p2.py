#!/usr/bin/python3 -u
'''
  0:      1:      2:      3:      4:
 aaaa    ....    aaaa    aaaa    ....
b    c  .    c  .    c  .    c  b    c
b    c  .    c  .    c  .    c  b    c
 ....    ....    dddd    dddd    dddd
e    f  .    f  e    .  .    f  .    f
e    f  .    f  e    .  .    f  .    f
 gggg    ....    gggg    gggg    ....

  5:      6:      7:      8:      9:
 aaaa    aaaa    aaaa    aaaa    aaaa
b    .  b    .  .    c  b    c  b    c
b    .  b    .  .    c  b    c  b    c
 dddd    dddd    ....    dddd    dddd
.    f  e    f  .    f  e    f  .    f
.    f  e    f  .    f  e    f  .    f
 gggg    gggg    ....    gggg    gggg

2 segments: 1
3 segments: 7
4 segments: 4
5 segments: 2, 3, 5
6 segments: 0, 6, 9
7 segments: 8

e appears in 4 numbers
b appears in 6 numbers
d appears in 7 numbers
g appears in 7 numbers
a appears in 8 numbers
c appears in 8 numbers
f appears in 9 numbers

2 segments letters must be C and F
3 segments, the one not part of 2 segments must be A
'''

debug = False

digit_signature = {
    'abcefg'  : 0,
    'cf'      : 1,
    'acdeg'   : 2,
    'acdfg'   : 3,
    'bcdf'    : 4,
    'abdfg'   : 5,
    'abdefg'  : 6,
    'acf'     : 7,
    'abcdefg' : 8,
    'abcdfg'  : 9,
}

def readdigit(dstr):
  '''Return the int corresponding to the display segments, or None.'''
  dnorm = ''.join(sorted(dstr))
  if debug:
    print(f'dstr={dstr} dnorm={dnorm}')
  if dnorm in digit_signature:
    return(digit_signature[dnorm])
  else:
    return None


def computemap(s):
  '''Return a map of input->output connections given a list of signals.'''
  smap = {}

  # First figure out what input maps to 'a'
  d1 = [x for x in s if len(x) == 2][0]
  d7 = [x for x in s if len(x) == 3][0]
  m_a = (set(d7) - set(d1)).pop()
  smap[m_a] = 'a'

  # Now use occurrence counts to find more
  letters = ''.join(s)
  letcount = {}
  for L in 'abcdefg':
    letcount[L] = letters.count(L)
  m_b = [x for x in letcount if letcount[x] == 6][0]
  m_e = [x for x in letcount if letcount[x] == 4][0]
  m_f = [x for x in letcount if letcount[x] == 9][0]
  smap[m_b] = 'b'
  smap[m_e] = 'e'
  smap[m_f] = 'f'

  # 'c' and 'a' occur 8 times, but we already know 'a'
  m_c = set(set([x for x in letcount if letcount[x] == 8]) - set((m_a,))).pop()
  smap[m_c] = 'c'

  # Use '4' to find 'd'
  d4 = [x for x in s if len(x) == 4][0]
  m_d = (set(d4) - set((m_b, m_c, m_f))).pop()
  smap[m_d] = 'd'

  # Now 'g' is the last mapping left
  m_g = (set('abcdefg') - set(smap)).pop()
  smap[m_g] = 'g'

  if debug:
    print(f's={s}')
    print(f'smap={smap}')

  assert len(smap) == 7
  return smap


def display(smap, outs):
  '''Return the real number in the display given the connection map and the current display output.'''
  if debug:
     print(f'smap={smap} outs={outs}')
  n = []
  for a in outs:
     atrans = ''.join([smap[x] for x in a])
     if debug:
       print(f'a={a} atrans={atrans}')
     d = readdigit(atrans)
     assert d is not None
     n.append(d)
  ret = int(''.join([str(x) for x in n]))
  return(ret)


myinput = {}

with open('input.txt') as digitsfile:
  for line in digitsfile:
    line = line.rstrip()
    signals_str, outputs_str = line.split('|')
    signals = tuple(signals_str.split())
    outputs = tuple(outputs_str.split())
    myinput[signals] = outputs

answer = 0
for s in myinput:
  if debug:
    print(f's={s} myinput[s]={myinput[s]}')
  smap = computemap(s)
  display_out = display(smap, myinput[s])
  answer += display_out

print(answer)
