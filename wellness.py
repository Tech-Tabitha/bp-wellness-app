# ---------------------- IMPORTS & LOGIN SETUP ----------------------
import streamlit as st
import datetime
import pandas as pd
import plotly.express as px
from firebase_auth import login_user, create_account, save_user_data
from fpdf import FPDF

# ---------------------- USER SESSION & LOGIN ----------------------
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "user_email" not in st.session_state:
    st.session_state.user_email = None
if "user" not in st.session_state:
    st.session_state.user = None

if "is_guest" not in st.session_state:
    st.session_state.is_guest = False

st.set_page_config(page_title="Wellness Hub", page_icon="🩺", layout="centered")

if not st.session_state.authenticated:
    st.title("🔐 Login to Your Wellness Tracker")

    email_input = st.text_input("Email")
    password_input = st.text_input("Password", type="password")

    col1, col2, col3 = st.columns([1, 1, 1])

    with col1:
        if st.button("Login or Create Account"):
            user = login_user(email_input, password_input)
            if user:
                st.session_state.authenticated = True
                st.session_state.user_email = email_input
                st.session_state.user = user
                st.success("✅ Logged in successfully!")
                st.rerun()
            else:
                user = create_account(email_input, password_input)
                if user:
                    st.session_state.authenticated = True
                    st.session_state.user_email = email_input
                    st.success("✅ Account created and logged in!")
                    st.rerun()
                else:
                    st.error("⚠️ Login failed and account already exists or password is weak.")

    with col2:
        if st.button("Continue as Guest"):
            st.session_state.authenticated = True
            st.session_state.is_guest = True
            st.session_state.user_email = "guest_user"
            st.info("👤 Continuing as Guest...")
            st.rerun()

    st.stop()

# ---------------------- LANGUAGE, THEME, & TABS ----------------------
lang_options = {
    "English": "en",
    "Yoruba": "yo",
    "Hausa": "ha",
    "Igbo": "ig"
}

st.sidebar.markdown("## 🌐 Language")
selected_lang = st.sidebar.selectbox("Choose your language:", list(lang_options.keys()))
lang_code = lang_options[selected_lang]

st.sidebar.markdown("## 🎨 Theme")
theme = st.sidebar.radio("Choose Theme:", ["Light", "Dark"])
if theme == "Dark":
    st.markdown("""
        <style>
            .stApp {
                background-color: #0e1117;
                color: #ffffff;
            }
            .block-container {
                background-color: #1e1e2f;
                border-radius: 12px;
                box-shadow: 0 0 20px rgba(255, 255, 255, 0.1);
            }
        </style>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
        <style>
            .stApp {
                background-color: #ffe6f0;
                color: #000000;
            }
        </style>
    """, unsafe_allow_html=True)

# ---------------------- APP HEADER ----------------------
st.markdown("""
    <h1 style='text-align: center;'>💉 Dorcas Wellness App</h1>
    <h3 style='text-align: center;'>Welcome to your health companion!</h3>
""", unsafe_allow_html=True)

# ---------------------- LOGOUT BUTTON ----------------------
if st.sidebar.button("🚪 Logout"):
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()

# ---------------------- Daily Health Tip ----------------------
health_tips = {
    "en": ["Stay hydrated!", "Walk 30 mins daily.", "Sleep well!", "Reduce salt intake."],
    "yo": ["Maa mu omi to!", "Rin fun iṣẹju 30 lojoojumọ.", "Sun to!", "Din iye iyọ rẹ ku."],
    "ha": ["Sha ruwa sosai!", "Yi yawo na mintuna 30 a rana.", "Yi bacci lafiya!", "Rage amfani da gishiri."],
    "ig": ["Na-aṅụ mmiri!", "Na-eje ije nkeji iri atọ kwa ụbọchị.", "Na-ehi ụra nke ọma!", "Belata nnu i ji nri."]
}
index = datetime.datetime.now().day % len(health_tips[lang_code])
st.sidebar.success(f"💡 {health_tips[lang_code][index]}")

email = st.session_state.user_email

# ---------------------- Additional Suggestions Placeholder ----------------------
st.sidebar.markdown("---")
st.sidebar.markdown("### 🔔 Next Suggestions")
st.sidebar.markdown("- 📥 Download PDF Report")
st.sidebar.markdown("- 📅 View Calendar History")
st.sidebar.markdown("- 🧘‍♀️ Fitness Advice")
st.sidebar.markdown("- 💊 Track Medications")
st.sidebar.markdown("- 🧠 Symptom Risk Detector")
st.sidebar.markdown("- 🌐 Join Leaderboard")
st.sidebar.markdown("---")

