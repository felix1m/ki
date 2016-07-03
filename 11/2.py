
a = (1,2)
b = (3,1)
c = (2,4)
d = (6,5)
e = (8,4)
f = (1,6)

all=[a,b,c,d,e,f]

def sq_distance(a,b):
  return (a[0] - b[0])**2 + (a[1] - b[1])**2

def sq_distance_row(a):
  return [sq_distance(a, x) for x in all]

def sq_distance_all():
  return [sq_distance_row(x) for x in all]

print(sq_distance_all())
# =
# [[0, 5, 5, 34, 53, 16],
#  [5, 0, 10, 25, 34, 29],
#  [5, 10, 0, 17, 36, 5],
#  [34, 25, 17, 0, 5, 26],
#  [53, 34, 36, 5, 0, 53],
#  [16, 29, 5, 26, 53, 0]]
# Nun Denke man sich in jeder Zeile eine Wurzel dazu :)


# b)
# =========

#     a   b   c   d   e   f
# a   0,  5,  5,  34, 53, 16
# b   0,  0,  10, 25, 34, 29
# c   0,  0,  0,  17, 36, 5
# d   0,  0,  0,  0,  5,  26
# e   0,  0,  0,  0,  0,  53
# f   0,  0,  0,  0,  53, 0

#     a   b,c d   e   f
# a   0,  5,  34, 53, 16
# b,c 0,  0,  25, 34, 29
# d   0,  0,  0,  5,  26
# e   0,  0,  0,  0,  53
# f   0,  0,  0,  53, 0


#       a,b,c d   e   f
# a,b,c 0,    25, 34, 16
# d     0,    0,  5,  26
# f     0,    0,  53, 0

#       a,b,c d,e f
# a,b,c 0,    5,  16
# d,e   0,    0,  26
# f     0,    0,  0


# immer noch alles im wurzeln


