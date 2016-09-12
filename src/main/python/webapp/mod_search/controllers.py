from flask import Blueprint, request, render_template, redirect, url_for

mod_search = Blueprint('search', __name__, url_prefix='/search')

@mod_search.route('/', methods=['POST', 'GET'])
def test():
	return "This is search route"