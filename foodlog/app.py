# -*- coding: utf-8 -*-
"""
"""
from pprint import pprint

from flask import Flask, request, render_template, jsonify

from text_parser import parser, ParseException

app = Flask(__name__)

@app.route('/parse')
def parse():
    text = request.values.get('text')
    try:
        data = dict(parser.parseString(text))
    except ParseException as exc:
        return jsonify(error=str(exc))
    return jsonify(text=text, data=data)

@app.route('/')
def input():
    return render_template('input.html')

@app.route("/favicon.ico")
def favicon():
    return send_from_directory("static", "favicon.ico", 
                               mimetype="image/vnd.microsoft.icon")

if __name__ == '__main__': 
    app.run(host='0.0.0.0', debug=True)