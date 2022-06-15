from flask_marshmallow import Marshmallow

from .models import Recipe, Coops, Ingredients, Tips

ma = Marshmallow()


class CoopsSchema(ma.Schema):
    class Meta:
        model = Coops
        # fields to expose
        fields = ("id", "name", "age", "breed", "number_of_chickens", "date_added", "date_for_next_feed")


ma = Marshmallow()


class RecipeSchema(ma.Schema):
    class Meta:
        model = Recipe
        # Fields to expose

        fields = ("id", "feed", "number_of_days_to feed", "result", "coops")  # " user_id ")

    category = ma.Nested(CoopsSchema)


class IngredientsSchema(ma.Schema):
    class Meta:
        model = Ingredients
        fields = ("id", "wmaize", "soya", "fishm", "maizeb", "limes", "wheat")  # " user_id ")


class RecipeIngredientsSchema(ma.Schema):
    class Meta:
        model = Recipe
        # Fields to expose

        fields = ("id", "feed", "number_of_days_to feed", "result", "ingredients")  # " user_id ")

    ingredients = ma.Nested(IngredientsSchema)


class ProfileSchema(ma.Schema):
    class Meta:
        # fields to expose for current user profile
        fields = ("id", "username", "email", "date_added", "phone")


class TipsSchema(ma.Schema):
    class Meta:
        model = Tips
        fields = ("title", "id", "content", "date_added")
