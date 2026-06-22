# import streamlit as st
# import pandas as pd
# import folium
# import joblib
# from streamlit_folium import st_folium
# from folium.plugins import HeatMap

# st.set_page_config(page_title="AQI & HCHO Monitoring System", layout="wide")

# aqi_df = pd.read_csv("data/aqi_sample.csv")

# hcho_df = pd.read_csv("data/hcho_sample.csv")

# fire_df = pd.read_csv("data/fire_sample.csv")

# sat_df = pd.read_csv("data/sentinel_hcho.csv")

# firms_df = pd.read_csv("data/firms_fire_data.csv")


# def get_category(aqi):
#     if aqi <= 50:
#         return "Good"
#     elif aqi <= 100:
#         return "Satisfactory"
#     elif aqi <= 200:
#         return "Moderate"
#     elif aqi <= 300:
#         return "Poor"
#     elif aqi <= 400:
#         return "Very Poor"
#     return "Severe"


# aqi_df["Category"] = aqi_df["aqi"].apply(get_category)

# st.sidebar.title("⚙ Dashboard Controls")
# st.sidebar.success("AQI Module ✓")
# st.sidebar.success("HCHO Module ✓")
# st.sidebar.success("Fire Module ✓")
# st.sidebar.success("ML Module ✓")
# st.sidebar.divider()

# selected_city = st.sidebar.selectbox("Select City", ["All"] + list(aqi_df["city"]))

# filtered_df = (
#     aqi_df.copy() if selected_city == "All" else aqi_df[aqi_df["city"] == selected_city]
# )

# st.title("🌍 AQI & HCHO Monitoring System")

# st.markdown("---")

# col1, col2, col3, col4 = st.columns(4)

# col1.metric("AQI Stations", len(aqi_df))

# col2.metric("HCHO Hotspots", len(sat_df[sat_df["hcho"] > 0.00020]))

# col3.metric("Fire Events", int(firms_df["fire_count"].sum()))

# col4.metric("Highest AQI", int(aqi_df["aqi"].max()))

# st.markdown("---")

# st.info(
#     """
#     This dashboard analyzes the relationship between
#     Biomass Burning, Formaldehyde (HCHO), and Air Quality Index (AQI)
#     using satellite-inspired datasets.
#     """
# )

# tab1, tab2, tab3, tab4, tab5 = st.tabs(
#     [
#         "🌍 AQI Monitoring",
#         "🧪 HCHO Hotspots",
#         "🔥 Biomass Burning",
#         "🤖 AQI Prediction",
#         "📈 Correlation Analysis",
#     ]
# )

# with tab1:
#     st.subheader("📊 AQI Summary")

#     c1, c2, c3 = st.columns(3)
#     c1.metric("Cities Monitored", len(filtered_df))
#     c2.metric("Average AQI", round(filtered_df["aqi"].mean(), 1))
#     c3.metric("Maximum AQI", int(filtered_df["aqi"].max()))

#     m = folium.Map(location=[22.5, 78.9], zoom_start=5)

#     for _, row in filtered_df.iterrows():
#         color = "green"
#         if row["aqi"] > 250:
#             color = "red"
#         elif row["aqi"] > 150:
#             color = "orange"

#         folium.CircleMarker(
#             location=[row["lat"], row["lon"]],
#             radius=10,
#             popup=f"{row['city']} | AQI: {row['aqi']}",
#             color=color,
#             fill=True,
#         ).add_to(m)

#     HeatMap(
#         [[r["lat"], r["lon"], r["aqi"]] for _, r in filtered_df.iterrows()],
#         radius=25,
#         blur=15,
#     ).add_to(m)

#     st_folium(m, width=1200, height=550)
#     st.dataframe(filtered_df, use_container_width=True)
#     st.bar_chart(filtered_df["Category"].value_counts())

#     st.subheader("⚠ AQI Risk Classification")

# risk_df = filtered_df.copy()

# risk_df = risk_df.sort_values("aqi", ascending=False)

# st.dataframe(risk_df[["city", "aqi", "Category"]], use_container_width=True)

# highest_city = risk_df.iloc[0]

# st.error(f"Highest Risk City: {highest_city['city']} (AQI {highest_city['aqi']})")

