import calendar

import pandas as pd
from bokeh.layouts import row
from bokeh.models import ColumnDataSource, Select, Slider
from bokeh.palettes import Category20
from bokeh.plotting import curdoc, figure

# Membaca data dari file CSV
data = pd.read_csv('austin_weather.csv')
data['Date'] = pd.to_datetime(data['Date'])

# Mengurutkan bulan berdasarkan urutan kalender
months = list(calendar.month_name)[1:]

# Membuat pilihan unik untuk tahun dan bulan
years = sorted(data['Date'].dt.year.unique().tolist())
months = sorted(months, key=lambda x: list(calendar.month_name).index(x))

# Membuat data source Bokeh dari DataFrame
source = ColumnDataSource(data)

# Membuat plot
plot = figure(x_axis_type="datetime", title="Grafik Seluruh Suhu Rata-rata Harian dalam satuan Fahrenheit di kota Austin dari Tahun 2013-2017", width=1200, height=600)
plot.line('Date', 'TempAvgF', source=source, line_width=2)

# Membuat slider untuk tahun
year_slider = Slider(title="Tahun", start=min(years), end=max(years), value=min(years), step=1)

# Membuat dropdown menu untuk bulan
month_select = Select(title="Bulan", options=months, value=months[0])

# Fungsi untuk memperbarui data yang ditampilkan berdasarkan slider dan dropdown menu
def update_data(attrname, old, new):
    selected_year = year_slider.value
    selected_month = month_select.value

    filtered_data = data[(data['Date'].dt.year == selected_year) & (data['Date'].dt.month_name() == selected_month)]

    if filtered_data.empty:
        # Jika data kosong, menampilkan tulisan "Data tidak tersedia"
        plot.title.text = "Data tidak tersedia"
        source.data = dict()
    else:
        # Jika data tersedia, menampilkan data yang difilter
        plot.title.text = "Grafik Suhu Rata-rata Harian dalam satuan Fahrenheit di kota Austin"
        source.data = dict(ColumnDataSource(filtered_data).data)


# Mengikat fungsi update_data dengan perubahan pada slider dan dropdown menu
year_slider.on_change('value', update_data)
month_select.on_change('value', update_data)

# Menambahkan elemen ke layout
layout = row(year_slider, month_select)
curdoc().add_root(layout)
curdoc().add_root(plot)
