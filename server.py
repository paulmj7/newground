from flask import Flask, escape, request, render_template
import jinja2
from data_filtering import (
    get_df,
    filter_by_income, 
    filter_by_state, 
    filter_by_zipcode
)

app = Flask(__name__)
df = get_df()

@app.route('/', methods=['GET'])
def index():
    x = filter_by_income(df)
    zipdf = x.groupby('zip')['balance'].mean().reset_index()
    return render_template('hello.html', x=zipdf)

@app.route('/', methods=['POST'])
def get_income_reqs():
    if not request.form['val1'].isdigit():
        state_val = request.form['val1']
        x = filter_by_state(df, state_val)
    elif len(request.form['val1']) == 5 and request.form['val1'].isdigit():
        zip_val = request.form['val1']
        x = filter_by_zipcode(df, zip_val)
    else:
        min_val = float(request.form['val1'])
        max_val = float(request.form['max-val'])
        x = filter_by_income(df, min_val, max_val)
    zipdf = x.groupby('zip')['balance'].mean().reset_index()
    return render_template('hello.html', x=zipdf)
    

