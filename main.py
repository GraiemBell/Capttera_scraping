# from get_categories import get_categoreis
from get_products import get_info_products
import get_products2 as gp

from test import categories, category_links

# categories = categories[12:]
# category_links = category_links[12:]

# [63, 99, 141, 255]
# print(categories[0], category_links[0])
start_id = 141

for id, category in enumerate(categories[start_id:]):
    current_id = id+start_id
    print(current_id, category)
    gp.get_info_products(category_links[current_id]), 
