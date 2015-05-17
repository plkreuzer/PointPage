# Line format: {name},{attribute},{value}
#     example: child3,allowance,20
#              child3,points,10
#              child2,points,20
#              child1,allowance,10

import os
import sys
import string

db = {}

fname = 'database.txt'
file = open(fname)
for line in file :
    result = line.lower().split()
    db[result[0]][result[1]] += result[2]
    

file.close()