# with tab2:
#     st.subheader("🧪 HCHO Hotspot Detection")

#     hcho_df = pd.read_csv("data/hcho_sample.csv")
#     st.dataframe(hcho_df, use_container_width=True)

#     hmap = folium.Map(location=[22.5, 78.9], zoom_start=5)

#     for _, row in hcho_df.iterrows():
#         color = "green"
#         if row["hcho"] > 0.00030:
#             color = "red"
#         elif row["hcho"] > 0.00015:
#             color = "orange"

#         folium.CircleMarker(
#             location=[row["lat"], row["lon"]],
#             radius=12,
#             popup=f"{row['city']} | HCHO: {row['hcho']}",
#             color=color,
#             fill=True,
#         ).add_to(hmap)

#     st_folium(hmap, width=1200, height=550)
#     st.bar_chart(hcho_df.set_index("city")["hcho"])
#     st.subheader("🛰 Sentinel-5P HCHO Satellite Layer")

# sat_df = pd.read_csv("data/sentinel_hcho.csv")

# st.dataframe(sat_df, use_container_width=True)

# sat_map = folium.Map(location=[22.5, 78.9], zoom_start=5)

# for _, row in sat_df.iterrows():
#     if row["hcho"] > 0.00030:
#         color = "red"
#     elif row["hcho"] > 0.00015:
#         color = "orange"
#     else:
#         color = "green"

#     folium.CircleMarker(
#         location=[row["lat"], row["lon"]],
#         radius=15,
#         popup=f"""
#         State: {row["state"]}
#         <br>HCHO: {row["hcho"]}
#         """,
#         color=color,
#         fill=True,
#         fill_opacity=0.8,
#     ).add_to(sat_map)

# st_folium(sat_map, width=1200, height=500)

# st.subheader("🏆 HCHO Hotspot Ranking")

# ranking = sat_df.sort_values("hcho", ascending=False)

# st.dataframe(ranking, use_container_width=True)

# st.bar_chart(ranking.set_index("state")["hcho"])

# with tab3:
#     st.subheader("🔥 Biomass Burning Analysis")

#     fire_df = pd.read_csv("data/fire_sample.csv")
#     st.dataframe(fire_df, use_container_width=True)

#     fmap = folium.Map(location=[22.5, 78.9], zoom_start=5)

#     for _, row in fire_df.iterrows():
#         folium.CircleMarker(
#             location=[row["lat"], row["lon"]],
#             radius=max(5, row["fire_count"] / 10),
#             popup=f"{row['location']} | Fire Count: {row['fire_count']}",
#             color="red",
#             fill=True,
#         ).add_to(fmap)

#     st_folium(fmap, width=1200, height=550)
#     st.bar_chart(fire_df.set_index("location")["fire_count"])

#     st.subheader("🚨 NASA FIRMS Fire Hotspots")

# firms_df = pd.read_csv("data/firms_fire_data.csv")

# st.dataframe(firms_df, use_container_width=True)

# firms_map = folium.Map(location=[22.5, 78.9], zoom_start=5)

# for _, row in firms_df.iterrows():
#     if row["brightness"] > 340:
#         color = "red"
#     elif row["brightness"] > 300:
#         color = "orange"
#     else:
#         color = "yellow"

#     folium.CircleMarker(
#         location=[row["latitude"], row["longitude"]],
#         radius=max(6, row["fire_count"] / 5),
#         popup=f"""
#         State: {row["state"]}
#         <br>Brightness: {row["brightness"]}
#         <br>Fire Count: {row["fire_count"]}
#         """,
#         color=color,
#         fill=True,
#         fill_opacity=0.8,
#     ).add_to(firms_map)

# st_folium(firms_map, width=1200, height=500)

# st.subheader("🏆 Top Burning States")

# ranking = firms_df.sort_values("fire_count", ascending=False)

# st.dataframe(ranking, use_container_width=True)

# st.bar_chart(ranking.set_index("state")["fire_count"])

# with tab4:
#     st.subheader("🤖 AQI Prediction")

#     try:
#         model = joblib.load("models/aqi_model.pkl")

