# import folium
# from folium import plugins
# import pandas as pd
# import numpy as np
# from streamlit_echarts import st_echarts, st_pyecharts
# import streamlit as st
# from streamlit_folium import st_folium
# import requests
#
# st.set_page_config(layout='wide')
#
# df = pd.read_csv("../data.csv")
# # schools_by_state = df.groupby(by='LSTATE', as_index=False)['OBJECTID'].count()
# # schools_by_state
# # school_count = df.groupby()
# ga = df[(df['LSTATE'] == 'GA')]
# st.dataframe(ga)


# import pandas as pd
# from random import randint
# import streamlit as st
#
# from streamlit_echarts import JsCode
# from streamlit_echarts import st_echarts
#
# st.set_page_config(layout='wide')
#
# df = pd.read_csv("../data.csv")
# # ga = df[df['LSTATE']=='GA']
# gb = df.groupby(by=['LSTATE'], as_index=False)['OBJECTID'].count()
# st.dataframe(gb)
#
#
#
#
# def add_to_flare(n, flare):
#     children = flare["children"]
#
#     if len(n) == 2:
#         children.append({"name": n[0], "value": n[1]})
#     else:
#         for c in children:
#             if c["name"] == n[0]:
#                 add_to_flare(n[1:], c)
#                 return
#
#         children.append({"name": n[0], "children": []})
#         add_to_flare(n[1:], children[-1])
#
# flare = {
#     "name": "USA",
#     "children": []
# }
#
# for idx, i in gb[['LSTATE', 'OBJECTID']].iterrows():
#     add_to_flare(i, flare)
#
# # st.write(flare)
# data = flare
#
# for idx, _ in enumerate(data["children"]):
#     data["children"][idx]["collapsed"] = idx % 2 == 0
#
# option = {
#     "tooltip": {"trigger": "item", "triggerOn": "mousemove"},
#     "series": [
#         {
#             "type": "tree",
#             "data": [data],
#             "top": "1%",
#             "left": "7%",
#             "bottom": "1%",
#             "right": "20%",
#             "symbolSize": 7,
#             "label": {
#                 "position": "left",
#                 "verticalAlign": "middle",
#                 "align": "right",
#                 "fontSize": 9,
#             },
#             "leaves": {
#                 "label": {
#                     "position": "right",
#                     "verticalAlign": "middle",
#                     "align": "left",
#                 }
#             },
#             "emphasis": {"focus": "descendant"},
#             "expandAndCollapse": True,
#             "animationDuration": 550,
#             "animationDurationUpdate": 750,
#         }
#     ],
# }
# st_echarts(option, height="1500px")

import addfips
import altair as alt
import pandas as pd
import streamlit as st
from vega_datasets import data

st.set_page_config(layout='wide')
northeast = ["CT", "ME", "MA", "NH", "RI", "VT", "NJ", "NY", "PA"]
midwest = ["IL", "IN", "MI", "OH", "WI", "IA", "KS", "MN", "MO", "NE", "ND", "SD"]
south = ["DE", "FL", "GA", "MD", "NC", "SC", "VA", "WV", "DC", "AL", "KY", "MS", "TN", "AR", "LA", "OK", "TX"]
west = ["AZ", "CO", "ID", "MT", "NV", "NM", "UT", "WY", "AK", "CA", "HI", "OR", "WA"]
territory = ["GU", "MP", "AS", "PR", "VI"]

regions = {i: 'northeast' for i in northeast}
_ = {regions.update({i: 'midwest'}) for i in midwest}
_ = {regions.update({i: 'south'}) for i in south}
_ = {regions.update({i: 'west'}) for i in west}
_ = {regions.update({i: 'teritory'}) for i in territory}

if 'data' not in st.session_state:
    df = pd.read_csv('../data.csv', low_memory=False)
    st.session_state['data'] = df

df = st.session_state['data']
# df_profiling = ydata_profiling.ProfileReport(df)
# df_profiling
# r = df['LSTATE'].apply(lambda x: regions[x])
# df['region'] = r

# gb
#
# fig = px.sunburst(gb, path=['region', 'LSTATE'], values='OBJECTID')
#
# st.plotly_chart(fig, use_container_width=True)

