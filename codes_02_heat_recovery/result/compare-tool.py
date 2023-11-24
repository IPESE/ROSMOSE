import json
import pathlib

from plotnine import *
from plotnine.data import mtcars

import pandas as pd
import numpy as np
import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots


def get_json_list():
    jsons = pathlib.Path('.').glob('**/*.json')
    jsons = [str(x) for x in jsons if "venv" not in str(x)]
    jsons = sorted(jsons)
    return jsons


def substring_unit_name(uname):
    name_tab = uname.split("_")
    if len(name_tab) > 4:
        name = ""
        for i in range(3, len(name_tab)):
            name += name_tab[i] + " "
        return name[:-1]
    elif len(name_tab) == 4:
        return name_tab[3]
    else:
        return uname


def display_invcost(data):
    invCosts = data["results"]["Units_Cost"][0]["DefaultInvCost"]
    temp = []
    stacked_bar = []
    for k in invCosts:
        name = substring_unit_name(k)
        temp.append({"unit": name, "cost": invCosts[k]})
        stacked_bar.append(go.Bar(name=name, x=["scenario"], y=[invCosts[k]]))

    invc_df = pd.DataFrame.from_dict(temp)
    invc_dft = invc_df.T
    invc_dft.columns = invc_dft.iloc[0]
    invc_dft = invc_dft.drop(invc_dft.index[0])
    fig2 = go.Figure(data=stacked_bar)
    fig2.update_layout(barmode='stack')
    fig = go.Figure(go.Bar(x=invc_df["unit"], y=invc_df["cost"]))
    st.plotly_chart(fig2)
    st.plotly_chart(fig)
    st.write(invc_df)


def display_opcost(data):
    opCosts = data["results"]["Units_Cost"][0]["DefaultOpCost"]
    temp = []
    stacked_bar = []
    for k in opCosts:
        name = substring_unit_name(k)
        temp.append({"unit": name, "cost": opCosts[k]})
        stacked_bar.append(go.Bar(name=name, x=["scenario"], y=[opCosts[k]]))

    opc_df = pd.DataFrame.from_dict(temp)
    opc_dft = opc_df.T
    opc_dft.columns = opc_dft.iloc[0]
    opc_dft = opc_dft.drop(opc_dft.index[0])
    fig2 = go.Figure(data=stacked_bar)
    fig2.update_layout(barmode='stack')
    fig = go.Figure(go.Bar(x=opc_df["unit"], y=opc_df["cost"]))
    st.plotly_chart(fig2)
    st.plotly_chart(fig)
    st.write(opc_df)


def display_totcost(data):
    opCosts = [data["results"]["Units_Cost"][0]["DefaultOpCost"]]
    invCosts = [data["results"]["Units_Cost"][0]["DefaultInvCost"]]
    opCdf = pd.DataFrame.from_dict(opCosts)
    invCdf = pd.DataFrame.from_dict(invCosts)
    totCdf = opCdf + invCdf
    totCosts = totCdf.to_dict()
    temp = []
    stacked_bar = []
    for k in totCosts:
        name = substring_unit_name(k)
        temp.append({"unit": name, "cost": totCosts[k][0]})
        stacked_bar.append(go.Bar(name=name, x=["scenario"], y=[totCosts[k][0]]))

    totCdf = opc_df = pd.DataFrame.from_dict(temp)
    totc_dft = totCdf.T
    totc_dft.columns = totc_dft.iloc[0]
    totc_dft = totc_dft.drop(totc_dft.index[0])
    fig2 = go.Figure(data=stacked_bar)
    fig2.update_layout(barmode='stack')
    fig = go.Figure(go.Bar(x=totCdf["unit"], y=totCdf["cost"]))
    st.plotly_chart(fig2)
    st.plotly_chart(fig)
    st.write(totCdf)