#         pm25 = st.number_input("PM2.5", value=100.0)
#         pm10 = st.number_input("PM10", value=180.0)
#         no2 = st.number_input("NO2", value=40.0)
#         co = st.number_input("CO", value=0.8)
#         temp = st.number_input("Temperature", value=35.0)
#         humidity = st.number_input("Humidity", value=50.0)

#         if st.button("Predict AQI"):
#             pred = model.predict([[pm25, pm10, no2, co, temp, humidity]])[0]
#             st.success(f"Predicted AQI: {pred:.2f}")

#     except Exception as e:
#         st.error(f"Model Error: {e}")

# # ==================================================
# # CORRELATION TAB
# # ==================================================

# with tab5:
#     st.subheader("📈 Fire vs HCHO Correlation")

#     corr_df = pd.read_csv("data/correlation_data.csv")

#     st.dataframe(corr_df, use_container_width=True)

#     st.subheader("HCHO Levels")

#     st.bar_chart(corr_df.set_index("state")["hcho"])

#     st.subheader("Fire Counts")

#     st.bar_chart(corr_df.set_index("state")["fire_count"])

#     correlation = corr_df["hcho"].corr(corr_df["fire_count"])

#     st.metric("Correlation Coefficient", round(correlation, 3))

#     if correlation > 0.7:
#         st.success(
#             "Strong positive relationship between biomass burning and HCHO concentration."
#         )
#     else:
#         st.warning("Weak relationship detected.")


# st.subheader("📥 Download Data")

# csv = corr_df.to_csv(index=False)

# st.download_button(
#     label="Download Correlation Report",
#     data=csv,
#     file_name="correlation_report.csv",
#     mime="text/csv",
# )

# st.subheader("📥 Download Project Report")

# report_df = pd.DataFrame(
#     {
#         "Metric": [
#             "Total AQI Stations",
#             "Total Fire Events",
#             "HCHO Hotspots",
#             "Maximum AQI",
#         ],
#         "Value": [
#             len(aqi_df),
#             int(firms_df["fire_count"].sum()),
#             len(sat_df[sat_df["hcho"] > 0.00020]),
#             int(aqi_df["aqi"].max()),
#         ],
#     }
# )

# st.dataframe(report_df, use_container_width=True)

# csv = report_df.to_csv(index=False)

# st.download_button(
#     label="📥 Download Full Report",
#     data=csv,
#     file_name="AQI_HCHO_Report.csv",
#     mime="text/csv",
# )

import streamlit as st
import pandas as pd
import folium
import joblib
from streamlit_folium import st_folium
from folium.plugins import HeatMap

st.set_page_config(page_title="AQI & HCHO Monitoring System", layout="wide")

aqi_df = pd.read_csv("data/aqi_sample.csv")
hcho_df = pd.read_csv("data/hcho_sample.csv")
fire_df = pd.read_csv("data/fire_sample.csv")
sat_df = pd.read_csv("data/sentinel_hcho.csv")
firms_df = pd.read_csv("data/firms_fire_data.csv")


def get_category(aqi):
    if aqi <= 50:
        return "Good"
    elif aqi <= 100:
        return "Satisfactory"
    elif aqi <= 200:
        return "Moderate"
    elif aqi <= 300:
        return "Poor"
    elif aqi <= 400:
        return "Very Poor"
    return "Severe"


aqi_df["Category"] = aqi_df["aqi"].apply(get_category)

st.sidebar.title("⚙ Dashboard Controls")
st.sidebar.success("AQI Module ✓")
st.sidebar.success("HCHO Module ✓")
st.sidebar.success("Fire Module ✓")
st.sidebar.success("ML Module ✓")
st.sidebar.divider()

selected_city = st.sidebar.selectbox("Select City", ["All"] + list(aqi_df["city"]))

filtered_df = (
    aqi_df.copy() if selected_city == "All" else aqi_df[aqi_df["city"] == selected_city]
)

st.title("🌍 AQI & HCHO Monitoring System")

st.markdown("---")

col1, col2, col3, col4 = st.columns(4)

