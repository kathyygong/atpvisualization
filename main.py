from bokeh.plotting import figure, show
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from bokeh.models import Slope
from bokeh.models import Div, RangeSlider, Spinner
from bokeh.layouts import layout

atp_df = pd.read_csv('data.csv')
atp_df.head()

atp_hard = atp_df.loc[atp_df['surface'] == 'Hard']
atp_grass = atp_df.loc[atp_df['surface'] == 'Grass']
atp_clay = atp_df.loc[atp_df['surface'] == 'Clay']

# hard Court
atp_hard2 = atp_hard.dropna(subset=['winner_ht', 'w_ace'])
x=atp_hard2['winner_ht']
y=atp_hard2['w_ace']

# grass Court
atp_grass2 = atp_grass.dropna(subset=['winner_ht', 'w_ace'])
x2=atp_grass2['winner_ht']
y2=atp_grass2['w_ace']

# clay Court
atp_clay2 = atp_clay.dropna(subset=['winner_ht', 'w_ace'])
x3=atp_clay2['winner_ht']
y3=atp_clay2['w_ace']

# make and fit a linear regression model
model = LinearRegression().fit(x.values.reshape(-1, 1), y)
model2 = LinearRegression().fit(x2.values.reshape(-1, 1), y2)
model3 = LinearRegression().fit(x3.values.reshape(-1, 1), y3)
# x values need to be in a two-dimensional array, so use .reshape(-1, 1)

# find the slope and intercept from the model
slope = model.coef_[0] # Takes the first element of the array
intercept = model.intercept_
slope2 = model2.coef_[0] # Takes the first element of the array
intercept2 = model2.intercept_
slope3 = model3.coef_[0] # Takes the first element of the array
intercept3 = model3.intercept_

# make the regression line
regression_line = Slope(gradient=slope, y_intercept=intercept, line_color="blue")
regression_line2 = Slope(gradient=slope2, y_intercept=intercept2, line_color="green")
regression_line3 = Slope(gradient=slope3, y_intercept=intercept3, line_color="red")

# plot the data and regression line
fig=figure(title="Aces by Height", x_axis_label="Height", y_axis_label="Aces", x_range=(168, 212))
fig.circle(x, y, color="blue", legend_label="Hard")
fig.add_layout(regression_line)
fig.circle(x2, y2, color="green", legend_label="Grass")
fig.add_layout(regression_line2)
fig.circle(x3, y3, color="red", legend_label="Clay")
fig.add_layout(regression_line3)

# add a title to your legend
fig.legend.title = "Surface"

# change appearance of legend text
fig.legend.label_text_font = "times"
fig.legend.label_text_color = "black"

# change border and background of legend
fig.legend.border_line_width = 2
fig.legend.border_line_color = "darkgray"
fig.legend.border_line_alpha = 0.8
fig.legend.background_fill_color = "silver"
fig.legend.background_fill_alpha = 0.2

# change headline text
fig.title.text = "Aces by Height Across Surfaces"

# style the headline
fig.title.text_font_size = "20px"
fig.title.align = "center"
fig.title.text_color = "black"
fig.title.text_font = "times"

# change background fill color
fig.background_fill_color = (245, 245, 245)

# create range slider
range_slider = RangeSlider(
    title="Adjust x-axis range", # a title to display above the slider
    start=150,  # set the minimum value for the slider
    end=230,  # set the maximum value for the slider
    step=1,  # increments for the slider
    value=(fig.x_range.start, fig.x_range.end),  # initial values for slider
    )
range_slider.js_link("value", fig.x_range, "start", attr_selector=0)
range_slider.js_link("value", fig.x_range, "end", attr_selector=1)

# show results
layout = layout(
    [
        [range_slider],
        [fig],
    ]
)
show(layout)
#show(fig)