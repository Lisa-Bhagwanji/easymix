from flask_marshmallow import Marshmallow


ma = Marshmallow()


class RecipeSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ("id", "feed", "amount_entered", "result") #" user_id ")
    
class ProfileSchema(ma.Schema):
    class Meta:
        #fields to expose for current user profile
        fields = ("id", "username", "email", "date_added", "phone")
    
class CoopsSchema(ma.Schema):
    class Meta:
        #fields to expose 
        fields = ("id", "name", "age", "breed", "number")