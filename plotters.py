"""
plotters.py

Contains functions for extracting station info, generating matplotlib graphs,
and plotting icing data on a folium map. Also includes UI logic for selecting
a station and displaying its graph below the map.
"""

import folium
from typing import TypedDict
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import streamlit as st
import pandas as pd
import cmocean
import matplotlib.colors as mcolors

class StationInfo(TypedDict):
    name: str
    lat: float
    lon: float
    value: float


def get_deep_color(value, max_value):
    # Clampataan arvo välille [0.0, clamp_max]
    clamp_max = max_value
    clamped_value = min(max(value, 0.0), clamp_max)

    # Normalisoidaan arvo välille [0, 1]
    normalized_value = clamped_value / clamp_max

    # Haetaan deep-paletti cmoceanista
    # cmap = cmocean.cm.deep
    cmap = cmocean.cm.ice
    # cmap = cmocean.cm.matter

    # Haetaan RGBA-väri
    rgba = cmap(normalized_value)

    # Muutetaan HEX-muotoon
    hex_color = mcolors.to_hex(rgba)

    return hex_color


def extract_station_info(df) -> StationInfo:
    """
    Extracts station metadata and cumulative icing value from a DataFrame.

    Args:
        df (pd.DataFrame): DataFrame containing station data.

    Returns:
        StationInfo: Dictionary with name, lat, lon, and icing value.
    """
    return {
        "name": df["stationname"].iloc[0],
        "lat": float(df["lat"].iloc[0]),
        "lon": float(df["lon"].iloc[0]),
        "value": float(df["cumul_mm_filtered"].iloc[-1])
    }

def plot_icing_map(station_data: list[StationInfo]) -> folium.Map:
    """
    Creates a folium map with colored markers for each station.
    When a marker is clicked, the station name is shown in popup.

    Args:
        station_data (list): List of station dictionaries.

    Returns:
        folium.Map: Map object with station markers.
    """
    m = folium.Map(location=[64.5, 23], zoom_start=5)
    max_value = max(station['value'] for station in station_data)

    for station in station_data:
        value = station['value']
        rounded_value = round(value, 1)
        color = get_deep_color(rounded_value, max_value)

        # if rounded_value <= 0.0:
        #     # color = 'gray'
        #     color = '#E9FFFF'
        # elif rounded_value <= 0.2:
        #     # color = 'green'
        #     color = '#93B3E7'
        # elif rounded_value <= 0.8:
        #     # color = 'orange'
        #     color = '#3979B7'
        # else:
        #     # color = 'red'
        #     color = '#1D2E68'

       # popuphtml = folium.Html(f"<b>{station['name']}</b>", script=True)
        popup_html = folium.Html(f"<b>{station['name']}</b><br>{rounded_value} mm", script=True)
        popup = folium.Popup(popup_html, max_width=250)

        folium.CircleMarker(
            location=[station['lat'], station['lon']],
            radius=8,
            popup=popup,
            # tooltip="Click to select",
            tooltip=f"{station['name']}: {rounded_value} mm",
            color=color,
            fill=True,
            fill_color=color
        ).add_to(m)

    return m

def create_station_selector():
    """
    Displays a dropdown to select a station from session_state.station_data.
    Stores the selected station name in session_state.selected_station.
    """
    station_names = [station['name'] for station in st.session_state.station_data]
    selected = st.selectbox("Valitse asema nähdäksesi kuva:", station_names)
    st.session_state.selected_station = selected

def plot_icegraph(
    df: pd.DataFrame,
    place: str,
    fmisid: int,
    starttime: str,
    endtime: str,
    sensor_id: int = None
) -> plt.Figure:
    """
    Creates a multi-panel matplotlib figure visualizing icing-related variables over time.

    Parameters:
        df (pd.DataFrame): DataFrame containing processed icing data.
        place (str): Name of the weather station.
        fmisid (int): FMI station ID.
        starttime (str): Start time in format YYYYMMDDTHHMM.
        endtime (str): End time in format YYYYMMDDTHHMM.
        sensor_id (int, optional): Sensor ID if multiple sensors are used.

    Returns:
        plt.Figure: A matplotlib figure object with 5 subplots showing:
            - Ice accumulation
            - Raw and filtered frequency (fzfreq)
            - Instantaneous ice accretion
            - Net frequency change (NFC)
            - Filtered NFC
    """
    if sensor_id is not None:
        fzfreq_label = f"fzfreq#{sensor_id}"
    else:
        fzfreq_label = "fzfreq"

    fig, (ax1, ax2, ax3, ax4, ax5) = plt.subplots(5, 1, figsize=(16, 16), sharex=True)

    ax2.plot(df.index, df["fzfreq"], label=f"{fzfreq_label}", linestyle=':', color='blue')
    ax2.plot(df.index, df["moving_minimun_15minutes"], label="fz10min", linestyle=':', color='red')

    ax4.plot(df.index, df["NFC"], label="NFC", linestyle='--', color='red')
    ax5.plot(df.index, df["NFC_filtered"], label="NFC_filtered", linestyle=':', color='red')

    ax3.plot(df.index, df["mm_instant"], label="mm inst", linestyle='--', color='blue')
    ax3.plot(df.index, df["mm_instant_filtered"], label="mm instant filtered", linestyle=':', color='red')

    ax1.plot(df.index, df["cumul_mm_filtered"], label="cumul mm filtered", linestyle='--', color='red')
    ax1.plot(df.index, df["cumul_mm"], label="cumul mm", linestyle='-.', color='green')

    axes = [ax1, ax2, ax3, ax4, ax5]
    for ax in axes:
        ax.set_xlim(pd.Timestamp(starttime), pd.Timestamp(endtime))
        ax.xaxis.set_major_locator(mdates.HourLocator(byhour=range(0, 24, 3)))
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
        ax.xaxis.set_minor_locator(mdates.HourLocator(interval=1))
        ax.grid(which='major', linestyle='-', linewidth=0.8, color='gray')
        ax.grid(which='minor', linestyle='--', linewidth=0.5, color='lightgray')
        ax.legend()

    ax1.set_ylabel("ice accumulation/mm")
    ax1.set_title("Ice Accumulation")

    ax2.set_ylabel("FZFREQ/Hz")
    ax2.set_title("FZFREQ raw/min(15min) filtered")

    ax3.set_ylabel("ice intensity/(mm/1min)")
    ax3.set_title("Instantaneous ice accretion")

    ax4.set_ylabel("NFC/dHz")
    ax4.set_title("Net Frequency Change")

    ax5.set_ylabel("NFC_new/dHz")
    ax5.set_title("Net Frequency Change Filtered")

    plt.xlabel("Kellonaika")
    title = f"{place}#{sensor_id}: {fmisid}" if sensor_id else f"{place}: {fmisid}"
    plt.suptitle(f"{title}: {starttime}-{endtime} UTC")
    plt.tight_layout(rect=[0, 0, 1, 0.98])

    return fig