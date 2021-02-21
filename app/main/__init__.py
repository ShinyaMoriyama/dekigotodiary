from flask import Blueprint

main = Blueprint('main', __name__)

from .views import index, payment, optional_category
from .views.diary import diary_common, diary_free, diary_sleep, diary_drink, diary_read, diary_option
from .views.plot import plot_free, plot_sleep, plot_drink, plot_read, plot_option
