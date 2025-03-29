import pytest
import numpy as np
import pandas as pd
from maestro_pizza_maker.ingredients import PizzaIngredients
from maestro_pizza_maker.pizza import Pizza
from maestro_pizza_maker.pizza_menu import PizzaMenu

def test_pizza_creation():
    pizza = Pizza(
        dough=PizzaIngredients.CLASSIC_DOUGH,
        sauce=PizzaIngredients.TOMATO_SAUCE,
        cheese=[PizzaIngredients.MOZZARELA],
        meat=[PizzaIngredients.HAM],
        vegetables=[PizzaIngredients.MUSHROOMS]
    )
    assert isinstance(pizza, Pizza)

def test_average_fat_property():
    pizza = Pizza(
        dough=PizzaIngredients.CLASSIC_DOUGH,
        sauce=PizzaIngredients.TOMATO_SAUCE
    )
    expected_fat = np.mean([PizzaIngredients.CLASSIC_DOUGH.value.fat,
                           PizzaIngredients.TOMATO_SAUCE.value.fat],axis=0)
    assert pizza.average_fat == pytest.approx(float(np.mean(expected_fat)))

def test_taste_property():
    pizza = Pizza(
        dough=PizzaIngredients.CLASSIC_DOUGH,
        sauce=PizzaIngredients.TOMATO_SAUCE,
        cheese=[PizzaIngredients.MOZZARELA,PizzaIngredients.CHEDDAR]
    )
    expected_taste = (
        PizzaIngredients.CLASSIC_DOUGH.value.fat * 0.05 +
        PizzaIngredients.TOMATO_SAUCE.value.fat * 0.2 +
        sum([PizzaIngredients.MOZZARELA.value.fat,PizzaIngredients.CHEDDAR.value.fat]) * 0.3
    )
    assert np.allclose(pizza.taste, expected_taste)

def test_name_property():
    pizza = Pizza(
        dough=PizzaIngredients.CLASSIC_DOUGH,
        sauce=PizzaIngredients.TOMATO_SAUCE
    )
    assert isinstance(pizza.name, str)
    assert "CLASSIC_DOUGH" in pizza.name
    assert "TOMATO_SAUCE" in pizza.name

@pytest.fixture
def sample_pizzas():
    pizza1 = Pizza(
        dough=PizzaIngredients.CLASSIC_DOUGH,
        sauce=PizzaIngredients.TOMATO_SAUCE,
        cheese=[PizzaIngredients.MOZZARELA]
    )
    pizza2 = Pizza(
        dough=PizzaIngredients.THIN_DOUGH,
        sauce=PizzaIngredients.CREAM_SAUCE,
        meat=[PizzaIngredients.HAM]
    )
    pizza3 = Pizza(
        dough=PizzaIngredients.WHOLEMEAL_DOUGH,
        sauce=PizzaIngredients.TOMATO_SAUCE,
        vegetables=[PizzaIngredients.MUSHROOMS, PizzaIngredients.ONIONS]
    )
    return [pizza1, pizza2, pizza3]

@pytest.fixture
def pizza_menu(sample_pizzas):
    return PizzaMenu(pizzas=sample_pizzas)

def test_to_dataframe(pizza_menu):
    df = pizza_menu.to_dataframe(sort_by="price", descendent=True)
    assert isinstance(df, pd.DataFrame)
    assert list(df.columns) == ['name', 'price', 'protein', 'average_fat', 'carbohydrates', 'calories', 'ingredients']
    assert df['price'].is_monotonic_decreasing
    assert len(df) == len(pizza_menu.pizzas)  

def test_cheapest_pizza(pizza_menu):
    cheapest = pizza_menu.cheapest_pizza
    assert all(cheapest.price <= p.price for p in pizza_menu.pizzas)

def test_most_caloric_pizza(pizza_menu):
    most_caloric = pizza_menu.most_caloric_pizza
    assert all(most_caloric.calories >= p.calories for p in pizza_menu.pizzas)

def test_get_most_fat_pizza(pizza_menu):
    most_fat = pizza_menu.get_most_fat_pizza(quantile=0.5)
    for pizza in pizza_menu.pizzas:
        assert np.quantile(most_fat.fat, 0.5) >= np.quantile(pizza.fat, 0.5)

def test_add_pizza(pizza_menu):
    new_pizza = Pizza(
        dough=PizzaIngredients.CLASSIC_DOUGH,
        sauce=PizzaIngredients.TOMATO_SAUCE
    )
    initial_length = len(pizza_menu)
    pizza_menu.add_pizza(new_pizza)
    assert len(pizza_menu) == initial_length + 1
    assert new_pizza in pizza_menu.pizzas

def test_remove_pizza(pizza_menu):
    pizza_to_remove = pizza_menu.pizzas[0]
    initial_length = len(pizza_menu)
    pizza_menu.remove_pizza(pizza_to_remove)
    assert len(pizza_menu) == initial_length - 1
    assert pizza_to_remove not in pizza_menu.pizzas

def test_remove_nonexistent_pizza(pizza_menu):
    non_existent_pizza = Pizza(
        dough=PizzaIngredients.CLASSIC_DOUGH,
        sauce=PizzaIngredients.TOMATO_SAUCE
    )
    with pytest.raises(ValueError):
        pizza_menu.remove_pizza(non_existent_pizza)

def test_len(pizza_menu):
    assert len(pizza_menu) == len(pizza_menu.pizzas)