st.dataframe(df.head(10))

#
# gb = df.groupby(by=['LSTATE'], as_index=False)['OBJECTID'].count()
#
# selection = alt.selection_point(encodings=['color'], value='grey')
#
# bar_state = alt.Chart(gb, width=800).mark_bar().encode(
#     y=alt.Y('LSTATE:N', sort='-x'),
#     x=alt.X('OBJECTID:Q', title="Number of Schools"),
#     # color=alt.Color('LSTATE', legend=None)
#     color=alt.condition(selection, alt.Color('LSTATE:N', legend=None, scale=alt.Scale(scheme='category20')), alt.value('lightgrey'))
#
# ).add_params(
#     selection
# ).properties(
#     width=300
# )
#
# text = bar_state.mark_text(
#     align='center',
#     baseline='middle',
#     dx=15  # Move the text above the bar
# ).encode(
#     text='OBJECTID:Q'
# )

# county_bar = alt.Chart(county).mark_bar().encode(
#     x=alt.X('OBJECTID:Q', title="Number of Schools"),
#     y=alt.Y('NMCNTY:N', sort='-x'),
#     color=alt.Color('NMCNTY:N', legend=None, scale=alt.Scale(scheme='category20')),
#     tooltip=[
#         alt.Tooltip('NMCNTY', title='County'),
#         alt.Tooltip('OBJECTID:Q', title='Number of Schools'),
#     ]
# ).transform_filter(
#     selection
# )
#
# states = alt.topo_feature(data.us_10m.url, 'states')
#
# af = addfips.AddFIPS()
# # value = df[['LSTATE', 'NMCNTY']].values.tolist()[0]
# # st.write(af.get_county_fips(value[1], value[0]))
# t = [int(af.get_state_fips(s)) for s in gb['LSTATE'].values]
# gb['id'] = t
# # st.write(gb)
# # st.write(states)
# # st.stop()
#
# # Define a selection for states
# state_selection = alt.selection_point(fields=['LSTATE'], toggle=True)
#
# state = alt.Chart(states, title=alt.Title('Number of Schools By State', anchor='middle')).mark_geoshape(
#     stroke='black',  # Color of the border
#     strokeWidth=1  # Thickness of the border
# ).encode(
#     color=alt.Color('OBJECTID:Q', title='Number of Schools'),
#     opacity=alt.condition(state_selection, alt.value(1), alt.value(0.2)),
#     # color=alt.condition(selection, alt.Color('OBJECTID:Q', legend=None, scale=alt.Scale(scheme='category20')), alt.value('lightgrey')),
#     tooltip=[
#         alt.Tooltip('LSTATE:N', title='State'),
#         alt.Tooltip('OBJECTID:Q', title='Number of Schools')
#     ]
# ).transform_lookup(
#     lookup='id',
#     from_=alt.LookupData(gb, 'id', ['OBJECTID', 'LSTATE'])
# ).project(
#     type='albersUsa'
# ).add_params(
#     state_selection
# ).properties(width=300, height=400)
#
# # Bar chart for counties in the selected state
# # bars = alt.Chart(county, title=f'Number of Schools in County').mark_bar().encode(
# #     y=alt.Y('NMCNTY:N', sort='-x', title=None),
# #     x=alt.X('OBJECTID:Q', title=None),
# #     opacity=alt.condition(state_selection, alt.value(1), alt.value(0.2)),
# #     color=alt.condition(state_selection, alt.Color('NMCNTY:N', legend=None), alt.value('lightgray')),
# #     tooltip=['NMCNTY:N', 'OBJECTID:Q']
# # ).transform_filter(
# #     state_selection
# # )
# #
# # chart = ((bar_state + text) | county_bar).properties(title="ABC")
# #
# # c = (state | bars)
# # st.write(state)
# # st.altair_chart(c, use_container_width=True)
#
#
# counties = alt.topo_feature(data.us_10m.url, 'counties')
# _c = [int(af.get_county_fips(county=c, state=s)) if af.get_county_fips(county=c, state=s) is not None else None for s, c in county[['LSTATE', 'NMCNTY']].values]
# county['id'] = _c
# county = county.dropna(subset='id').reset_index(drop=True)
# # st.dataframe(county.head())
#
# county_selection = alt.selection_point(fields=['NMCNTY'])
#
# c_map = alt.Chart(counties, title=alt.Title(f'Number of Schools by County', anchor='middle')).mark_geoshape(
#     stroke='black',  # Color of the border
#     strokeWidth=1,  # Thickness of the border
# ).encode(
#     color=alt.Color('OBJECTID:Q', title='Number of Schoolss'),
#     # color=alt.condition(county_selection, alt.Color('OBJECTID:Q', title="Number of Schools"), alt.value('lightgray')),
#     opacity=alt.condition(county_selection, alt.value(1), alt.value(0.2)),
#     # color=alt.condition(selection, alt.Color('OBJECTID:Q', legend=None, scale=alt.Scale(scheme='category20')), alt.value('lightgrey')),
#     tooltip=[
#         alt.Tooltip('NMCNTY:N', title='County'),
#         alt.Tooltip('OBJECTID:Q', title='Number of Schools')
#     ]
# ).transform_lookup(
#     lookup='id',
#     from_=alt.LookupData(county, 'id', ['OBJECTID', 'NMCNTY', 'LSTATE'])
# ).transform_filter(
#     state_selection
# ).project(
#     type='albersUsa'
# ).add_params(
#     county_selection
# )
#
#
# city_sel = alt.selection_point(fields=['LCITY'])
# city = df.groupby(by=['NMCNTY', 'LCITY'], as_index=False)['OBJECTID'].count()
# # st.dataframe(city.head())
#
# city_chart = alt.Chart(city, title=alt.Title(f'Number of Schools in City', anchor='middle')).mark_bar().encode(
#     x=alt.X('OBJECTID:Q', title=None),
#     y=alt.Y('LCITY:N', title=None, sort='-x'),
#     color=alt.Color('LCITY:N', legend=None),
#     tooltip = [
#         alt.Tooltip('LCITY:N', title='City'),
#         alt.Tooltip('OBJECTID:Q', title='Number of Schools')
#     ]
# ).transform_filter(
#     county_selection
# )


