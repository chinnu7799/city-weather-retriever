import dash
from dash import html, dcc
from dash.dependencies import Input, Output, State

import requests
import pandas as pd

from config import API_KEY

# =========================================
# DASH APP
# =========================================

app = dash.Dash(__name__)

server = app.server

# =========================================
# DEFAULT BACKGROUND
# =========================================

DEFAULT_BACKGROUND = (
    "https://images.unsplash.com/"
    "photo-1506744038136-46273834b3fb"
)

# =========================================
# APP LAYOUT
# =========================================

app.layout = html.Div(

    id="main-div",

    style={

        "backgroundImage": f"url('{DEFAULT_BACKGROUND}')",

        "backgroundSize": "cover",

        "backgroundPosition": "center",

        "minHeight": "100vh",

        "padding": "40px",

        "transition": "0.5s"
    },

    children=[

        # =========================================
        # MOVING CLOUDS
        # =========================================

        html.Div(className="cloud cloud1"),
        html.Div(className="cloud cloud2"),
        html.Div(className="cloud cloud3"),

        # =========================================
        # TITLE
        # =========================================

        html.H1(

            "☁ Live Weather Dashboard",

            style={

                "textAlign": "center",

                "color": "white",

                "fontSize": "65px",

                "fontWeight": "bold",

                "textShadow": "2px 2px 20px rgba(0,0,0,0.5)"
            }
        ),

        html.Br(),
        html.Br(),
        html.Br(),

        # =========================================
        # SEARCH SECTION
        # =========================================

        html.Div(

            style={
                "textAlign": "center"
            },

            children=[

                # =========================================
                # BIG INPUT BOX
                # =========================================

                dcc.Input(

                    id="city-input",

                    type="text",

                    placeholder="🔍 Enter City Name...",

                    style={

                        # SIZE
                        "width": "700px",

                        "height": "75px",

                        # SPACING
                        "paddingLeft": "30px",

                        "paddingRight": "30px",

                        # TEXT
                        "fontSize": "28px",

                        "fontWeight": "600",

                        "letterSpacing": "1px",

                        "color": "black",

                        # DESIGN
                        "background":
                        "rgba(255,255,255,0.95)",

                        "border":
                        "3px solid rgba(255,255,255,0.4)",

                        "borderRadius": "60px",

                        # EFFECTS
                        "outline": "none",

                        "boxShadow":
                        "0 10px 40px rgba(0,0,0,0.35)",

                        "backdropFilter": "blur(15px)",

                        # ANIMATION
                        "transition": "0.3s ease"
                    }
                ),

                # =========================================
                # BUTTON
                # =========================================

                html.Button(

                    "Get Weather",

                    id="weather-btn",

                    n_clicks=0,

                    style={

                        "marginLeft": "20px",

                        "height": "75px",

                        "padding": "0px 40px",

                        "border": "none",

                        "borderRadius": "60px",

                        "cursor": "pointer",

                        "fontSize": "24px",

                        "fontWeight": "bold",

                        "background":
                        "linear-gradient(135deg, #4facfe, #00f2fe)",

                        "color": "white",

                        "boxShadow":
                        "0 10px 30px rgba(0,0,0,0.35)",

                        "transition": "0.3s ease"
                    }
                )
            ]
        ),

        html.Br(),
        html.Br(),
        html.Br(),

        # =========================================
        # WEATHER OUTPUT CARD
        # =========================================

        html.Div(

            id="weather-output",

            className="weather-card",

            style={

                "width": "650px",

                "margin": "auto",

                "padding": "40px",

                "borderRadius": "35px",

                "background": "rgba(255,255,255,0.15)",

                "backdropFilter": "blur(15px)",

                "color": "white",

                "textAlign": "center",

                "boxShadow":
                "0 8px 32px rgba(0,0,0,0.37)",

                "border":
                "1px solid rgba(255,255,255,0.18)"
            }
        ),

        html.Br(),

        # =========================================
        # DOWNLOAD BUTTON
        # =========================================

        html.Div(

            style={
                "textAlign": "center"
            },

            children=[

                html.Button(

                    "Download CSV",

                    id="download-btn",

                    n_clicks=0,

                    style={

                        "padding": "18px 35px",

                        "border": "none",

                        "borderRadius": "60px",

                        "cursor": "pointer",

                        "fontSize": "22px",

                        "fontWeight": "bold",

                        "background":
                        "linear-gradient(135deg, #43e97b, #38f9d7)",

                        "color": "white",

                        "boxShadow":
                        "0 10px 30px rgba(0,0,0,0.35)"
                    }
                ),

                dcc.Download(
                    id="download-data"
                )
            ]
        )
    ]
)

# =========================================
# WEATHER CALLBACK
# =========================================

