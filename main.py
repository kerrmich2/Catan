from map import Map

# Default parameters for default seafarers
seafarers_geography = {
    "sea": 17,
    "desert": 0,
    "gold_fields": 2,
    "fields": 5,
    "hills": 4,
    "mountains": 4,
    "pastures": 5,
    "forests": 5}
seafarers_numbers = {
    2: 2,
    3: 3,
    4: 3,
    5: 3,
    6: 2,
    8: 2,
    9: 3,
    10: 3,
    11: 2,
    12: 2}

# Default parameters for a large Catan board
large_seafarers_geography = {
    "sea": 24,
    "desert": 0,
    "gold_fields": 4,
    "fields": 7,
    "hills": 7,
    "mountains": 7,
    "pastures": 7,
    "forests": 7}
large_seafarers_numbers = {
    2: 2,
    3: 3,
    4: 4,
    5: 5,
    6: 5,
    8: 5,
    9: 5,
    10: 4,
    11: 3,
    12: 3}

# Default Catan
default_catan_geography = {
    "desert": 1,
    "fields": 4,
    "hills": 3,
    "mountains": 3,
    "pastures": 4,
    "forests": 4}
default_catan_numbers = {
    2: 1,
    3: 2,
    4: 2,
    5: 2,
    6: 2,
    8: 2,
    9: 2,
    10: 2,
    11: 2,
    12: 1}

# Test parameters
test_large_seafarers_geography = {
    "sea": 24,
    "desert": 0,
    "gold_fields": 4,
    "fields": 7,
    "hills": 7,
    "mountains": 7,
    "pastures": 7,
    "forests": 7}
test_large_seafarers_numbers = {
    2: 2,
    3: 3,
    4: 4,
    5: 5,
    6: 5,
    8: 5,
    9: 5,
    10: 4,
    11: 3,
    12: 3}

# Default parameters for a large Catan board
extra_large_seafarers_geography = {
    "sea": 31,
    "desert": 0,
    "gold_fields": 4,
    "fields": 7,
    "hills": 7,
    "mountains": 7,
    "pastures": 7,
    "forests": 7}
extra_large_seafarers_numbers = {
    2: 2,
    3: 3,
    4: 4,
    5: 5,
    6: 5,
    8: 5,
    9: 5,
    10: 4,
    11: 3,
    12: 3}

# Default Catan
# Map(5, 3, False, default_catan_geography, default_catan_numbers).main()

# 6 player seafarers Catan
# Map(7, 8, True, large_seafarers_geography, large_seafarers_numbers).main()

# 6 player seafarers Catan
# Map(7, 8, True, large_seafarers_geography, large_seafarers_numbers).main()

# 4 player seafarers Catan
Map(7, 5, True, seafarers_geography, seafarers_numbers).main()

# 6 player seafarers Catan TEST
# Map(7, 8, True, test_large_seafarers_geography, test_large_seafarers_numbers).main()
