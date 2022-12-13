import copy
from flask import Blueprint, g
from app.unit_config import default_result
from app.utils.auth_utils import auth_user

general = Blueprint('general', __name__)


@general.before_request
@auth_user
def general_before_request():
    g.result = copy.deepcopy(default_result)

from app.api.general import general_controller