col1.metric("AQI Stations", len(aqi_df))
col2.metric("HCHO Hotspots", len(sat_df[sat_df["hcho"] > 0.00020]))
col3.metric("Fire Events", int(firms_df["fire_count"].sum()))
col4.metric("Highest AQI", int(aqi_df["aqi"].max()))

st.markdown("---")

st.info(
    """
    This dashboard analyzes the relationship between
    Biomass Burning, Formaldehyde (HCHO), and Air Quality Index (AQI)
    using satellite-inspired datasets.
    """
)

tab1, tab2, tab3, tab4, tab5 = st.tabs(
    [
        "🌍 AQI Monitoring",
        "🧪 HCHO Hotspots",
        "🔥 Biomass Burning",
        "🤖 AQI Prediction",
        "📈 Correlation Analysis",
    ]
)

# ================= TAB 1 =================
with tab1:
    st.subheader("📊 AQI Summary")

    c1, c2, c3 = st.columns(3)
    c1.metric("Cities Monitored", len(filtered_df))
    c2.metric("Average AQI", round(filtered_df["aqi"].mean(), 1))
    c3.metric("Maximum AQI", int(filtered_df["aqi"].max()))

    m = folium.Map(location=[22.5, 78.9], zoom_start=5)

    for _, row in filtered_df.iterrows():
        color = "green"
        if row["aqi"] > 250:
            color = "red"
        elif row["aqi"] > 150:
            color = "orange"

        folium.CircleMarker(
            location=[row["lat"], row["lon"]],
            radius=10,
            popup=f"{row['city']} | AQI: {row['aqi']}",
            color=color,
            fill=True,
        ).add_to(m)

    HeatMap(
        [[r["lat"], r["lon"], r["aqi"]] for _, r in filtered_df.iterrows()],
        radius=25,
        blur=15,
    ).add_to(m)

    st_folium(m, width=1200, height=550)
    st.dataframe(filtered_df, use_container_width=True)
    st.bar_chart(filtered_df["Category"].value_counts())

    st.subheader("⚠ AQI Risk Classification")

    risk_df = filtered_df.copy()
    risk_df = risk_df.sort_values("aqi", ascending=False)

    st.dataframe(risk_df[["city", "aqi", "Category"]], use_container_width=True)

    highest_city = risk_df.iloc[0]
    st.error(f"Highest Risk City: {highest_city['city']} (AQI {highest_city['aqi']})")


# ================= TAB 2 =================
with tab2:
    st.subheader("🧪 HCHO Hotspot Detection")

    st.dataframe(hcho_df, use_container_width=True)

    hmap = folium.Map(location=[22.5, 78.9], zoom_start=5)

    for _, row in hcho_df.iterrows():
        color = "green"
        if row["hcho"] > 0.00030:
            color = "red"
        elif row["hcho"] > 0.00015:
            color = "orange"

        folium.CircleMarker(
            location=[row["lat"], row["lon"]],
            radius=12,
            popup=f"{row['city']} | HCHO: {row['hcho']}",
            color=color,
            fill=True,
        ).add_to(hmap)

    st_folium(hmap, width=1200, height=550)

    st.bar_chart(hcho_df.set_index("city")["hcho"])

    st.subheader("🛰 Sentinel-5P HCHO Satellite Layer")

    st.dataframe(sat_df, use_container_width=True)

    sat_map = folium.Map(location=[22.5, 78.9], zoom_start=5)

    for _, row in sat_df.iterrows():
        color = "green"
        if row["hcho"] > 0.00030:
            color = "red"
        elif row["hcho"] > 0.00015:
            color = "orange"

        folium.CircleMarker(
            location=[row["lat"], row["lon"]],
            radius=15,
            popup=f"""
            State: {row["state"]}
            <br>HCHO: {row["hcho"]}
            """,
            color=color,
            fill=True,
            fill_opacity=0.8,
        ).add_to(sat_map)

    st_folium(sat_map, width=1200, height=500)

    st.subheader("🏆 HCHO Hotspot Ranking")

    ranking = sat_df.sort_values("hcho", ascending=False)

    st.dataframe(ranking, use_container_width=True)

    st.bar_chart(ranking.set_index("state")["hcho"])