def display_unit_used_t(data):
    st.write("unit used t")
    uut = data["results"]["Units_Use_t"][0]
    uut_df = pd.DataFrame.from_dict(uut).T
    uut_df.index.name = "unitname"
    uut_df.reset_index(inplace=True)
    uut_df["unitname"] = uut_df["unitname"].apply(substring_unit_name)
    y = uut_df["unitname"].tolist()
    x = []
    for col in uut_df.columns:
        time = 1
        if col != "unitname":
            x.append("Time " + str(time))
            time += 1
    sub_df = uut_df.loc[:, uut_df.columns != "unitname"]
    z = sub_df.values
    fig = go.Figure(data=go.Heatmap(
        z=z,
        x=x,
        y=y,
        hoverongaps=False,
        colorscale=[[0, "red"], [1, "rgb(6,200,32)"]],
        colorbar=dict(
            tick0=0,
            dtick=1
        )
    ))
    st.plotly_chart(fig)
    st.write(uut_df)


def display_unit_size_percentage(data):
    fmax = data["evaluated"][0][0]["fmaxUnits"]
    fmax_df = pd.DataFrame.from_dict(fmax)
    fmax_df.columns = ["unitname", "fmaxValue"]
    units_mult = data["results"]["Units_Mult"]
    units_mult_df = pd.DataFrame.from_dict(units_mult).T
    units_mult_df.index.name = "unitname"
    units_mult_df.reset_index(inplace=True)
    data_df = pd.merge(fmax_df, units_mult_df, on=["unitname"])
    data_df.columns = ["unitname", "fmaxValue", "fmultValue"]
    data_df["percentage %"] = (data_df["fmultValue"] * 100) / data_df["fmaxValue"]
    data_df["unitname"] = data_df["unitname"].apply(substring_unit_name)
    fig = go.Figure([go.Bar(x=data_df["unitname"], y=data_df["percentage %"])])
    st.plotly_chart(fig)
    st.write(data_df)


def display_unit_mult(data):
    st.write("unit mult")
    units_mult = data["results"]["Units_Mult"]
    units_mult_df = pd.DataFrame.from_dict(units_mult).T
    units_mult_df.index.name = "unitname"
    units_mult_df.reset_index(inplace=True)
    units_mult_df.columns = ["unitname", "value"]
    units_mult_df["unitname"] = units_mult_df["unitname"].apply(substring_unit_name)
    st.write(units_mult_df)


def display_unit_mult_t(data):
    st.write("unit mult t")
    units_mult = data["results"]["Units_Mult_t"]
    units_mult_df = pd.DataFrame.from_dict(units_mult).T
    units_mult_df.index.name = "unitname"
    units_mult_df.reset_index(inplace=True)
    x = ["unitname"]
    for col in units_mult_df.columns:
        time = 1
        if col != "unitname":
            x.append("Time " + str(time))
            time += 1
    units_mult_df.columns = x
    units_mult_df["unitname"] = units_mult_df["unitname"].apply(substring_unit_name)
    st.write(units_mult_df)


def print_result_main_values(data):
    n_timesteps = data["evaluated"][0][0]["time"]
    n_scenarios = 1
    st.write("**Objective function:** " + data["results"]["solvers"][0]["hc"]["_objname"])
    st.write("**OPEX:** " + str(data["results"]["KPIs"]["opex"][0]))
    st.write("**CAPEX:** " + str(data["results"]["KPIs"]["capex"][0]))
    st.write("**Impact:** " + str(data["results"]["KPIs"]["impact"][0]))
    st.write("**Totalcost:** " + str(data["results"]["KPIs"]["totalcost"][0]))
    st.write("**Operating cost with impact:** " + str(data["results"]["KPIs"]["opcostwithimpact"][0]))
    st.write("**Totalcost with impact:** " + str(data["results"]["KPIs"]["totalcostwithimpact"][0]))
    st.write("**Total investment cost:** " + str(data["results"]["KPIs"]["totalinvestmentcost"][0]))
    st.write("**Number of time steps:** " + str(n_timesteps))


