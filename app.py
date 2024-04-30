from flask import Flask, render_template, redirect, request
from flask_debugtoolbar import DebugToolbarExtension
from models import db, Pet
from forms import AddPetForm, PetEditForm

app =  Flask(__name__)
debug = DebugToolbarExtension(app)

app.config["SECRET_KEY"] =  "shh"
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://Pets"
app.config["SQLALCHEMY_TRACK_MODIFCATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True

db.init_app(app)
app.app_context().push()

#Make Homepage Listing Pets
@app.route("/")
def homepage():
    '''Pet Home Page Displays all Pets Available/Not Available'''
    pets = Pet.query.all()
    return render_template("home.html", pets = pets)

@app.route("/add", methods = ["GET","POST"])
def addPetForm():
    '''From for Adding a New Pet'''
    form = AddPetForm()

    if form.validate_on_submit():
        name = form.name.data
        species = form.species.data
        if(form.photo_url.data != ""):
            photo_url = form.photo_url.data
        else:
            None
        if(form.age.data):
            age = form.age.data
        else:
            None
        if(form.notes.data != ""):
            notes = form.notes.data
        else: 
            None
        
        newPet = Pet(name=name, species=species, photo_url=photo_url, age=age, notes=notes)
        db.session.add(newPet)
        db.session.commit()
        
    
    else: 
        return render_template("add_pet_form.html", form=form)
    
@app.route("/<int:pet_id>", methods = ["GET","POST"])
def display_edit(pet_id):
    '''Pet Details and Form for Edits'''
    pet = Pet.query.get(pet_id)
    form = PetEditForm()

    if form.validate_on_submit():
        pet.photo_url = form.photo_url.data
        pet.notes = form.notes.data
        pet.available = form.available.data

        db.session.commit()

        return redirect("/<int:pet_id>", pet_id = pet_id)

    
    if request.method == "GET":
        form.photo_url.data = pet.photo_url
        form.notes.data = pet.notes
        form.available.data = pet.available

    return render_template("pet_details.html", pet= pet, form = form)


