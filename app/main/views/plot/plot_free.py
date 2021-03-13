import pandas as pd
import json
import plotly
from flask import render_template
from flask_login import current_user
from flask_babel import _, lazy_gettext as _l
from ... import main
from .... import db
from ....models import Category, Diary

@main.route('/plot_free', methods=['GET'])
def plot_free():
    query = Diary.query.filter_by(user=current_user._get_current_object(), category=Category.FREE)
    df = pd.read_sql(query.statement, db.engine)

    df['date'] = pd.to_datetime(df['date'])
    df = df.set_index(df['date'])
    df = df.drop(columns=['date', 'id', 'user_id']).resample(rule='MS').count()

    graphs = [
        dict(
            data=[
                dict(
                    x=df.index,
                    # x=ts,
                    y=df.note,
                    type='bar',
                )
            ],
            layout=dict(
                title=_('The number of diaries by month'),
                xaxis=dict(
                    dtick='M1',
                ),
                yaxis=dict(
                    dtick='5',
                    title=_('The number of diaries'),
                ),
            ),
        )
    ]

    # Add "ids" to each of the graphs to pass up to the client
    # for templating
    ids = ['graph-{}'.format(i) for i, _ in enumerate(graphs)]

    # Convert the figures to JSON
    # PlotlyJSONEncoder appropriately converts pandas, datetime, etc
    # objects to their JSON equivalents
    graphJSON = json.dumps(graphs, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('plot/plot_free.html',
                           ids=ids,
                           graphJSON=graphJSON)
