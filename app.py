import streamlit as st
import pandas as pd

st.set_page_config(page_title="Ultimate DataFrame Builder", layout="wide")
st.title("📊 Ultimate DataFrame Builder")

# ---------------- Session State ----------------
if "datasets" not in st.session_state:
    st.session_state.datasets = {}

if "df" not in st.session_state:
    st.session_state.df = pd.DataFrame()

if "dtypes" not in st.session_state:
    st.session_state.dtypes = {}

# ---------------- Helper: Auto Detect Types ----------------
def auto_detect_types(df):
    dtypes = {}
    for col in df.columns:
        # Try numeric
        try:
            df[col] = pd.to_numeric(df[col])
            dtypes[col] = "float"
            continue
        except:
            pass

        # Try date
        try:
            df[col] = pd.to_datetime(df[col]).dt.date
            dtypes[col] = "date"
        except:
            dtypes[col] = "string"

    return df, dtypes

# ---------------- Sidebar ----------------
st.sidebar.header("🗂 Dataset Manager")

dataset_name = st.sidebar.text_input("Dataset name")

if st.sidebar.button("💾 Save Dataset"):
    if dataset_name and not st.session_state.df.empty:
        st.session_state.datasets[dataset_name] = (
            st.session_state.df.copy(),
            st.session_state.dtypes.copy()
        )
        st.sidebar.success("Dataset saved")

if st.session_state.datasets:
    selected = st.sidebar.selectbox(
        "📂 Load Dataset",
        [""] + list(st.session_state.datasets.keys())
    )

    if selected:
        st.session_state.df, st.session_state.dtypes = (
            st.session_state.datasets[selected][0].copy(),
            st.session_state.datasets[selected][1].copy()
        )

# ---------------- Upload CSV ----------------
st.subheader("📤 Upload CSV")

uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    df, dtypes = auto_detect_types(df)
    st.session_state.df = df
    st.session_state.dtypes = dtypes
    st.success("CSV uploaded and loaded")

# ---------------- Create Columns ----------------
st.subheader("➕ Create New DataFrame")

with st.form("create_columns"):
    col_names = st.text_input(
        "Column names (comma-separated)",
        placeholder="name, age, salary, join_date"
    )

    col_types = st.multiselect(
        "Column data types (same order)",
        ["string", "int", "float", "date"]
    )

    if st.form_submit_button("Create / Reset DataFrame"):
        cols = [c.strip() for c in col_names.split(",") if c.strip()]
        if not cols:
            st.warning("Enter column names.")
        elif len(cols) != len(col_types):
            st.warning("Number of columns and types must match.")
        else:
            st.session_state.df = pd.DataFrame(columns=cols)
            st.session_state.dtypes = dict(zip(cols, col_types))

# ---------------- Add Row ----------------
st.subheader("➕ Add New Row")

if not st.session_state.df.empty:
    with st.form("add_row"):
        row = {}
        for col, dtype in st.session_state.dtypes.items():
            if dtype == "int":
                row[col] = st.number_input(col, step=1)
            elif dtype == "float":
                row[col] = st.number_input(col)
            elif dtype == "date":
                row[col] = st.date_input(col)
            else:
                row[col] = st.text_input(col)

        if st.form_submit_button("Add Row"):
            st.session_state.df.loc[len(st.session_state.df)] = row

# ---------------- Data Editor ----------------
st.subheader("✏️ Edit / Delete Data")

if not st.session_state.df.empty:
    st.session_state.df = st.data_editor(
        st.session_state.df,
        num_rows="dynamic",
        use_container_width=True
    )

# ---------------- Rename Column ----------------
st.subheader("🔤 Rename Column")

if not st.session_state.df.empty:
    old = st.selectbox("Select column", st.session_state.df.columns)
    new = st.text_input("New column name")

    if st.button("Rename Column"):
        if new.strip():
            st.session_state.df.rename(columns={old: new}, inplace=True)
            st.session_state.dtypes[new] = st.session_state.dtypes.pop(old)

# ---------------- Remove Column ----------------
st.subheader("🗑 Remove Column")

if not st.session_state.df.empty:
    col_del = st.selectbox("Column to delete", st.session_state.df.columns)

    if st.button("Delete Column"):
        st.session_state.df.drop(columns=[col_del], inplace=True)
        st.session_state.dtypes.pop(col_del, None)

# ---------------- Download ----------------
st.subheader("⬇️ Download Final Data")

if not st.session_state.df.empty:
    csv = st.session_state.df.to_csv(
        index=False,
        date_format="%Y-%m-%d"
    ).encode("utf-8")

    st.download_button(
        "Download CSV",
        csv,
        "dataframe.csv",
        "text/csv"
    )