def display_ts(data):
    heat = data["evaluated"][0][0]["streams"]
    heat_df = pd.DataFrame.from_dict(heat)
    heat_df["Tin_corr"] = heat_df["Tin_corr"] - 273.15
    heat_df["Tout_corr"] = heat_df["Tout_corr"] - 273.15
    heat_df["name"] = heat_df["name"].apply(substring_unit_name)
    heat_df['tin'] = np.where(heat_df['hout'] > heat_df['hin'], heat_df['Tin_corr'] - heat_df['dt'],
                              heat_df['Tin_corr'] + heat_df['dt'])
    heat_df['color'] = np.where(heat_df['hout'] > heat_df['hin'], "red", "blue")
    heat_df['base'] = np.where(heat_df['hout'] > heat_df['hin'], heat_df['Tin_corr'], heat_df['Tout_corr'])
    heat_df['diff'] = np.where(heat_df['hout'] > heat_df['hin'], heat_df['Tout_corr'], heat_df['Tin_corr'])
    heat_df['tout'] = np.where(heat_df['hout'] > heat_df['hin'], heat_df['Tout_corr'] - heat_df['dt'],
                              heat_df['Tout_corr'] + heat_df['dt'])

    p = ggplot(heat_df) + \
        geom_segment(aes(x=heat_df["name"], xend=heat_df["name"], y=heat_df["base"], yend=heat_df["diff"]),
                     color=heat_df["color"], size=3, alpha=0.5) + \
        geom_point(aes(x=heat_df["name"], y=heat_df["tin"]), color=heat_df["color"]) + \
        geom_point(aes(x=heat_df["name"], y=heat_df["tout"]), color=heat_df["color"]) + \
        coord_flip() + \
        ggtitle("Heat exchange for Time") + \
        ylab("Temperature [°C]") + \
        xlab("") + \
        theme_minimal()
    st.pyplot(ggplot.draw(p))
    display_heat_at_time(data)


def display_heat_at_time(data):
    unit_h_mult = data["results"]["streamQ"][0]
    unit_h_mult_df = pd.DataFrame.from_dict(unit_h_mult).T
    unit_h_mult_df.index.name = "name"
    unit_h_mult_df.reset_index(inplace=True)

    heat = data["evaluated"][0][0]["streams"]
    heat_df = pd.DataFrame.from_dict(heat)
    names = unit_h_mult_df["name"].values.tolist()
    to_update = []
    for name in names:
        hin = heat_df.loc[heat_df["name"] == name]["hin"].tolist()[0]
        hout = heat_df.loc[heat_df["name"] == name]["hout"].tolist()[0]
        if hout < hin:
            to_update.append(name)
    other_cols = list(unit_h_mult_df.columns.difference(["name"]))
    for index, row in unit_h_mult_df.iterrows():
        if row["name"] in to_update:
            unit_h_mult_df.loc[index, other_cols] = row[other_cols] * (-1)

    unit_h_mult_df["name"] = unit_h_mult_df["name"].apply(substring_unit_name)

    y = unit_h_mult_df["name"].tolist()
    x = []
    for col in unit_h_mult_df.columns:
        time = 1
        if col != "name":
            x.append("Time " + str(time))
            time += 1
    sub_df = unit_h_mult_df.loc[:, unit_h_mult_df.columns != "name"]
    z = sub_df.values
    fig = go.Figure(data=go.Heatmap(
        z=z,
        x=x,
        y=y,
        hoverongaps=False,
        colorscale=[[0, "red"], [1, "rgb(6,200,32)"]],
        colorbar=dict(title="HEAT [kW]")
    ))
    st.plotly_chart(fig)

    st.write(unit_h_mult_df)


