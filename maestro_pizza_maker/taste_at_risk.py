# The maestro pizza maker is aware of the fact that the fat content of the ingredients is random and it is not always the same.
# Since fat is the most important factor in taste, the maestro pizza maker wants to know how risky his pizza menu is.

# TODO: define 2 risk measures for the pizza menu and implement them (1 - Taste at Risk (TaR), 2 - Conditional Taste at Risk (CTaR), also known as Expected Shorttaste (ES)

from maestro_pizza_maker.pizza import Pizza
from maestro_pizza_maker.pizza_menu import PizzaMenu
import numpy as np
#As we know that taste function returns np.array 
#Value at risk

def taste_at_risk_pizza(pizza: Pizza, quantile: float) -> float:
    # TODO: implement the taste at risk measure for a pizza
    # quantile is the quantile that we want to consider
    # Hint: Similarity between the Taste at Risk and the Value at Risk is not a coincidence or is it?
    # Hint: Use function taste from Pizza class, but be aware that the higher the taste, the better -> the lower the taste, the worse
    return np.quantile(pizza.taste, 1 - quantile) #NOTE: here 1-quantile because higher the taste better so to find worst cases we need to look fo lowertail

#NOTE:risk of a portfolio always less or equal than the sum total of risks of individual assets in a portfolio
def taste_at_risk_menu(menu: PizzaMenu, quantile: float) -> float:
    # TODO: implement the taste at risk measure for a menu
    # quantile is the quantile that we want to consider
    # Hint: the taste of the whole menu is the sum of the taste of all pizzas in the menu, or? ;)
    menu_taste = np.array([pizza.taste for pizza in menu.pizzas])
    final_menu_taste = np.sum(menu_taste, axis = 0)
    return np.quantile(final_menu_taste, 1 - quantile)


def conditional_taste_at_risk_pizza(pizza: Pizza, quantile: float) -> float:
    # TODO: implement the conditional taste at risk measure for a pizza
    # quantile is the quantile that we want to consider
    # Hint: Simmilarity between the Conditional Taste at Risk and the Conditional Value at Risk is not a coincidence or is it?
    threshold = np.quantile(pizza.taste, 1 - quantile)
    worst_tastes = pizza.taste[pizza.taste <= threshold]
    return np.mean(worst_tastes)


def conditional_taste_at_risk_menu(menu: PizzaMenu, quantile: float) -> float:
    # TODO: implement the conditional taste at risk measure for a menu
    # Hint: the taste of the whole menu is the sum of the taste of all pizzas in the menu, or? ;) (same as for the taste at risk)
    menu_taste = np.array([pizza.taste for pizza in menu.pizzas])
    final_menu_taste = np.sum(menu_taste, axis = 0)
    threshold =  np.quantile(final_menu_taste, 1 - quantile)
    worst_tastes = final_menu_taste[final_menu_taste <= threshold]
    return np.mean(worst_tastes)
