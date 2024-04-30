from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, BooleanField
from wtforms.validators import ValidationError, Optional, URL, NumberRange

def validate_species(form, field):
    allowed_species = ["cat", "dog", "porcupine"]
    if field.data.lower() not in allowed_species:
        raise ValidationError("Species must be 'cat', 'dog', or 'porcupine'.")

class AddPetForm(FlaskForm):
    ''' Form for adding a pet '''

    name = StringField("Pet Name")
    species = StringField("Species", validators= [validate_species])
    photo_url = StringField("URL for Pet Photo", validators= [Optional(), URL(message= "Photo must be a URL")])
    age = IntegerField("Age", validators = [NumberRange(min=0, max=30, message= "Age must be between 0-30")])
    notes = StringField("Notes")

class PetEditForm(FlaskForm):
    '''Pet Edit form for adding/updating new info'''

    photo_url = StringField("Photo Url", validators = [URL()])
    notes = StringField("Notes")
    available = BooleanField("Available")
