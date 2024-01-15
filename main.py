from map import Map

# Default parameters for large Catan board
geography = {"sea": 24,
             "desert": 0,
             "gold_fields": 4,
             "fields": 7,
             "hills": 7,
             "mountains": 7,
             "pastures": 7,
             "forests": 7}
numbers = {2: 2,
           3: 3,
           4: 4,
           5: 5,
           6: 5,
           8: 5,
           9: 5,
           10: 4,
           11: 3,
           12: 3}

for i in range(4):
    Map(7, 8, True, geography, numbers).main()