# ================= TAB 3 =================
with tab3:
    st.subheader("🔥 Biomass Burning Analysis")

    st.dataframe(fire_df, use_container_width=True)

    fmap = folium.Map(location=[22.5, 78.9], zoom_start=5)

    for _, row in fire_df.iterrows():
        folium.CircleMarker(
            location=[row["lat"], row["lon"]],
            radius=max(5, row["fire_count"] / 10),
            popup=f"{row['location']} | Fire Count: {row['fire_count']}",
            color="red",
            fill=True,
        ).add_to(fmap)

    st_folium(fmap, width=1200, height=550)

    st.bar_chart(fire_df.set_index("location")["fire_count"])

    st.subheader("🚨 NASA FIRMS Fire Hotspots")

    st.dataframe(firms_df, use_container_width=True)

    firms_map = folium.Map(location=[22.5, 78.9], zoom_start=5)

    for _, row in firms_df.iterrows():
        if row["brightness"] > 340:
            color = "red"
        elif row["brightness"] > 300:
            color = "orange"
        else:
            color = "yellow"

        folium.CircleMarker(
            location=[row["latitude"], row["longitude"]],
            radius=max(6, row["fire_count"] / 5),
            popup=f"""
            State: {row["state"]}
            <br>Brightness: {row["brightness"]}
            <br>Fire Count: {row["fire_count"]}
            """,
            color=color,
            fill=True,
            fill_opacity=0.8,
        ).add_to(firms_map)

    st_folium(firms_map, width=1200, height=500)

    st.subheader("🏆 Top Burning States")

    ranking = firms_df.sort_values("fire_count", ascending=False)

    st.dataframe(ranking, use_container_width=True)

    st.bar_chart(ranking.set_index("state")["fire_count"])


# ================= TAB 4 =================
with tab4:
    st.subheader("🤖 AQI Prediction")

    try:
        model = joblib.load("models/aqi_model.pkl")

        pm25 = st.number_input("PM2.5", value=100.0)
        pm10 = st.number_input("PM10", value=180.0)
        no2 = st.number_input("NO2", value=40.0)
        co = st.number_input("CO", value=0.8)
        temp = st.number_input("Temperature", value=35.0)
        humidity = st.number_input("Humidity", value=50.0)

        if st.button("Predict AQI"):
            pred = model.predict([[pm25, pm10, no2, co, temp, humidity]])[0]
            st.success(f"Predicted AQI: {pred:.2f}")

    except Exception as e:
        st.error(f"Model Error: {e}")


# ================= TAB 5 =================
with tab5:
    st.subheader("📈 Fire vs HCHO Correlation")

    corr_df = pd.read_csv("data/correlation_data.csv")

    st.dataframe(corr_df, use_container_width=True)

    st.subheader("HCHO Levels")
    st.bar_chart(corr_df.set_index("state")["hcho"])

    st.subheader("Fire Counts")
    st.bar_chart(corr_df.set_index("state")["fire_count"])

    correlation = corr_df["hcho"].corr(corr_df["fire_count"])

    st.metric("Correlation Coefficient", round(correlation, 3))

    if correlation > 0.7:
        st.success(
            "Strong positive relationship between biomass burning and HCHO concentration."
        )
    else:
        st.warning("Weak relationship detected.")


# ================= DOWNLOAD (OUTSIDE TABS - FIXED) =================
st.subheader("📥 Download Data")

csv = corr_df.to_csv(index=False)

st.download_button(
    label="Download Correlation Report",
    data=csv,
    file_name="correlation_report.csv",
    mime="text/csv",
)

st.subheader("📥 Download Project Report")

report_df = pd.DataFrame(
    {
        "Metric": [
            "Total AQI Stations",
            "Total Fire Events",
            "HCHO Hotspots",
            "Maximum AQI",
        ],
        "Value": [
            len(aqi_df),
            int(firms_df["fire_count"].sum()),
            len(sat_df[sat_df["hcho"] > 0.00020]),
            int(aqi_df["aqi"].max()),
        ],
    }
)

st.dataframe(report_df, use_container_width=True)

csv = report_df.to_csv(index=False)

st.download_button(
    label="📥 Download Full Report",
    data=csv,
    file_name="AQI_HCHO_Report.csv",
    mime="text/csv",
)