def display_carnot(data):
    graph = data["results"]["graph"][0][0]
    carnot_base_df = None
    carnot_utilities_df = None
    for g in graph:
        if g["plot_type"] == "carnot.utilities":
            for c in g["data"]:
                if c["title"] == "base":
                    carnot_base_df = pd.DataFrame.from_dict(c["curve"])
                elif c["title"] == "utilities":
                    carnot_utilities_df = pd.DataFrame.from_dict(c["curve"])
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=carnot_base_df["Q"], y=carnot_base_df["T"], mode="lines+markers", name="base",
                             line=dict(color="blue"), marker=dict(color="blue")))
    fig.add_trace(go.Scatter(x=carnot_utilities_df["Q"], y=carnot_utilities_df["T"], mode="lines+markers",
                             name="utilities", line=dict(color="red"), marker=dict(color="red")))
    fig.update_layout(title='Carnot',
                      xaxis_title='Heat load [kW]',
                      yaxis_title='Carnot factor 1-To/T [-]')
    st.plotly_chart(fig)
    st.write("### base")
    st.write(carnot_base_df)
    st.write("### utilities")
    st.write(carnot_utilities_df)


def display_cc(data):
    graph = data["results"]["graph"][0][0]
    hcc_df = None
    ccc_df = None
    for g in graph:
        if g["plot_type"] == "cc":
            for c in g["data"]:
                if c["title"] == "Hot streams":
                    hcc_df = pd.DataFrame.from_dict(c["curve"])
                elif c["title"] == "Cold streams":
                    ccc_df = pd.DataFrame.from_dict(c["curve"])
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=hcc_df["Q"], y=hcc_df["T"], mode="lines+markers", name="Hot streams",
                             line=dict(color="red"), marker=dict(color="red")))
    fig.add_trace(go.Scatter(x=ccc_df["Q"], y=ccc_df["T"], mode="lines+markers", name="Cold streams",
                             line=dict(color="blue"), marker=dict(color="blue")))
    fig.update_layout(title='Composite Curve',
                      xaxis_title='Quantity',
                      yaxis_title='Temperature (degrees C)')
    st.plotly_chart(fig)


def display_icc(data):
    graph = data["results"]["graph"][0][0]
    hcc_df = None
    ccc_df = None
    for g in graph:
        if g["plot_type"] == "icc.utilities":
            for c in g["data"]:
                if c["title"] == "base":
                    base_df = pd.DataFrame.from_dict(c["curve"])
                elif c["title"] == "utilities":
                    utilities_df = pd.DataFrame.from_dict(c["curve"])
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(go.Scatter(x=base_df["Q"], y=base_df["T"]-273.15, mode="lines+markers", name="Base streams",
                             line=dict(color="red"), marker=dict(color="red")))
    fig.add_trace(go.Scatter(x=utilities_df["Q"], y=utilities_df["T"]-273.15, mode="lines+markers", name="Utilities streams",
                             line=dict(color="blue"), marker=dict(color="blue")), secondary_y=False)
    fig.add_trace(go.Scatter(x=utilities_df["Q"], y=1-298.15/utilities_df["T"], showlegend=False,
                             line=dict(color="blue"), marker=dict(color="blue")), secondary_y=True)
    fig.update_layout(title='Integrated Composite Curve')
    fig.update_xaxes(title='Heat load [kW]')
    fig.update_yaxes(title='Corrected Temperatures [°C]', secondary_y=False)
    fig.update_yaxes(title='Carnot factor 1-To/T [-]', secondary_y=True)
    st.plotly_chart(fig)


def display_gcc(data):
    graph = data["results"]["graph"][0][0]
    hcc_df = None
    ccc_df = None
    for g in graph:
        if g["plot_type"] == "gcc":
            data = g["data"][0]["curve"]
            df = pd.DataFrame.from_dict(data)
    fig = go.Figure()
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(go.Scatter(x=df["Q"], y=df["T"]-273.15, mode="lines+markers", name="streams",
                             line=dict(color="blue"), marker=dict(color="blue")), secondary_y=False)
    fig.add_trace(go.Scatter(x=df["Q"], y=1-298.15/df["T"], mode="lines+markers",
                             line=dict(color="blue"), marker=dict(color="blue")), secondary_y=True)

    fig.update_layout(title='Grand Composite Curve')
    fig.update_xaxes(title='Heat load [kW]')
    fig.update_yaxes(title='Corrected Temperatures [°C]', secondary_y=False)
    fig.update_yaxes(title='Carnot factor 1-To/T [-]', secondary_y=True)
    st.plotly_chart(fig)


