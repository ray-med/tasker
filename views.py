from flask import Blueprint, render_template, request, jsonify, redirect, url_for
import psycopg2

def get_html_table(headers, body):
    html_table = '<table>'

    html_table += '<tr>'
    for col in headers:
        html_table += f'<th>{col}</th>'
    html_table += '</tr>'

    for row in body:
        html_table += '<tr>'
        for cell in row:
            html_table += f'<td>{str(cell)}</td>'
        html_table += '</tr>'
    html_table += '</table>'
    return html_table

views = Blueprint(__name__, 'views')


@views.route('/')
def home():
    return render_template('index.html', name='Leo', age=36)

@views.route('/profile')
def profile():
    return render_template('profile.html')

@views.route('/dbas')
def getDBAs():
    # 1 Get info from the Database (list of tuples)
    URI = 'postgresql://postgres:postgres@192.168.1.114:5432/prod'

    with psycopg2.connect(URI) as conn:
        with conn.cursor() as cur:
            cur.execute('SELECT * FROM cik_dba')
            column_names = [desc[0] for desc in cur.description]
            DBAs = cur.fetchall()


    # 2 Show info like a text
    html_table = get_html_table(column_names, DBAs)
    return render_template('dbas.html', msg=html_table)


@views.route('/json')
def get_json():
    return jsonify({'name': 'leo', 'coolness': 10})

@views.route('/data')
def get_data():
    data = request.json
    return jsonify(data)

@views.route('/go-to-home')
def go_to_home():
    return redirect(url_for('views.home'))