# ---------------------- Tabs Setup ----------------------
t = {
    "check_bp": {"en": "Check Blood Pressure", "yo": "Ṣayẹwo Ẹjẹ", "ha": "Duba Matsi", "ig": "Le BP anya"},
    "bmi_calc": {"en": "BMI Calculator", "yo": "Isiro Iwuwo", "ha": "Lissafin BMI", "ig": "Ngụkọta BMI"},
    "quiz": {"en": "Health Quiz", "yo": "Idanwo Ilera", "ha": "Tambayoyin Lafiya", "ig": "Ajụjụ Ahụ Ike"},
    "mood": {"en": "Mood & Symptoms", "yo": "Ipo Inu & Aami", "ha": "Yanayi da Alamomi", "ig": "Okwu Obi na Ihe Ngosipụta"},
    "chart": {"en": "Pie Chart", "yo": "Atẹjade Pie", "ha": "Zane-zane na Pie", "ig": "Ụdị Pie"}
}

# ---------------------- Tabs ----------------------
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    f"📊 {t['check_bp'][lang_code]}",
    f"⚖️ {t['bmi_calc'][lang_code]}",
    f"📝 {t['quiz'][lang_code]}",
    f"😊 {t['mood'][lang_code]}",
    f"📈 {t['chart'][lang_code]}"
])

# ---------------------- Blood Pressure Checker ----------------------
with tab1:
    st.subheader(t['check_bp'][lang_code])
    systolic = st.number_input("Systolic (Upper)", min_value=50, max_value=250)
    diastolic = st.number_input("Diastolic (Lower)", min_value=30, max_value=150)
    if st.button("Submit BP"):
        category = "Low" if systolic < 90 or diastolic < 60 else "Normal" if systolic <= 120 and diastolic <= 80 else "Elevated" if systolic <= 139 or diastolic <= 89 else "High"
        bp_data = {"Systolic": systolic, "Diastolic": diastolic, "Status": category}
        st.session_state.setdefault("bp_history", []).append(bp_data)
        if not st.session_state.is_guest:
            save_user_data(email, "bp_history", bp_data, st.session_state.user)
        st.success(f"🩺 BP Status: {category}")

# ---------------------- BMI Calculator ----------------------
with tab2:
    st.subheader(t['bmi_calc'][lang_code])
    weight = st.number_input("Weight (kg)", min_value=10.0, max_value=300.0)
    height = st.number_input("Height (cm)", min_value=50.0, max_value=250.0)
    if st.button("Calculate BMI"):
        if height > 0:
            bmi = weight / ((height / 100) ** 2)
            category = "Underweight" if bmi < 18.5 else "Normal" if bmi < 24.9 else "Overweight" if bmi < 29.9 else "Obese"
            st.session_state.setdefault("bmi_history", []).append({"BMI": bmi, "Category": category})
            if not st.session_state.is_guest:
                save_user_data(email, "bmi_history", {"bmi": bmi, "category": category}, st.session_state.user)
            st.success(f"BMI: {bmi:.2f} — {category}")

# ---------------------- Health Quiz ----------------------
with tab3:
    st.subheader(t['quiz'][lang_code])
    score = 0
    if st.radio("1. How much water should you drink daily?", ["1 glass", "2 liters", "5 liters"], key="q1") == "2 liters":
        score += 1
    if st.radio("2. Which nutrient is essential for muscle growth?", ["Carbohydrate", "Protein", "Fat"], key="q2") == "Protein":
        score += 1
    if st.radio("3. What is a healthy blood pressure range?", ["90/60 to 120/80", "140/90", "160/100"], key="q3") == "90/60 to 120/80":
        score += 1
    if st.button("Submit Quiz"):
        st.success(f"You scored {score}/3.")

# ---------------------- Mood & Symptoms Tracker ----------------------
with tab4:
    st.subheader(t['mood'][lang_code])
    mood = st.selectbox("How do you feel today?", ["Happy", "Sad", "Tired", "Energetic", "Anxious"])
    symptoms = st.multiselect("Any symptoms?", ["Headache", "Fever", "Cough", "Sore throat", "Fatigue"])
    if st.button("Save Mood & Symptoms"):
        entry = {"Mood": mood, "Symptoms": symptoms, "Time": str(datetime.datetime.now())}
        st.session_state.setdefault("mood_history", []).append(entry)
        if not st.session_state.is_guest:
            save_user_data(email, "mood_history", entry, st.session_state.user)
        st.success("✅ Mood and symptoms saved!")

# ---------------------- Pie Chart for Health Categories ----------------------
with tab5:
    st.subheader(t['chart'][lang_code])
    data = []
    if "bp_history" in st.session_state:
        data += [item["Status"] for item in st.session_state["bp_history"]]
    if "bmi_history" in st.session_state:
        data += [item["Category"] for item in st.session_state["bmi_history"]]
    if "mood_history" in st.session_state:
        data += [item["Mood"] for item in st.session_state["mood_history"]]
    if data:
        df = pd.DataFrame(data, columns=["Category"])
        fig = px.pie(df, names="Category", title="Health Overview Pie Chart", color_discrete_sequence=px.colors.sequential.RdPu)
        st.plotly_chart(fig)
    else:
        st.info("No data available to display.")

