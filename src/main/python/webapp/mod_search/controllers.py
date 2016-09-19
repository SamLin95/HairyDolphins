from flask import Blueprint, request, render_template, redirect, url_for

mod_search = Blueprint('search', __name__, url_prefix='/search')

@mod_search.route('/laSearch', methods=['POST', 'GET'])
def searchLocalAdvisors():
    return render_template('laSearch.html')

@mod_search.route('/rdSearch', methods=['POST', 'GET'])
def search_recommendations():
    return render_template('recommendations.html')
