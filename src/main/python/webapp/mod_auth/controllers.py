from flask import Blueprint, request, render_template, redirect, url_for

mod_auth = Blueprint('auth', __name__, url_prefix='/auth')

@mod_auth.route('/', methods=['POST', 'GET'])
def test():
	return "This is authentication route"