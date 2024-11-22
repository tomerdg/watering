import streamlit as st
import pandas as pd
import os
from datetime import  datetime
# Initializing data
columns = ["Block \\ Tunnel", "Name", "BB\\RB"]
data = [
    ["M", "Legacy", "BB"], ["1", "Titan", "BB"], ["1", "Och", "BB"], ["1", "Colibri", "BB"],
    ["2", "Haven S", "BB"], ["2", "Haven C", "BB"], ["2", "Clarita S", "RB"], ["2", "Biloxi", "BB"],
    ["2", "Clarita N", "RB"], ["2", "Titan", "BB"], ["3", "Biloxi N", "BB"], ["3", "Biloxi C", "BB"],
    ["3", "Louis", "RB"], ["3", "Rabel", "BB"], ["3", "Haven C", "BB"], ["3", "Clarita", "RB"],
    ["3", "Haven S", "BB"], ["T1(47)", "Louis", "RB"], ["T2(46)", "Amalya", "RB"], ["T3 w(50)", "Clarita", "RB"],
    ["T4(51)", "Clarita", "RB"], ["T5(52)", "Clarita", "RB"], ["T6(53)", "Clarita", "RB"], ["T7(54)", "osna", "RB"],
    ["T8(55)", "osna", "RB"], ["T9(56)", "osna", "RB"], ["T10(57)", "osna", "RB"], ["4(61)", "damba", "BB"],
    ["4(62)", "damba", "BB"], ["4(62)", "damba", "BB"], ["4(63)", "damba", "BB"], ["t11", "", ""]
]

# Dropdown data
options = pd.DataFrame(data, columns=columns)

# App state
if "dataframe" not in st.session_state:
    st.session_state.dataframe = pd.DataFrame(columns=[
        "Block \\ Tunnel", "Name", "BB\\RB", "Test No.", "Nekez_ml", "Nekez_EC",
        "Nekez_Ratio (%)", "Taftefet_ml", "Taftefet_EC"
    ])

# Streamlit UI
st.title("Hashkaya")

# Arrange input fields in two columns
col1, col2 = st.columns(2)

# Inputs in the first column
with col1:
    test_no = st.number_input("Test No. (1-7)", min_value=1, max_value=7, step=1)

    nekez_ml = st.number_input("Nekez ml", min_value=0, step=1)
    taftefet_ml = st.number_input("Taftefet ml", min_value=0, step=1)


# Inputs in the second column
with col2:
    selected_row = st.selectbox("Choose Block/Tunnel, Name, BB\\RB:", options.apply(
        lambda row: f"{row[0]} - {row[1]} - {row[2]}", axis=1))
    nekez_ec = st.number_input("Nekez EC", min_value=0.0, step=0.1, format="%.1f")
    taftefet_ec = st.number_input("Taftefet EC", min_value=0.0, step=0.1, format="%.1f")

# # Calculate ratios
nekez_ratio = (nekez_ml / taftefet_ml * 100) if taftefet_ml != 0 else 0


# ADD button
if st.button("ADD"):
    block_tunnel, name, bb_rb = selected_row.split(" - ")
    cur_time = datetime.now()
    new_row = {
        "Block \\ Tunnel": block_tunnel, "Name": name, "BB\\RB": bb_rb, "Test No.": test_no,
        "Nekez_ml": nekez_ml, "Nekez_EC": nekez_ec, "Nekez_Ratio (%)": round(nekez_ratio, 2),
        "Taftefet_ml": taftefet_ml, "Taftefet_EC": taftefet_ec, "Time":cur_time
    }
    st.session_state.dataframe = pd.concat([st.session_state.dataframe, pd.DataFrame([new_row])], ignore_index=True)

# SAVE button
if st.button("SAVE"):

    output_file = "hashkaya.csv"
    if os.path.exists(output_file):
            # Append to the file without headers
        st.session_state.dataframe.to_csv(output_file, mode="a", header=False, index=False)
    else:
            # Create the file with headers
        st.session_state.dataframe.to_csv(output_file, mode="w", header=True, index=False)

    st.session_state.dataframe.to_csv("output.csv", index=False, mode='a')
    st.success(f"Added {len(st.session_state.dataframe)} records to `{output_file}`")
    st.session_state.dataframe = pd.DataFrame(columns=st.session_state.dataframe.columns)

# CLEAR ALL button
if st.button("CLEAR ALL"):
    st.session_state.dataframe = pd.DataFrame(columns=st.session_state.dataframe.columns)
    st.success("All data cleared.")

# Display data
st.write("### Data Table")
st.dataframe(st.session_state.dataframe)