# ch = (state | c_map | city_chart).resolve_scale(color='independent')
# r = st.altair_chart(ch)
# st.write(r)

# school, student = st.tabs(['By Schools', 'By Students'])
with st.container(border=True):
    gb = df.groupby(by=['LSTATE'], as_index=False)['OBJECTID'].count()
    l,m,r = st.columns(3)
    with l:
        states = alt.topo_feature(data.us_10m.url, 'states')

        af = addfips.AddFIPS()
        t = [int(af.get_state_fips(s)) for s in gb['LSTATE'].values]
        gb['id'] = t
        state_selection = alt.selection_point(fields=['LSTATE'], toggle=True)

        state = alt.Chart(states, title=alt.Title('Schools By State', anchor='middle')).mark_geoshape(
            stroke='black',  # Color of the border
            strokeWidth=1  # Thickness of the border
        ).encode(
            color=alt.Color('OBJECTID:Q', scale=alt.Scale(scheme='yelloworangered'), legend=alt.Legend(title='Number of Schools', format='.3s')),
            opacity=alt.condition(state_selection, alt.value(1), alt.value(0.2)),
            # color=alt.condition(selection, alt.Color('OBJECTID:Q', legend=None, scale=alt.Scale(scheme='category20')), alt.value('lightgrey')),
            tooltip=[
                alt.Tooltip('LSTATE:N', title='State'),
                alt.Tooltip('OBJECTID:Q', title='Number of Schools')
            ]
        ).transform_lookup(
            lookup='id',
            from_=alt.LookupData(gb, 'id', ['OBJECTID', 'LSTATE'])
        ).project(
            type='albersUsa'
        ).add_params(
            state_selection
        )
        _l = st.altair_chart(state, on_select='rerun', use_container_width=True)
        selected_state = _l['selection']['param_1']
    with m:
        if selected_state:
            selected_state = selected_state[0]
            _state = df[df['LSTATE']==selected_state['LSTATE']]
            county = _state.groupby(by=['LSTATE','NMCNTY'], as_index=False)['OBJECTID'].count()

            counties = alt.topo_feature(data.us_10m.url, 'counties')
            _c = [int(af.get_county_fips(county=c, state=s)) if af.get_county_fips(county=c, state=s) is not None else None for s, c in county[['LSTATE', 'NMCNTY']].values]
            county['id'] = _c
            county = county.dropna(subset='id').reset_index(drop=True)
            # st.dataframe(county.head())

            county_selection = alt.selection_point(fields=['NMCNTY'])
            title = f'Schools by County in State {selected_state["LSTATE"]}' if selected_state else 'Number of Schools by County in USA'
            c_map = alt.Chart(counties, title=alt.Title(title, anchor='middle')).mark_geoshape(
                stroke='black',  # Color of the border
                strokeWidth=1,  # Thickness of the border
            ).encode(
                color=alt.Color('OBJECTID:Q', title='Number of Schools', scale=alt.Scale(scheme='yelloworangered')),
                # color=alt.condition(county_selection, alt.Color('OBJECTID:Q', title="Number of Schools"), alt.value('lightgray')),
                opacity=alt.condition(county_selection, alt.value(1), alt.value(0.2)),
                # color=alt.condition(selection, alt.Color('OBJECTID:Q', legend=None, scale=alt.Scale(scheme='category20')), alt.value('lightgrey')),
                tooltip=[
                    alt.Tooltip('NMCNTY:N', title='County'),
                    alt.Tooltip('OBJECTID:Q', title='Number of Schools')
                ]
            ).transform_lookup(
                lookup='id',
                from_=alt.LookupData(county, 'id', ['OBJECTID', 'NMCNTY', 'LSTATE'])
            ).project(
                type='albersUsa'
            ).add_params(
                county_selection
            )

            selected_county = st.altair_chart(c_map, on_select='rerun', use_container_width=True)
            selected_county = selected_county['selection']['param_1']
        else:
            selected_county = None
    with r:
        if selected_county:
            # st.write(_state)
            # st.write(selected_county)
            selected_county = selected_county[0]
            _county = _state[_state['NMCNTY']==selected_county['NMCNTY']]
            city = _county.groupby(by=['NMCNTY', 'LCITY'], as_index=False)['OBJECTID'].count()
            # city_sel = alt.selection_point(fields=['LCITY'])

            # st.dataframe(city.head())
            city_title = f"Schools by City in {selected_county['NMCNTY']}, {selected_state['LSTATE']}"
            city_chart = alt.Chart(city, title=alt.Title(city_title, anchor='middle')).mark_bar().encode(
                x=alt.X('OBJECTID:Q', title=None),
                y=alt.Y('LCITY:N', title=None, sort='-x'),
                color=alt.Color('LCITY:N', legend=None),
                tooltip = [
                    alt.Tooltip('LCITY:N', title='City'),
                    alt.Tooltip('OBJECTID:Q', title='Number of Schools')
                ]
            )

            text = city_chart.mark_text(
                align='center',
                baseline='middle',
                dx=10  # Move the text above the bar
            ).encode(
                text='OBJECTID:Q'
            )
            c = (city_chart + text)
            st.altair_chart(c, use_container_width=True)
        else:
            pass

