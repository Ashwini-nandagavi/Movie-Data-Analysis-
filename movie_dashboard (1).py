import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ========================= LOGIN SETUP =========================
USERNAME = "admin"
PASSWORD = "1234"

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# ========================= DATA LOADER =========================
@st.cache_data
def load_movie_data(custom_path: str = None):
    candidates = []
    if custom_path:
        candidates.append(custom_path)
    candidates.extend([
        r"C:\Users\HP\Desktop\Myapp\movie.csv.xls",
        "movie.csv.xls",
        "movie.csv"
    ])
    last_exc = None
    for p in candidates:
        try:
            if str(p).lower().endswith(".csv") or ".csv" in str(p).lower():
                df = pd.read_csv(p)
            else:
                df = pd.read_excel(p, engine="openpyxl")
            df.columns = df.columns.astype(str).str.strip()
            return df
        except Exception as e:
            last_exc = e
            continue
    raise FileNotFoundError(f"Could not load dataset. Tried paths: {candidates}. Last error: {last_exc}")

# ========================= LOGIN PAGE =========================
if not st.session_state.logged_in:
    st.title("🎬 Movie Data Analysis Dashboard")
    st.subheader("Please login to continue")

    username = st.text_input("👤 Username")
    password = st.text_input("🔒 Password", type="password")

    if st.button("Login"):
        if username == USERNAME and password == PASSWORD:
            st.session_state.logged_in = True
            st.success("✅ Login successful! Redirecting...")
            st.rerun()
        else:
            st.error("❌ Invalid username or password.")

# ========================= MAIN DASHBOARD =========================
else:
    st.sidebar.title("📊 Navigation")
    option = st.sidebar.selectbox(
        "Choose an Option:",
        (
            "🏠 Home",
            "Display Data",
            "Color vs Black & White Count",
            "🎭 Movie Genres",
            "🌏 Bar Graph - Australia, Germany, Japan",
            "💰 Top 5 Movies (Highest Budget)",
            "📅 Movies Released in 2009",
            "ℹ️ About Us"
        )
    )

    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

    st.sidebar.markdown("---")
    st.sidebar.caption("Optional: Enter custom dataset path")
    data_path_input = st.sidebar.text_input("📂 Custom Dataset Path", "")

    try:
        df = load_movie_data(custom_path=data_path_input.strip() or None)
    except Exception as e:
        st.error(f"❌ Unable to load dataset.\n\n*Error:* {e}")
        st.stop()

    # ========================= HOME PAGE =========================
    if option == "🏠 Home":
        st.title("🎬 Movie Data Analysis Dashboard")
        st.subheader("Explore insights from the movie dataset")
        st.image(
            "https://cdn.pixabay.com/photo/2016/03/27/19/54/cinema-1282796_1280.jpg",
            caption="Movies & Cinema World",
            use_container_width=True
        )
        st.success("👉 Use the sidebar to navigate different analyses.")

    # ========================= DISPLAY DATA =========================
    elif option == "Display Data":
        st.header("📄 Complete Movie Dataset")
        st.dataframe(df)

    # ========================= COLOR VS BLACK & WHITE =========================
    elif option == "Color vs Black & White Count":
        st.header("🎨 Color vs Black & White Movies Count")
        if "color" in df.columns:
            color_count = df["color"].value_counts()
            st.write(color_count)

            # Bar Graph
            fig, ax = plt.subplots()
            ax.bar(color_count.index, color_count.values, color=["#FFD700", "#708090"])
            ax.set_xlabel("Movie Type")
            ax.set_ylabel("Count")
            ax.set_title("Color vs Black & White Movies")
            st.pyplot(fig)

            # Pie Chart
            fig, ax = plt.subplots()
            ax.pie(color_count.values, labels=color_count.index, autopct="%1.1f%%", startangle=90)
            ax.set_title("Color vs Black & White Movies")
            st.pyplot(fig)
        else:
            st.warning("The dataset has no 'color' column.")

    # ========================= MOVIE GENRES =========================
    elif option == "🎭 Movie Genres":
        if "genres" in df.columns:
            st.header("🎭 All Movie Genres")
            genres = sorted(set("|".join(df["genres"].dropna()).split("|")))
            st.write(genres)
            st.success(f"Total Unique Genres: {len(genres)}")
        else:
            st.warning("No 'genres' column found.")

    # ========================= BAR GRAPH (AUSTRALIA, GERMANY, JAPAN) =========================
    elif option == "🌏 Bar Graph - Australia, Germany, Japan":
        if "country" in df.columns:
            countries = ["Australia", "Germany", "Japan"]
            movie_counts = df["country"].value_counts().reindex(countries, fill_value=0)

            st.header("🎬 Movies Released in Australia, Germany & Japan")
            st.write(movie_counts)

            fig, ax = plt.subplots()
            ax.bar(movie_counts.index, movie_counts.values, color=["#1E90FF", "#32CD32", "#FF6347"])
            ax.set_xlabel("Country")
            ax.set_ylabel("Number of Movies")
            ax.set_title("Movies Released by Country")
            st.pyplot(fig)
        else:
            st.warning("No 'country' column found.")

    # ========================= TOP 5 MOVIES BY BUDGET =========================
    elif option == "💰 Top 5 Movies (Highest Budget)":
        if "budget" in df.columns:
            st.header("💰 Top 5 Movies with Highest Budget")
            top5 = df.nlargest(5, "budget")[["movie_title", "budget", "country", "director_name"]]
            st.table(top5)
        else:
            st.warning("No 'budget' column found.")

    # ========================= MOVIES RELEASED IN 2009 =========================
    elif option == "📅 Movies Released in 2009":
        if "title_year" in df.columns:
            movies_2009 = df[df["title_year"] == 2009]
            st.header("🎞️ Movies Released in 2009")
            st.dataframe(movies_2009)
            st.success(f"Total Movies Released in 2009: {len(movies_2009)}")
        else:
            st.warning("No 'title_year' column found.")

    # ========================= ABOUT US =========================
    elif option == "ℹ️ About Us":
        st.header("👩‍💻 About Us")
        st.image(
            "https://cdn.pixabay.com/photo/2017/08/01/00/55/people-2569234_1280.jpg",
            caption="Team Behind Movie Dashboard",
            use_container_width=True
        )
        st.markdown("""
        ### 🎬 Project: Movie Data Dashboard
        *Developed by:* 🌟 Your Name  
        📧 yourname@email.com
        """)
