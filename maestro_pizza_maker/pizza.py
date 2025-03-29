# class representing a pizza

from dataclasses import dataclass
from typing import List, Literal, Optional

from maestro_pizza_maker.ingredients import PizzaIngredients
import numpy as np
import uuid


@dataclass
class Pizza:
    dough: Literal[
        PizzaIngredients.CLASSIC_DOUGH,
        PizzaIngredients.THIN_DOUGH,
        PizzaIngredients.WHOLEMEAL_DOUGH,
    ]
    sauce: Literal[PizzaIngredients.TOMATO_SAUCE, PizzaIngredients.CREAM_SAUCE]
    cheese: Optional[
        List[
            Literal[
                PizzaIngredients.MOZZARELA,
                PizzaIngredients.CHEDDAR,
                PizzaIngredients.PARMESAN,
            ]
        ]
    ] = None
    fruits: Optional[
        List[Literal[PizzaIngredients.PINEAPPLE, PizzaIngredients.APPLE]]
    ] = None
    meat: Optional[
        List[
            Literal[
                PizzaIngredients.HAM, PizzaIngredients.BACON, PizzaIngredients.SAUSAGE
            ]
        ]
    ] = None
    vegetables: Optional[
        List[
            Literal[
                PizzaIngredients.MUSHROOMS,
                PizzaIngredients.ONIONS,
                PizzaIngredients.PEPPER,
            ]
        ]
    ] = None

    def __post_init__(self) -> None:
        if self.cheese is None:
            self.cheese = []
        if self.fruits is None:
            self.fruits = []
        if self.meat is None:
            self.meat = []
        if self.vegetables is None:
            self.vegetables = []
        self.ingredients = [
            self.dough,
            self.sauce,
            *self.cheese,
            *self.fruits,
            *self.meat,
            *self.vegetables,
        ]

    @property
    def price(self) -> float:
        return sum(ingredient.value.price for ingredient in self.ingredients)

    @property
    def protein(self) -> float:
        return sum(ingredient.value.protein for ingredient in self.ingredients)

    @property
    def fat(self) -> np.array:
        return sum(ingredient.value.fat for ingredient in self.ingredients)

    @property
    def average_fat(self) -> float:
        # TODO: implement average fat calculation
        # HINT: check the `PizzaIngredients` class properly, you will find a `fat` property there which is a numpy array representing the drawings from the fat distribution
        # since fat is a random variable, we will calculate the average fat of the pizza by averaging the fat vectors of the ingredients
        fat_vectors = [ingredient.value.fat for ingredient in self.ingredients]
        avg_fat_vectors = np.mean(fat_vectors, axis=0) 
        # NOTE: averaging the fat_vectors for each simulation points But still a bit confused about the HINT
        return float(np.mean(avg_fat_vectors))

    @property
    def carbohydrates(self) -> float:
        return sum(ingredient.value.carbohydrates for ingredient in self.ingredients)

    @property
    def calories(self) -> float:
        return sum(ingredient.value.calories for ingredient in self.ingredients)

    @property
    def name(self) -> str:
        # TODO: implement name generation, it is purely up to you how you want to do it
        # (you can use random, you can use some kind of algorithm) - just make sure that
        # the name is unique.
        name = "_".join(sorted([ingredient.value.name.replace(' ','_') for ingredient in self.ingredients]))
        suffix = uuid.uuid4().hex[:6]
        return f"{name}_{suffix}"

    @property
    def taste(self) -> np.array:
        # TODO: implement taste function
        # The famous fact that taste is subjective is not true in this case. We believe that fat is the most important factor, since fat carries the most flavor.
        # So we will use the fat vector to calculate the taste of the pizza with the following formula:
        # taste = 0.05 * fat_dough + 0.2 * fat_sauce + 0.3 * fat_cheese + 0.1 * fat_fruits + 0.3 * fat_meat + 0.05 * fat_vegetables
        fat_dough = self.dough.value.fat * 0.05
        fat_sauce = self.sauce.value.fat * 0.2
        fat_cheese = (
        np.sum([c.value.fat for c in self.cheese], axis=0) * 0.3
        if self.cheese
        else 0
        )
        fat_fruits = (
        np.sum([f.value.fat for f in self.fruits], axis=0) * 0.1
        if self.fruits
        else 0
        )
        fat_meat = (
        np.sum([m.value.fat for m in self.meat], axis=0) * 0.3
        if self.meat
        else 0
        )
        fat_vegetables = (
            np.sum([v.value.fat for v in self.vegetables], axis=0) * 0.05
            if self.vegetables
            else 0
        )
        return fat_dough+fat_sauce+fat_cheese+fat_fruits+fat_meat+fat_vegetables


