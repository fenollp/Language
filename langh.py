tree = []
## ( (a) c ( b )((()E)) )
# [{pos:0, len:20, childs:6},
#   [{pos:2, len:1, content:" "}],
#   [{pos:, len:1, childs:1},
#     {pos:, len:1, content:"a"}
#   ],
#   [{pos:, len:3, content:" c "}],
#   [{pos:, len:, childs:1}, {item:" b "}],
#   [{…},
#     [{…},
#       [{pos:u, len:0, childs:0}],
#       {pos:v, len:1, content:"E"}
#     ]
#   ],
#   [{item:" "}]
# ]

I = """( (a) c ( b )((()E)) )"""
i = 0
L = len(I)
a = ''
tree = []

while i < L:
    if '(' == I[i]:
        if current['content']:    # if is an item
            current['len'] = current['pos'] - i + 1
            current['content'] = a

        new = [{'pos':i, 'len':-1, 'childs':-1}]
        current.append(new)
        current = current.child(-1)    # current's last child

    elif ')' == I[i]:
        current['len'] = current['pos'] - i + 1
        current['childs'] = count(current)
        current = current.parent()

    else
        tok += I[i]

    i += 1

print tree

