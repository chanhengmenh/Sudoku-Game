from itertools import islice

width, height = 450, 450
num_cell = 9
cell_size = (width // num_cell, height // num_cell)

# Convert 1D list to 2D list
def convert_list(lst, var_lst):
    it = iter(lst)
    return [list(islice(it, i)) for i in var_lst]