with open('sty.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)


st.write(f"""
    <img src="https://ipese-internal.epfl.ch/osmose/images/osmose-logo-white.png" width="300"/>
    """, unsafe_allow_html=True)

st.markdown("---")

runs = get_json_list()

left_col, right_col = st.columns(2)

with left_col:
    first_run = st.selectbox("Compare situation in", runs)
    with st.spinner('Collecting data...'):
        with open(first_run, "r") as f:
            data1 = f.read()
        data1 = json.loads(data1)
        if "evaluated" in data1 and "model" in data1 and "results" in data1 and "clusters" in data1:
            print_result_main_values(data1)
        else:
            st.write("Incorrect Osmose run input")
with right_col:
    second_run = st.selectbox("To", runs)
    with st.spinner('Collecting data...'):
        with open(second_run, "r") as f:
            data2 = f.read()
        data2 = json.loads(data2)
        if "evaluated" in data2 and "model" in data2 and "results" in data2 and "clusters" in data2:
            print_result_main_values(data2)
        else:
            st.write("Incorrect Osmose run input")

main = st.container()
with main:
    with st.expander("Costs breakdown"):
        invcost, opcost, totcost = st.tabs(["Investment Costs", "Operating Costs", "Total Costs"])
        with invcost:
            invc_left, invc_right = st.columns(2)
            with invc_left:
                display_invcost(data1)
            with invc_right:
                display_invcost(data2)
        with opcost:
            opc_left, opc_right = st.columns(2)
            with opc_left:
                display_opcost(data1)
            with opc_right:
                display_opcost(data2)
        with totcost:
            tc_left, tc_right = st.columns(2)
            with tc_left:
                display_totcost(data1)
            with tc_right:
                display_totcost(data2)

    with st.expander("Units resume"):
        st.header("Units resume")
        uut, usizeperc, umult, umultt = st.tabs(["Units used at time t", "Units percentage size %", "Units Multiplication (size)", "Units Multiplication (size) at time t"])
        with uut:
            st.write("## Units used T")
            uut_left, uut_right = st.columns(2)
            with uut_left:
                display_unit_used_t(data1)
            with uut_right:
                display_unit_used_t(data2)
        with usizeperc:
            st.write("## Units size percentage in %")
            usp_left, usp_right = st.columns(2)
            with usp_left:
                display_unit_size_percentage(data1)
            with usp_right:
                display_unit_size_percentage(data2)
        with umult:
            st.write("## Units mult")
            umult_left, umult_right = st.columns(2)
            with umult_left:
                display_unit_mult(data1)
            with umult_right:
                display_unit_mult(data2)
        with umultt:
            st.write("## Units mult T")
            umultt_left, umultt_right = st.columns(2)
            with umultt_left:
                display_unit_mult_t(data1)
            with umultt_right:
                display_unit_mult_t(data2)

    with st.expander("Thermal Streams"):
        ts, cc, gcc, icc, carnot = st.tabs(["Temperature Streams", "CC", "GCC", "ICC", "carnot"])
        with ts:
            st.write("## Temperature streams")
            ts_left, ts_right = st.columns(2)
            with ts_left:
                display_ts(data1)
            with ts_right:
                display_ts(data2)
        with cc:
            st.write("## CC")
            cc_left, cc_right = st.columns(2)
            with cc_left:
                display_cc(data1)
            with cc_right:
                display_cc(data2)
        with gcc:
            st.write("## GCC")
            gcc_left, gcc_right = st.columns(2)
            with gcc_left:
                display_gcc(data1)
            with gcc_right:
                display_gcc(data2)
        with icc:
            st.write("## ICC")
            icc_left, icc_right = st.columns(2)
            with icc_left:
                display_icc(data1)
            with icc_right:
                display_icc(data2)
        with carnot:
            st.write("## Carnot")
            carnot_left, carnot_right = st.columns(2)
            with carnot_left:
                display_carnot(data1)
            with carnot_right:
                display_carnot(data2)
    st.markdown('---')
