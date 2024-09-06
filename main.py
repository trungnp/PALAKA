import altair as alt
import numpy as np
import pandas as pd
import streamlit as st
from vega_datasets import data

st.set_page_config(layout='wide')
overview, experiment, dat = st.tabs(['Overview', 'Experiment', 'Data'])
us_map = alt.topo_feature(data.us_10m.url, 'states')
with overview:
    st.markdown('#### This is how the original dataset was sampled to around 200k rows')
    code = """
    df = pd.read_sas('spm_pu_2022.sas7bdat', encoding='utf-8')
    # Remove error data
    df = df[df['st'] != 99]
    # Count cases in each state
    case_count_by_state = df['st'].value_counts()
    # Normalize to percentage
    case_pct_by_state = case_count_by_state/df.shape[0]
    # Calculate distribution (in number of rows) of each state in a sample of 200k rows, round down
    sample_case_dist_by_state = (case_pct_by_state*200000).astype(int)
    # Get random rows from the original dataset for each state based on the distribution above
    sample = [df[df['st'] == i].sample(j, random_state=0) for i,j in sample_case_dist_by_state.items()]
    # Form the new dataset
    f = pd.concat(sample, ignore_index=True)
    """
    st.code(code, language='python')
    overview_df = pd.read_csv('overview.csv')
    overview_df['original_pct'] = (overview_df['original'] / overview_df['original'].sum() * 100).round(2)
    overview_df['sample_pct'] = (overview_df['sample'] / overview_df['sample'].sum() * 100).round(2)
    overview_df = overview_df.rename(columns={'st': 'id'})

    overview_sel = alt.selection_point(fields=['id'])
    overviews = [
        ['original', 'original_pct', overview_df, '% of Total Cases by State in Original Dataset With Over 3M Rows', 'yelloworangered'],
        ['sample', 'sample_pct', overview_df, '% of Total Cases by State in Sample Dataset With Around 200k Rows', 'yelloworangered']
    ]

    chart = None
    for i in overviews:
        overview_map = alt.Chart(us_map, title=alt.Title(i[3], anchor='middle')).mark_geoshape(
            stroke='black',
            strokeWidth=1
        ).encode(
            color=alt.Color(f'{i[1]}:Q', scale=alt.Scale(scheme=i[4]), legend=alt.Legend(title='%', )),
            opacity=alt.condition(overview_sel, alt.value(1), alt.value(0.2)),
            tooltip=[
                alt.Tooltip('id:O', title='State'),
                alt.Tooltip(f'{i[0]}:Q', title='Count', format=','),
                alt.Tooltip(f'{i[1]}:Q', title='%')
            ]
        ).transform_lookup(
            lookup='id',
            from_=alt.LookupData(i[2], 'id', i[:2])
        ).project(
            type='albersUsa'
        ).add_params(
            overview_sel
        ).properties(width=700, height=700)

        chart = overview_map if chart is None else chart | overview_map

    chart = chart.resolve_scale(color='independent')
    with st.container():
        st.altair_chart(chart, use_container_width=True)


