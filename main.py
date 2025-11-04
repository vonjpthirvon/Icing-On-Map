import streamlit as st
import pandas as pd
from datetime import datetime, time, timedelta, date
from dateutil.relativedelta import relativedelta
from data_fetchers import fetch_icedata
from plotters import plot_icegraph, extract_station_info, plot_icing_map
from streamlit_folium import st_folium
from io import BytesIO
import matplotlib.pyplot as plt

def main():
    st.set_page_config(page_title="Icing Map And Graph", layout="centered")
    st.title("Icing On Map")

    for key in ["show_map", "station_data", "figure_data", "selected_station", "shown_graphs"]:
        if key not in st.session_state:
            st.session_state[key] = [] if "data" in key or key == "shown_graphs" else None

    places = {
        "Vantaa": 100968, "Turku": 101065, "Maarianhamina": 100907,
        "Pori": 101044, "Tampere": 101118, "Halli": 101315, "Tikkakoski": 137208,
        "Seinäjoki": 137188, "Vaasa": 101462, "Kruunupyy": 101662, "Siilinjärvi": 101570,
        "Joensuu": 101608, "Utti": 101191, "Lappeenranta": 101237, "Savonlinna": 101430,
        "Mikkeli": 855522, "Kajaani": 101725, "Oulu": 101786, "Kemi": 101840, "Kuusamo": 101886,
        "Rovaniemi": 137190, "Ivalo": 102033, "Kittilä": 101986
    }

    places = dict(sorted(places.items()))
    place_options = ["All Stations"] + list(places.keys())
    selected_places = st.multiselect("Choose stations to plot:", place_options)

    if "All Stations" in selected_places:
        st.info("All stations selected.")
        selected_places = list(places.keys())

    today = date.today()
    tomorrow = today + timedelta(days=1)

    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Start Date:", value=today)
        end_date = st.date_input("End Date:", value=tomorrow)
    with col2:
        start_time = st.time_input("Start Time:", value=time(0, 0))
        end_time = st.time_input("End Time:", value=time(0, 0))

    start_datetime = datetime.combine(start_date, start_time)
    end_datetime = datetime.combine(end_date, end_time)

    if start_datetime >= end_datetime:
        st.error("Start Time must be before End Time.")
        return
    if end_datetime > start_datetime + relativedelta(months=1):
        st.error("Too long period (max 1 month).")
        return

    starttime = start_datetime.strftime("%Y%m%dT%H%M")
    endtime = end_datetime.strftime("%Y%m%dT%H%M")

    if st.button("Show Map"):
        st.session_state.show_map = True
        st.session_state.station_data = []
        st.session_state.figure_data = []
        st.session_state.df_data = []
        st.session_state.shown_graphs = []

        with st.spinner("Fetching data..."):
            for i, place in enumerate(selected_places):
                FMISID = places[place]
                sensor_id = None
                # print(f"{i}, {repr(place)}, {FMISID}, {sensor_id}")
                # if place in ["Vantaa"]:
                if place.strip().lower() == "vantaa":
                    sensor_id = 37
                    df = fetch_icedata(FMISID, starttime, endtime, place, sensor_id)
                else:
                    df = fetch_icedata(FMISID, starttime, endtime, place)
                print(f"{i}, {place}, {FMISID}, {sensor_id}")

                if df is None or df.empty:
                    st.warning(f"No data for {place}")
                    continue

                station = extract_station_info(df)

                # fig = plot_icegraph(df, place, FMISID, starttime, endtime)

                st.session_state.station_data.append(station)
                st.session_state.df_data.append((df, place, FMISID))
                # st.session_state.figure_data.append(fig)

    if st.session_state.show_map and st.session_state.station_data:
        with st.spinner("Plotting map..."):
            m = plot_icing_map(st.session_state.station_data)
            st_folium(m, width=700, height=500)

    st.title("Icing Graph")
    station_names = sorted([station['name'] for station in st.session_state.station_data])
    selected_station = st.selectbox("Select station to show graph:", station_names)

    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("Show Graph"):
            if selected_station not in st.session_state.shown_graphs:
                st.session_state.shown_graphs.append(selected_station)
    with col2:
        if st.button("Reset Graphs"):
            st.session_state.shown_graphs = []

    with st.spinner("Plotting graph..."):
        for station_name in st.session_state.shown_graphs:
            idx = next((i for i, s in enumerate(st.session_state.station_data)
                        if s["name"] == station_name), None)
            if idx is not None:
                df, place, FMISID = st.session_state.df_data[idx]
                fig = plot_icegraph(df, place, FMISID, starttime, endtime)
                # fig = st.session_state.figure_data[idx]
                buf = BytesIO()
                fig.savefig(buf, format="png")
                buf.seek(0)
                st.image(buf, caption=f"Icing Station: {station_name}", width='stretch')

if __name__ == "__main__":
    main()
    