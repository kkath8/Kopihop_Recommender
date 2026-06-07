from flask import Blueprint, render_template
from database.models import Cafe

main_bp = Blueprint("main", __name__)

@main_bp.route("/")
def home():
    cafes = Cafe.query.all()        # fetch all cafes
    return render_template("home.html", cafes=cafes)