with st.container(border=True):
    gb = df.groupby(by=['LSTATE'], as_index=False)['TOTAL'].sum()
    l, m, r = st.columns(3, )
    with l:
        states = alt.topo_feature(data.us_10m.url, 'states')

        af = addfips.AddFIPS()
        t = [int(af.get_state_fips(s)) for s in gb['LSTATE'].values]
        gb['id'] = t
        state_selection = alt.selection_point(fields=['LSTATE'], toggle=True)

        state = alt.Chart(states, title=alt.Title('Students By State', anchor='middle')).mark_geoshape(
            stroke='black',  # Color of the border
            strokeWidth=1  # Thickness of the border
        ).encode(
            color=alt.Color('TOTAL:Q', scale=alt.Scale(scheme='yelloworangered'), legend=alt.Legend(title='Number of Students', format='.3s')),
            opacity=alt.condition(state_selection, alt.value(1), alt.value(0.2)),
            # color=alt.condition(selection, alt.Color('OBJECTID:Q', legend=None, scale=alt.Scale(scheme='category20')), alt.value('lightgrey')),
            tooltip=[
                alt.Tooltip('LSTATE:N', title='State'),
                alt.Tooltip('TOTAL:Q', title='Number of Students')
            ]
        ).transform_lookup(
            lookup='id',
            from_=alt.LookupData(gb, 'id', ['TOTAL', 'LSTATE'])
        ).project(
            type='albersUsa'
        ).add_params(
            state_selection
        )
        _l = st.altair_chart(state, on_select='rerun', use_container_width=True)
        selected_state = _l['selection']['param_1']
    with m:
        if selected_state:
            selected_state = selected_state[0]
            _state = df[df['LSTATE'] == selected_state['LSTATE']]
            county = _state.groupby(by=['LSTATE', 'NMCNTY'], as_index=False)['TOTAL'].sum()

            counties = alt.topo_feature(data.us_10m.url, 'counties')
            _c = [int(af.get_county_fips(county=c, state=s)) if af.get_county_fips(county=c, state=s) is not None else None for s, c in county[['LSTATE', 'NMCNTY']].values]
            county['id'] = _c
            county = county.dropna(subset='id').reset_index(drop=True)
            # st.dataframe(county.head())

            county_selection = alt.selection_point(fields=['NMCNTY'])
            title = f'Students by County in State {selected_state["LSTATE"]}' if selected_state else 'Number of Student by County in USA'
            c_map = alt.Chart(counties, title=alt.Title(title, anchor='middle')).mark_geoshape(
                stroke='black',  # Color of the border
                strokeWidth=1,  # Thickness of the border
            ).encode(
                color=alt.Color('TOTAL:Q', title='Number of Students', scale=alt.Scale(scheme='yelloworangered')),
                # color=alt.condition(county_selection, alt.Color('OBJECTID:Q', title="Number of Schools"), alt.value('lightgray')),
                opacity=alt.condition(county_selection, alt.value(1), alt.value(0.2)),
                # color=alt.condition(selection, alt.Color('OBJECTID:Q', legend=None, scale=alt.Scale(scheme='category20')), alt.value('lightgrey')),
                tooltip=[
                    alt.Tooltip('NMCNTY:N', title='County'),
                    alt.Tooltip('TOTAL:Q', title='Number of Students')
                ]
            ).transform_lookup(
                lookup='id',
                from_=alt.LookupData(county, 'id', ['TOTAL', 'NMCNTY', 'LSTATE'])
            ).project(
                type='albersUsa'
            ).add_params(
                county_selection
            )

            selected_county = st.altair_chart(c_map, on_select='rerun', use_container_width=True)
            selected_county = selected_county['selection']['param_1']
        else:
            selected_county = None
    with r:
        if selected_county:
            # st.write(_state)
            # st.write(selected_county)
            selected_county = selected_county[0]
            _county = _state[_state['NMCNTY'] == selected_county['NMCNTY']]
            city = _county.groupby(by=['NMCNTY', 'LCITY'], as_index=False)['TOTAL'].sum()
            # city_sel = alt.selection_point(fields=['LCITY'])

            # st.dataframe(city.head())
            city_title = f"Students by City in {selected_county['NMCNTY']}, {selected_state['LSTATE']}"
            city_chart = alt.Chart(city, title=alt.Title(city_title, anchor='middle')).mark_bar().encode(
                x=alt.X('TOTAL:Q', title=None),
                y=alt.Y('LCITY:N', title=None, sort='-x'),
                color=alt.Color('LCITY:N', legend=None),
                tooltip=[
                    alt.Tooltip('LCITY:N', title='City'),
                    alt.Tooltip('TOTAL:Q', title='Number of Students')
                ]
            )

            text = city_chart.mark_text(
                align='center',
                baseline='middle',
                dx=10  # Move the text above the bar
            ).encode(
                text='TOTAL:Q'
            )
            c = (city_chart + text)
            st.altair_chart(c, use_container_width=True)
        else:
            pass