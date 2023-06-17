import calendar
import pandas as pd
import streamlit as st
from bokeh.models import ColumnDataSource, Select, Slider
from bokeh.palettes import Category20
from bokeh.plotting import figure


def load_data():
    # Membaca data dari file CSV
    data = pd.read_csv('austin_weather.csv')
    data['Date'] = pd.to_datetime(data['Date'])
    return data


def filter_data(data, selected_year, selected_month):
    filtered_data = data[
        (data['Date'].dt.year == selected_year) & (data['Date'].dt.month_name() == selected_month)
    ]
    return filtered_data


def main():
    # Load data
    data = load_data()

    # Mengurutkan bulan berdasarkan urutan kalender
    months = list(calendar.month_name)[1:]

    # Membuat pilihan unik untuk tahun dan bulan
    years = sorted(data['Date'].dt.year.unique().tolist())
    months = sorted(months, key=lambda x: list(calendar.month_name).index(x))

    # Membuat plot
    plot = figure(x_axis_type="datetime", title="Grafik Seluruh Suhu Rata-rata Harian dalam satuan Fahrenheit di kota Austin dari Tahun 2013-2017", width=1200, height=600)

    # Menampilkan plot kosong
    plot.line([], [], line_width=2)

    # Membuat slider untuk tahun
    selected_year = st.sidebar.slider("Tahun", min_value=min(years), max_value=max(years), value=min(years), step=1)

    # Membuat dropdown menu untuk bulan
    selected_month = st.sidebar.selectbox("Bulan", months, index=0)

    # Fungsi untuk memperbarui data yang ditampilkan berdasarkan slider dan dropdown menu
    filtered_data = filter_data(data, selected_year, selected_month)

    if filtered_data.empty:
        # Jika data kosong, menampilkan tulisan "Data tidak tersedia"
        plot.title.text = "Data tidak tersedia"
    else:
        # Jika data tersedia, menampilkan data yang difilter
        source = ColumnDataSource(filtered_data)
        plot.line('Date', 'TempAvgF', source=source, line_width=2)
        plot.title.text = "Grafik Suhu Rata-rata Harian dalam satuan Fahrenheit di kota Austin"

    # Menampilkan plot menggunakan Streamlit
    st.bokeh_chart(plot)


if __name__ == "__main__":
    main()
