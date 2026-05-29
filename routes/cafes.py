from flask import Blueprint, render_template, abort
from database.models import Cafe, MenuItem
from itertools import groupby

cafes_bp = Blueprint("cafes", __name__, url_prefix="/cafes")


@cafes_bp.route("/")
def cafe_list():
    cafes = Cafe.query.all()
    return render_template("cafes.html", cafes=cafes)


@cafes_bp.route("/<int:cafe_id>")
def cafe_detail(cafe_id):
    cafe = Cafe.query.get_or_404(cafe_id)

    # Group menu items by category
    items = MenuItem.query.filter_by(cafe_id=cafe_id).order_by(MenuItem.category).all()
    menu_by_category = {}
    for item in items:
        menu_by_category.setdefault(item.category, []).append(item)

    return render_template("cafe_detail.html", cafe=cafe, menu=menu_by_category)
