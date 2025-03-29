# The maestro pizza maker wants to fully understand of the properties of his pizza menu.
# Therefore he defines the follwing variables in the pizza industry known as "pizza sensitivities":
# 1. menu_sensitivity_protein - represents the rate of change between the price of the pizza and the amount of protein in the pizza
# 2. menu_sensitivity_carbs - represents the rate of change between the price of the pizza and the amount of carbohydrates in the pizza
# 3. menu_sensitivity_fat - represents the rate of change between the price of the pizza and the amount of average_fat in the pizza

# TODO: implement above mentioned sensitivities
# hint: simple linear regression might be helpful

from maestro_pizza_maker.pizza_menu import PizzaMenu
import numpy as np
#we can use scipy or formula
def find_slope_lr(x, y):
    n = len(x)
    s_x = np.sum(x)
    s_y = np.sum(y)
    ss_xy = np.sum(x * y)
    ss_xx = np.sum(x * x)
    
    slope = (n * ss_xy - s_x * s_y) / (n * ss_xx - s_x * s_x)
    return slope

def menu_sensitivity_protein(menu: PizzaMenu) -> float:
    # TODO: implement according to the description above
    # dependent variable price(y) and protein is independent var (x)
    df=menu.to_dataframe("price",True)
    return find_slope_lr(df['protein'].values,df['price'].values)


def menu_sensitivity_carbs(menu: PizzaMenu) -> float:
    # TODO: implement according to the description above
    df = menu.to_dataframe("price", True)
    return find_slope_lr(df['carbohydrates'].values, df['price'].values)


def menu_sensitivity_fat(menu: PizzaMenu) -> float:
    # TODO: implement according to the description above
    df = menu.to_dataframe("price", True)
    return find_slope_lr(df['average_fat'].values, df['price'].values)
