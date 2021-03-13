import pandas as pd
import json
import plotly
from flask import render_template
from flask_login import current_user
from flask_babel import _, lazy_gettext as _l
from ... import main
from .... import db
from ....models import Category, Diary, DrinkCondition

def to_label(drink_condition):
    if drink_condition == DrinkCondition.HUNGOVER:
        return _('Hungover')
    else:
        return ''

@main.route('/plot_drink', methods=['GET'])
def plot_drink():
    query = Diary.query.filter_by(user=current_user._get_current_object(), category=Category.DRINK)
    df = pd.read_sql(query.statement, db.engine)

    df['date'] = pd.to_datetime(df['date'])
    df = df.set_index(df['date'])
    df_1 = df.drop(columns=['date', 'id', 'user_id']).resample(rule='MS').count()
    df_2 = df.sort_index(ascending=False)[:30]
    df_2_hungover = df_2.loc[df_2['drink_condition'] == DrinkCondition.HUNGOVER, 'amt_of_drink']
    df_2_others = df_2.loc[df_2['drink_condition'] != DrinkCondition.HUNGOVER, 'amt_of_drink']

    print(df_2)
    graphs = [
        dict(
            data=[
                dict(
                    x=df_1.index,
                    # x=ts,
                    y=df_1.note,
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
        ),
        dict(
            data=[
                dict(
                    x=df_2_others.index,
                    y=df_2_others,
                    name=_('Not Bad'),
                    mode='markers',
                    type='scatter',
                    marker=dict(size=10),
                ),               
                dict(
                    x=df_2_hungover.index,
                    y=df_2_hungover,
                    name=_('Hungover'),
                    mode='markers',
                    type='scatter',
                    marker=dict(size=10),
                ),
            ],
            layout=dict(
                title=_('The amount of pure alcohol (g)') + ' - ' + _('How much alcohol do you drink these days?'),
                yaxis=dict(
                    title=_('The amount of pure alcohol (g)'),
                ),
            ),
        ),
        dict(
            data=[
                dict(
                    type='table',
                    header=dict(
                        values=[_('Date'), 'ALC(g)', _('Condition'), _('Note')],
                        fill=dict(color='grey'),
                        font=dict(color='white'),
                        ),
                    cells=dict(
                        values=[
                            df_2['date'].apply(lambda val: val.strftime('%Y-%m-%d')),
                            df_2['amt_of_drink'].apply(lambda val: val if val >= 0 else ''),
                            df_2['drink_condition'].apply(to_label),
                            df_2['note']],
                        align=[
                            'center',
                            'center',
                            'center',
                            'left',
                        ]),
                ),
            ],
            layout=dict(
                title=_(_('The diaries these days')),
                height=1000,
            ),
        ),        
    ]

    # Add "ids" to each of the graphs to pass up to the client
    # for templating
    ids = ['graph-{}'.format(i) for i, _ in enumerate(graphs)]

    # Convert the figures to JSON
    # PlotlyJSONEncoder appropriately converts pandas, datetime, etc
    # objects to their JSON equivalents
    graphJSON = json.dumps(graphs, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('plot/plot_drink.html',
                           ids=ids,
                           graphJSON=graphJSON)
