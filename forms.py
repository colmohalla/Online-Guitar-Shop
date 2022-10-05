from ast import Pass
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, RadioField, IntegerField,FloatField
from wtforms.validators import InputRequired, EqualTo, NumberRange


class RegistrationForm(FlaskForm):
    user_id = StringField("User id:", validators=[InputRequired()])
    password = PasswordField("Password:", validators=[InputRequired()])
    password2 = PasswordField("Repeat password:",
                validators=[InputRequired(), EqualTo("password")])
    submit = SubmitField("Submit")

class LoginForm(FlaskForm):
    user_id = StringField("User id:", validators=[InputRequired()])
    password = PasswordField("Password:", validators=[InputRequired()])
    submit = SubmitField("Login")

class BuildForm(FlaskForm):
    shape = RadioField("Please select your basic guitar shape",
        choices = ["Stratocaster", "Les Paul", "SG", "Jazzmaster", "Telecaster", "Flying-V","Explorer", "Jaguar", "ES-335", "Mustang"],
        default = "Stratocaster")
    colour = RadioField("Please select your desired finish",
        choices = ["Candy-Apple Red","Pelham Blue","Olympic White", "Bull Black", "Shell Pink", "Seafoam Green", "Sunburst", "Gold-Top"],
        default = "Pelham Blue")
    wood = RadioField("Please select your preferred neckboard",
        choices = ["Maple", "Rosewood", "Ebony", "Swamp Ash", "Alder", "Walnut"],
        default = "Rosewood")
    pickup = RadioField("Please select your pickups",
        choices = ["Seymour Duncan P-90","Fender Vintera Single-Coil", "Maplegrove 6X Humbucker", "Seymour Duncan Double Barrel","Yellowbelly Humbucker"],
        default = "Seymour Duncan P-90")
    submit = SubmitField("Submit")

class CheckoutForm(FlaskForm):
    first_name = StringField("First name:", validators=[InputRequired()])
    surname = StringField("Surname:", validators=[InputRequired()])
    address = StringField("Address:", validators=[InputRequired()])
    delivery_method = RadioField("Please select a delivery method:", 
        choices = ["Standard", "Next Day"],
        default = "Standard")
    submit = SubmitField("Confirm Order")

class AdminForm(FlaskForm):
    admin_id = StringField("Admin ID:", validators=[InputRequired()])
    password= PasswordField("Password:", validators=[InputRequired()])
    submit = SubmitField("Login")

class StockForm(FlaskForm):
    name = StringField("Guitar model:", validators=[InputRequired()])
    price = FloatField("Price:", validators=[InputRequired()])
    image = StringField("Image URL:", validators=[InputRequired()])
    description = StringField("Description:", validators=[InputRequired()])
    submit = SubmitField("Update Stock")

class QuoteForm(FlaskForm):
    email = StringField("Please enter your email:", validators=[InputRequired()])
    submit = SubmitField("Send Me a Quote")






# 'pbkdf2:sha256:260000$OrRjtG9QOi7YeY5T$3f79465e7eae5abacd6022148de4ef6ed92bc29f48b15c685b06ce509a612ccb'