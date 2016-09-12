from flask import Blueprint, request, render_template, redirect, url_for

mod_user = Blueprint('user', __name__, url_prefix='/user')

@mod_user.route('/', methods=['POST', 'GET'])
def test():
	return "This is user route"