with experiment:
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
        df = pd.read_csv('sample.csv')
        st.session_state['data'] = df

    df = st.session_state['data']
    diff = np.where(df['SPM_Poor'] == df['OFFPoor'], True, False)
    df['Matched'] = diff
    df = df.rename(columns={'st': 'id'})
    us_map = alt.topo_feature(data.us_10m.url, 'states')
    groupby_state = df.groupby(by=['id', 'StateAbbr'], as_index=False)
    off1 = groupby_state['OFFPoor'].sum()
    off0 = groupby_state['OFFPoor'].count()
    off0['OFFPoor'] = off0['OFFPoor'] - off1['OFFPoor']
    survey1 = groupby_state['SPM_Poor'].sum()
    survey0 = groupby_state['SPM_Poor'].count()
    survey0['SPM_Poor'] = survey0['SPM_Poor'] - survey1['SPM_Poor']
    single_value = [
        ['OFFPoor', 'StateAbbr', off1, 'Official Poverty (OFFPoor=1)', 'yelloworangered'],
        ['OFFPoor', 'StateAbbr', off0, 'Official Poverty (OFFPoor=0)', 'teals'],
        ['SPM_Poor', 'StateAbbr', survey1, 'Survey Poverty (SPM_Poor=1)', 'bluegreen'],
        ['SPM_Poor', 'StateAbbr', survey0, 'Survey Poverty (SPM_Poor=0)', 'lighttealblue'],
    ]

    st.markdown("#### Single value of Official Pover Status & Survey Poverty Status")
    with st.container(border=True):
        official_selection = alt.selection_point(fields=['id'])

        chart = None
        for i in single_value:
            map = alt.Chart(us_map, title=alt.Title(i[3], anchor='middle')).mark_geoshape(
                stroke='black',
                strokeWidth=1
            ).encode(
                color=alt.Color(f'{i[0]}:Q', scale=alt.Scale(scheme=i[4]), legend=alt.Legend(title='Case', format='.3s')),
                opacity=alt.condition(official_selection, alt.value(1), alt.value(0.2)),
                tooltip=[
                    alt.Tooltip(f'{i[1]}:N', title='State'),
                    alt.Tooltip(f'{i[0]}:Q', title='Case')
                ]
            ).transform_lookup(
                lookup='id',
                from_=alt.LookupData(i[2], 'id', i[:2])
            ).project(
                type='albersUsa'
            ).add_params(
                official_selection
            ).properties(width=300, height=300)

            chart = map if chart is None else chart | map

        st.altair_chart(chart.resolve_scale(color='independent'), use_container_width=True)

    true_official = df[df['OFFPoor'] == 1]
    false_official = df[df['OFFPoor'] == 0]
    vals = [0, 1]
    cols = ['OFFPoor', 'SPM_Poor']
    dfs = []
    for i in vals:
        off = df[df['OFFPoor'] == i]
        for j in vals:
            dfs.append(off[off['SPM_Poor'] == j].groupby(by=['id', 'StateAbbr'], as_index=False)['SPM_Poor'].count())

    compared_value = [
        ['SPM_Poor', 'StateAbbr', dfs[0], 'True Negative (OFFPoor=0, SPM_Poor=0)', 'yelloworangered'],
        ['SPM_Poor', 'StateAbbr', dfs[1], 'False Negative (OFFPoor=0, SPM_Poor=1)', 'teals'],
        ['SPM_Poor', 'StateAbbr', dfs[2], 'False Positive (OFFPoor=1, SPM_Poor=0)', 'bluegreen'],
        ['SPM_Poor', 'StateAbbr', dfs[3], 'True Positive (OFFPoor=1, SPM_Poor=1)', 'lighttealblue'],
    ]

    st.markdown("#### Match values between Official Pover Status vs. Survey Poverty Status")
    with st.container(border=True):
        official_selection = alt.selection_point(fields=['id'])

        chart = None
        for i in compared_value:
            map = alt.Chart(us_map, title=alt.Title(i[3], anchor='middle')).mark_geoshape(
                stroke='black',
                strokeWidth=1
            ).encode(
                color=alt.Color(f'{i[0]}:Q', scale=alt.Scale(scheme=i[4]), legend=alt.Legend(title='Case', format='.3s')),
                opacity=alt.condition(official_selection, alt.value(1), alt.value(0.2)),
                tooltip=[
                    alt.Tooltip(f'{i[1]}:N', title='State'),
                    alt.Tooltip(f'{i[0]}:Q', title='Case')
                ]
            ).transform_lookup(
                lookup='id',
                from_=alt.LookupData(i[2], 'id', i[:2])
            ).project(
                type='albersUsa'
            ).add_params(
                official_selection
            ).properties(width=300, height=300)

            chart = map if chart is None else chart | map

        st.altair_chart(chart.resolve_scale(color='independent'), use_container_width=True)

with dat:
    df