# Safe placeholder content for PDF (avoids crash)
sample_pdf_bytes = b"%PDF-1.4\n%PLACEHOLDER PDF\n%%EOF"

st.sidebar.download_button("⬇️ Download Report (PDF)", data=sample_pdf_bytes, file_name="wellness_report.pdf")

# Placeholder sections for implementation

# ---------------------- 📅 Calendar View ----------------------
with st.expander("📅 Calendar View"):
    st.write("View your BP and BMI history by date:")

    # Combine history by date
    bp_data = st.session_state.get("bp_history", [])
    bmi_data = st.session_state.get("bmi_history", [])

    records = []
    today = datetime.date.today()

    for i in range(len(bp_data)):
        date = today - datetime.timedelta(days=(len(bp_data) - 1 - i))
        bp = f"{bp_data[i]['Systolic']}/{bp_data[i]['Diastolic']} ({bp_data[i]['Status']})" if i < len(bp_data) else ""
        bmi = f"{bmi_data[i]['BMI']:.2f} ({bmi_data[i]['Category']})" if i < len(bmi_data) else ""
        records.append({"Date": date.strftime("%Y-%m-%d"), "Blood Pressure": bp, "BMI": bmi})

    if records:
        calendar_df = pd.DataFrame(records)
        st.dataframe(calendar_df)
    else:
        st.info("No history available yet. Submit some BP or BMI data.")


# ---------------------- 🧠 Symptom Checker ----------------------
with st.expander("🧠 Symptom Checker"):
    st.write("Log how you feel and see if there are patterns.")
    mood = st.selectbox("How do you feel today?", ["🙂 Good", "😐 Okay", "😟 Unwell", "😢 Very bad"])
    symptoms = st.multiselect("Select any symptoms you're experiencing:", [
        "Headache", "Fatigue", "Chest Pain", "Dizziness", "Shortness of Breath", "Nausea"
    ])
    if st.button("Check Severity"):
        if "Chest Pain" in symptoms or "Shortness of Breath" in symptoms:
            st.error("⚠️ High Risk: Seek medical attention.")
        elif symptoms:
            st.warning("🟡 Mild symptoms logged. Monitor and rest.")
        else:
            st.success("✅ You're doing well!")

# ---------------------- 💊 Medication Log ----------------------
with st.expander("💊 Medication Log"):
    st.write("Keep track of medications you're taking.")
    med_name = st.text_input("Medication Name")
    med_time = st.time_input("Time Taken", value=datetime.time(8, 0))
    med_date = st.date_input("Date Taken", value=datetime.date.today())
    if st.button("Log Medication"):
        med_entry = {
            "Name": med_name,
            "Date": str(med_date),
            "Time": str(med_time)
        }
        st.session_state.setdefault("medications", []).append(med_entry)
        if not st.session_state.is_guest:
           save_user_data(email, "medications", med_entry, st.session_state.user)
        st.success(f"💊 {med_name} logged for {med_date} at {med_time}.")


# ---------------------- 📄 Generate PDF Report ----------------------
with st.expander("📄 Download Health Report"):
    class PDF(FPDF):
        def header(self):
            self.set_font("Arial", "B", 12)
            self.cell(0, 10, "Wellness Report", ln=True, align="C")

        def footer(self):
            self.set_y(-15)
            self.set_font("Arial", "I", 8)
            self.cell(0, 10, f"Page {self.page_no()}", align="C")

        def add_report(self, name, bp_list, bmi_list):
            self.set_font("Arial", "", 12)
            self.cell(0, 10, f"Email: {name}", ln=True)
            self.ln(5)
            self.set_font("Arial", "B", 12)
            self.cell(0, 10, "Blood Pressure History:", ln=True)
            self.set_font("Arial", "", 11)
            for bp in bp_list:
                self.cell(0, 10, f"- {bp}", ln=True)

            self.ln(5)
            self.set_font("Arial", "B", 12)
            self.cell(0, 10, "BMI History:", ln=True)
            self.set_font("Arial", "", 11)
            for bmi in bmi_list:
                self.cell(0, 10, f"- {bmi}", ln=True)

    if st.button("📤 Generate & Download PDF"):
        pdf = PDF()
        pdf.add_page()
        bp_list = [f"{bp['Systolic']}/{bp['Diastolic']} - {bp['Status']}" for bp in st.session_state.get("bp_history", [])]
        bmi_list = [f"{b['BMI']:.2f} - {b['Category']}" for b in st.session_state.get("bmi_history", [])]
        pdf.add_report(email, bp_list, bmi_list)
        pdf_output = pdf.output(dest="S").encode("latin1")
        st.download_button("⬇️ Download Your Report", data=pdf_output, file_name="wellness_summary.pdf")