@app.callback(

    [
        Output("weather-output", "children"),
        Output("main-div", "style")
    ],

    Input("weather-btn", "n_clicks"),

    State("city-input", "value")
)

def get_weather(n_clicks, city):

    if n_clicks == 0 or not city:

        return (

            "",

            {
                "backgroundImage":
                f"url('{DEFAULT_BACKGROUND}')",

                "backgroundSize": "cover",

                "backgroundPosition": "center",

                "minHeight": "100vh",

                "padding": "40px"
            }
        )

    # =========================================
    # API REQUEST
    # =========================================

    url = (
        "https://api.openweathermap.org/data/2.5/weather"
    )

    params = {

        "q": city,

        "appid": API_KEY,

        "units": "metric"
    }

    response = requests.get(
        url,
        params=params
    )

    # =========================================
    # ERROR HANDLING
    # =========================================

    if response.status_code != 200:

        return (

            html.Div([

                html.H2(
                    "City Not Found"
                ),

                html.P(
                    "Check spelling and try again."
                )
            ]),

            {
                "backgroundImage":
                f"url('{DEFAULT_BACKGROUND}')",

                "backgroundSize": "cover",

                "backgroundPosition": "center",

                "minHeight": "100vh",

                "padding": "40px"
            }
        )

    data = response.json()

    # =========================================
    # EXTRACT DATA
    # =========================================

    city_name = data["name"]

    country = data["sys"]["country"]

    temperature = data["main"]["temp"]

    feels_like = data["main"]["feels_like"]

    humidity = data["main"]["humidity"]

    pressure = data["main"]["pressure"]

    wind_speed = data["wind"]["speed"]

    weather_main = data["weather"][0]["main"]

    description = data["weather"][0]["description"]

    # =========================================
    # BACKGROUND CHANGE
    # =========================================

    if weather_main == "Rain":

        background = (
            "https://images.unsplash.com/"
            "photo-1515694346937-94d85e41e6f0"
        )

    elif weather_main == "Clouds":

        background = (
            "https://images.unsplash.com/"
            "photo-1534088568595-a066f410bcda"
        )

    elif weather_main == "Clear":

        background = (
            "https://images.unsplash.com/"
            "photo-1507525428034-b723cf961d3e"
        )

    elif weather_main == "Snow":

        background = (
            "https://images.unsplash.com/"
            "photo-1517299321609-52687d1bc55a"
        )

    elif weather_main == "Thunderstorm":

        background = (
            "https://images.unsplash.com/"
            "photo-1605727216801-e27ce1d0cc28"
        )

    else:

        background = (
            "https://images.unsplash.com/"
            "photo-1499346030926-9a72daac6c63"
        )

    # =========================================
    # WEATHER CARD
    # =========================================

    output = html.Div([

        html.H2(
            f"{city_name}, {country}"
        ),

        html.Hr(),

        html.H2(
            f"🌡 {temperature} °C"
        ),

        html.H3(
            f"🥵 Feels Like: {feels_like} °C"
        ),

        html.H3(
            f"💧 Humidity: {humidity}%"
        ),

        html.H3(
            f"🌀 Pressure: {pressure} hPa"
        ),

        html.H3(
            f"🌬 Wind Speed: {wind_speed} m/s"
        ),

        html.H3(
            f"☁ Condition: {weather_main}"
        ),

        html.H3(
            f"📄 {description}"
        )
    ])

    style = {

        "backgroundImage":
        f"url('{background}')",

        "backgroundSize": "cover",

        "backgroundPosition": "center",

        "minHeight": "100vh",

        "padding": "40px",

        "transition": "0.5s"
    }

    return output, style

# =========================================
# DOWNLOAD CSV
# =========================================

@app.callback(

    Output("download-data", "data"),

    Input("download-btn", "n_clicks"),

    State("city-input", "value"),

    prevent_initial_call=True
)

def download_csv(n_clicks, city):

    if not city:
        return

    url = (
        "https://api.openweathermap.org/data/2.5/weather"
    )

    params = {

        "q": city,

        "appid": API_KEY,

        "units": "metric"
    }

    response = requests.get(
        url,
        params=params
    )

    data = response.json()

    df = pd.DataFrame({

        "City": [data["name"]],

        "Country": [data["sys"]["country"]],

        "Temperature":
        [data["main"]["temp"]],

        "Feels Like":
        [data["main"]["feels_like"]],

        "Humidity":
        [data["main"]["humidity"]],

        "Pressure":
        [data["main"]["pressure"]],

        "Wind Speed":
        [data["wind"]["speed"]],

        "Condition":
        [data["weather"][0]["main"]],

        "Description":
        [data["weather"][0]["description"]]
    })

    return dcc.send_data_frame(

        df.to_csv,

        f"{city}_weather.csv",

        index=False
    )

# =========================================
# RUN APP
# =========================================

if __name__ == "__main__":

    app.run(debug=True)