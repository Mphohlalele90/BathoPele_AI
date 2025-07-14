import streamlit as st
import pandas as pd
import hashlib
from datetime import datetime, timedelta
import pytz

SA_TIMEZONE = pytz.timezone('Africa/Johannesburg')

# ====== STYLES ======
st.set_page_config(layout="wide", page_title="BathoPele_AI Hospital System")
st.markdown("""
<style>
.stApp { background-color: #f8fcff; }
.header { background: #003366; color: white; padding: 1rem 2rem; border-radius: 0 0 15px 15px; margin-bottom: 2rem;}
.section-title { font-size: 1.2rem; font-weight: 600; margin-bottom: 0.7rem;}
.metric-card { background: white; box-shadow: 0 2px 8px rgba(0,0,0,0.08); padding: 1.1rem 1rem; margin-bottom: 1rem; border-radius: 12px; border-left: 6px solid #003366;}
.sidebar-metric { font-size: 1rem; font-weight: bold; background: #003366; color: white; padding: 0.42rem 1rem; border-radius: 8px; cursor: pointer; margin-bottom: 0.6rem; border: 1px solid #00529b;}
.sidebar-welcome { font-size: 1.1rem; color: #003366; margin-bottom: 1.2rem; font-weight: 700;}
.stButton>button { background: #003366 !important; color: white !important; font-weight: bold; border-radius: 8px; height: 44px; font-size: 1rem;}
.stTextInput>div>input { background: #eaf4ff; }
.stSelectbox>div>div { background: #eaf4ff; }
.stTextArea textarea { background: #eaf4ff; }
hr {margin: 1.4rem 0;}
</style>
""", unsafe_allow_html=True)

# ====== AUTHENTICATION ======
def validate_credentials(username, password):
    credentials = {
        "admin": hashlib.sha256("admin123".encode()).hexdigest(),
        "clerk": hashlib.sha256("clerk123".encode()).hexdigest(),
        "Mpho_Hlalele": "907fbbb4869dc75cb3d3493f580adb2bedbf5da51f5d60465722941a9042fa9c"
    }
    return username in credentials and hashlib.sha256(password.encode()).hexdigest() == credentials[username]

if not st.session_state.get('authenticated'):
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.image("assets/Batho_pele.png", width=120)
    st.title("BathoPele_AI Staff Login")
    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Login")
        if submit:
            if validate_credentials(username, password):
                st.session_state.authenticated = True
                st.session_state.username = username
                st.session_state.page = "dashboard"
                st.rerun()
            else:
                st.error("Invalid credentials. Try again.")
    st.stop()

# ====== DATA ======
if "patients_df" not in st.session_state:
    st.session_state.patients_df = pd.DataFrame(columns=['name', 'doc_number', 'doc_type', 'nationality', 'result', 'legal_status', 'timestamp'])
if "visits_df" not in st.session_state:
    st.session_state.visits_df = pd.DataFrame(columns=['patient_name', 'visit_date', 'diagnosis', 'treatment', 'cost', 'hospital', 'ward'])
if "resources_df" not in st.session_state:
    st.session_state.resources_df = pd.DataFrame([
        {"hospital": "BathoPele_AI", "ward": "Trauma", "total_beds": 10, "available_beds": 8, "medications": "Antibiotics", "medication_stock": 500, "doctors": "Dr Gule,Dr Moreki", "nurses": "Nurse Gugu"},
        {"hospital": "BathoPele_AI", "ward": "Maternity", "total_beds": 18, "available_beds": 15, "medications": "Painkillers", "medication_stock": 320, "doctors": "Dr Moreki", "nurses": "Nurse Gugu"}
    ])
patients_df = st.session_state.patients_df
visits_df = st.session_state.visits_df
resources_df = st.session_state.resources_df

if "page" not in st.session_state:
    st.session_state.page = "dashboard"
if "show_treatment_form" not in st.session_state:
    st.session_state.show_treatment_form = False
if "show_actions" not in st.session_state:
    st.session_state.show_actions = False

# ====== SIDEBAR ======
with st.sidebar:
    st.image("assets/Batho_pele.png", width=90)
    st.markdown(f'<div class="sidebar-welcome">Welcome {st.session_state.get("username", "")}</div>', unsafe_allow_html=True)
    st.divider()
    if st.button("🏠 Dashboard"):
        st.session_state.page = "dashboard"
        st.rerun()
    if st.button("📋 Patient Intake"):
        st.session_state.page = "patient_intake"
        st.rerun()
    if st.button("👥 Patient Search"):
        st.session_state.page = "patient_search"
        st.rerun()
    if st.button("🏥 Resource Monitoring"):
        st.session_state.page = "resource_monitoring"
        st.rerun()
    st.divider()
    # Sidebar metrics
    sa_patients = len(patients_df[patients_df['nationality'] == 'South African'])
    foreign_patients = len(patients_df[patients_df['nationality'] != 'South African'])
    needs_referral = len(patients_df[patients_df['legal_status'] == 'Pending'])
    st.markdown(f'<div class="sidebar-metric">SA Patients: {sa_patients}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="sidebar-metric">Foreign Nationals: {foreign_patients}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="sidebar-metric">Needs Referral: {needs_referral}</div>', unsafe_allow_html=True)
    st.divider()
    # Resource metrics
    for ward in resources_df['ward'].unique():
        ward_data = resources_df[resources_df['ward'] == ward].iloc[0]
        st.markdown(f'<div class="section-title">{ward} Section</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="sidebar-metric">Beds Available: {ward_data["available_beds"]}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="sidebar-metric">Doctors: {ward_data["doctors"]}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="sidebar-metric">Nurses: {ward_data["nurses"]}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="sidebar-metric">Medication {ward_data["medications"]}: {ward_data["medication_stock"]}</div>', unsafe_allow_html=True)
    st.divider()
    if st.button("Logout"):
        st.session_state.authenticated = False
        st.rerun()

# ====== DASHBOARD ======
def dashboard_ui():
    st.markdown('<div class="header"><h1>🏥 BathoPele_AI Hospital Dashboard</h1></div>', unsafe_allow_html=True)
    today_str = datetime.now(SA_TIMEZONE).strftime('%Y-%m-%d')
    visits_today = len(visits_df[visits_df['visit_date'] == today_str])
    sa_patients = len(patients_df[patients_df['nationality'] == 'South African'])
    foreign_patients = len(patients_df[patients_df['nationality'] != 'South African'])
    needs_referral = len(patients_df[patients_df['legal_status'] == 'Pending'])
    st.markdown('<div class="section-title">Patient Metrics</div>', unsafe_allow_html=True)
    dash_cols = st.columns(4)
    if dash_cols[0].button("Visits Today"):
        st.session_state.page = "patient_search"
        st.rerun()
    dash_cols[0].markdown(f'<div class="metric-card">{visits_today}</div>', unsafe_allow_html=True)
    if dash_cols[1].button("SA Patients"):
        st.session_state.page = "patient_intake"
        st.rerun()
    dash_cols[1].markdown(f'<div class="metric-card">{sa_patients}</div>', unsafe_allow_html=True)
    if dash_cols[2].button("Foreign Nationals"):
        st.session_state.page = "patient_intake"
        st.rerun()
    dash_cols[2].markdown(f'<div class="metric-card">{foreign_patients}</div>', unsafe_allow_html=True)
    if dash_cols[3].button("Needs Referral"):
        st.session_state.page = "patient_intake"
        st.rerun()
    dash_cols[3].markdown(f'<div class="metric-card">{needs_referral}</div>', unsafe_allow_html=True)
    st.markdown('<hr>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Resource Daily Metrics</div>', unsafe_allow_html=True)
    rcols = st.columns(len(resources_df['ward'].unique()))
    for i, ward in enumerate(resources_df['ward'].unique()):
        ward_data = resources_df[resources_df['ward'] == ward].iloc[0]
        rcols[i].markdown(f'<div class="metric-card">{ward} Section<br>Beds Available: {ward_data["available_beds"]}<br>Doctors: {ward_data["doctors"]}<br>Nurses: {ward_data["nurses"]}<br>Medication {ward_data["medications"]}: {ward_data["medication_stock"]}</div>', unsafe_allow_html=True)

# ====== PATIENT INTAKE ======
def intake_ui():
    st.markdown('<div class="header"><h1>📋 Patient Intake</h1></div>', unsafe_allow_html=True)
    treatment_plans = {
        "Hypertension": {
            "plan": "Lifestyle changes and medication",
            "medications": [
                {"name": "Amlodipine", "dosage": "5-10 mg", "frequency": "Once daily"},
                {"name": "Hydrochlorothiazide", "dosage": "12.5-25 mg", "frequency": "Once daily"},
            ],
            "costs": {"SA Residents": 0, "Legal Immigrants": 350, "Illegal Immigrants": 800}
        },
        "Type 2 Diabetes": {
            "plan": "Diet and medication",
            "medications": [
                {"name": "Metformin", "dosage": "500-1000 mg", "frequency": "Twice daily"},
            ],
            "costs": {"SA Residents": 0, "Legal Immigrants": 510, "Illegal Immigrants": 1150}
        }
    }
    with st.expander("📋 Patient Information", expanded=True):
        with st.form("patient_intake_form"):
            cols = st.columns(2)
            name = cols[0].text_input("Full Name*", placeholder="First Last")
            nationality = cols[0].selectbox("Nationality*", ["South African", "Zimbabwean", "Malawian", "Mozambican", "Other"])
            doc_number = cols[0].text_input("Document Number*", placeholder="ID/Passport Number")
            dob_col = cols[1]
            dob_col.markdown("Date of Birth*")
            dob_known = dob_col.checkbox("Known DOB", value=True, key="dob_known")
            if dob_known:
                dob = dob_col.date_input("Date of Birth", min_value=datetime(1900,1,1), max_value=datetime.now(), label_visibility="collapsed")
            else:
                dob_col.markdown("Using estimated age (DOB unknown)")
                age = dob_col.number_input("Estimated Age", min_value=0, max_value=120, value=30)
                dob = (datetime.now() - timedelta(days=age*365)).date()
            doc_type = cols[1].selectbox("Document Type*", ["RSA ID", "Passport", "Asylum Seeker Permit"])
            medical_aid = cols[1].text_input("Medical Aid Number (if applicable)", placeholder="Leave blank if none")
            conditions = st.text_area("Known Medical Conditions", placeholder="List any known conditions")
            submitted = st.form_submit_button("Submit Patient Information")
        if submitted:
            if not name or not doc_number:
                st.error("Fill required fields!")
            else:
                verification_result = {
                    'result': 'Valid',
                    'legal_status': 'Valid',
                    'details': 'Verification successful for SA Citizen.'
                }
                if (doc_type == 'RSA ID' and nationality != 'South African') or (doc_type == 'Passport' and nationality == 'South African'):
                    verification_result['result'] = 'Needs Verification'
                    verification_result['legal_status'] = 'Pending'
                    verification_result['details'] = 'Needs referral to Home Affairs.'
                patient_data = {
                    "name": name,
                    "dob": dob.strftime('%Y-%m-%d') if dob_known else f"Estimated age: {age}",
                    "nationality": nationality,
                    "doc_type": doc_type,
                    "doc_number": doc_number,
                    "medical_aid": medical_aid if medical_aid else "None",
                    "conditions": conditions if conditions else "None reported",
                    "timestamp": datetime.now(SA_TIMEZONE).strftime('%Y-%m-%d %H:%M:%S'),
                    **verification_result
                }
                patients_df.loc[len(patients_df)] = [
                    patient_data['name'],
                    patient_data['doc_number'],
                    patient_data['doc_type'],
                    patient_data['nationality'],
                    patient_data['result'],
                    patient_data['legal_status'],
                    patient_data['timestamp']
                ]
                st.session_state.last_patient = patient_data
                st.success("Patient record created!")
                st.info(patient_data['details'])
                st.session_state.show_treatment_form = True
    if st.session_state.get('show_treatment_form', False) and 'last_patient' in st.session_state:
        patient = st.session_state.last_patient
        with st.expander("🩺 Treatment Information", expanded=True):
            diagnosis_options = list(treatment_plans.keys()) + ["Other"]
            diagnosis = st.selectbox("Diagnosis*", diagnosis_options, key="diagnosis_select")
            meds = []
            if diagnosis != "Other" and diagnosis in treatment_plans:
                treatment_plan = treatment_plans[diagnosis]["plan"]
                cost = (
                    treatment_plans[diagnosis]["costs"]["SA Residents"]
                    if patient['nationality'] == 'South African'
                    else treatment_plans[diagnosis]["costs"]["Legal Immigrants"]
                    if patient['legal_status'] == 'Valid'
                    else treatment_plans[diagnosis]["costs"]["Illegal Immigrants"]
                )
                st.text_area("Treatment Plan*", value=treatment_plan, key="treatment_plan_area", disabled=True)
                st.write("### Prescribed Medications")
                meds = treatment_plans[diagnosis]["medications"]
                for med in meds:
                    st.markdown(f"- **{med['name']}**: {med['dosage']} {med['frequency']}")
                dr_comment = st.text_area("Doctor Comments (editable)", value=f"Standard protocol for {diagnosis}.")
            else:
                treatment_plan = st.text_area("Treatment Plan*")
                cost = st.number_input("Treatment Cost (R)*", min_value=0, value=1500)
                dr_comment = st.text_area("Doctor Comments (editable)", value="")
            if st.button("Submit Treatment Details"):
                if not diagnosis or not treatment_plan:
                    st.error("Fill required diagnosis and treatment!")
                else:
                    visit_data = {
                        "patient_name": patient['name'],
                        "diagnosis": diagnosis,
                        "treatment": treatment_plan,
                        "medication": ", ".join([f"{med['name']} {med['dosage']} {med['frequency']}" for med in meds]) if diagnosis != "Other" and diagnosis in treatment_plans else "",
                        "cost": cost,
                        "notes": dr_comment,
                        "hospital": "BathoPele_AI",
                        "ward": "Trauma",
                        "visit_date": datetime.now(SA_TIMEZONE).strftime('%Y-%m-%d'),
                        "timestamp": datetime.now(SA_TIMEZONE).strftime('%Y-%m-%d %H:%M:%S')
                    }
                    visits_df.loc[len(visits_df)] = [
                        visit_data['patient_name'],
                        visit_data['visit_date'],
                        visit_data['diagnosis'],
                        visit_data['treatment'],
                        visit_data['cost'],
                        visit_data['hospital'],
                        visit_data['ward']
                    ]
                    st.success("Treatment saved!")
                    st.session_state.treatment_details = visit_data
                    st.session_state.show_actions = True
    if st.session_state.get('show_actions', False):
        st.markdown("---")
        st.subheader("Patient Actions")
        action_cols = st.columns(3)
        patient = st.session_state.last_patient
        treatment = st.session_state.treatment_details
        if action_cols[0].button("📄 Generate Invoice"):
            with st.expander("🧾 Invoice", expanded=True):
                st.subheader(f"Invoice for {patient['name']}")
                st.write(f"**Date:** {datetime.now(SA_TIMEZONE).strftime('%Y-%m-%d')}")
                st.write(f"**Patient:** {patient['name']} ({patient['nationality']})")
                st.write(f"**Document:** {patient['doc_type']} {patient['doc_number']}")
                st.write(f"**Diagnosis:** {treatment['diagnosis']}")
                st.write(f"**Treatment:** {treatment['treatment']}")
                if treatment['medication']:
                    st.write(f"**Medication:** {treatment['medication']}")
                st.write(f"**Total Cost:** R{treatment['cost']:,.2f}")
                invoice_text = f"""
                BATHO PELE HEALTHCARE INITIATIVE
                ---------------------------------
                Invoice Date: {datetime.now(SA_TIMEZONE).strftime('%Y-%m-%d')}
                Patient: {patient['name']}
                ID: {patient['doc_number']}
                ---------------------------------
                Diagnosis: {treatment['diagnosis']}
                Treatment: {treatment['treatment']}
                Medication: {treatment['medication']}
                ---------------------------------
                TOTAL COST: R{treatment['cost']:,.2f}
                """
                st.download_button(
                    label="Download Invoice",
                    data=invoice_text,
                    file_name=f"invoice_{patient['name']}_{datetime.now(SA_TIMEZONE).strftime('%Y%m%d')}.txt",
                    mime="text/plain"
                )
        if patient.get('legal_status') == 'Pending':
            if action_cols[1].button("⚠️ Refer to Home Affairs"):
                st.success(f"Patient {patient['name']} referred to Home Affairs")
        if action_cols[2].button("👤 View Full Record"):
            with st.expander("Patient Record Summary", expanded=True):
                st.write(f"**Name:** {patient['name']}")
                st.write(f"**DOB:** {patient['dob']}")
                st.write(f"**Nationality:** {patient['nationality']}")
                st.write(f"**Status:** {patient.get('legal_status', 'Valid')}")
                st.write(f"**Conditions:** {patient['conditions']}")
                st.write("---")
                st.write(f"**Last Treatment:** {treatment['diagnosis']}")
                st.write(f"**Medication:** {treatment['medication']}")
                st.write(f"**Cost:** R{treatment['cost']:,.2f}")
                st.write(f"**Last Updated:** {treatment['timestamp']}")

# ====== PATIENT SEARCH ======
def search_ui():
    st.markdown('<div class="header"><h1>👥 Patient Search</h1></div>', unsafe_allow_html=True)
    search_cols = st.columns(3)
    name_search = search_cols[0].text_input("Name")
    id_search = search_cols[1].text_input("ID/Passport Number")
    nationality_filter = search_cols[2].selectbox("Nationality", ["All"] + list(patients_df['nationality'].dropna().unique()))
    filtered_patients = patients_df.copy()
    if name_search:
        filtered_patients = filtered_patients[
            filtered_patients['name'].notna() & 
            filtered_patients['name'].str.contains(name_search, case=False, na=False)
        ]
    if id_search:
        filtered_patients = filtered_patients[
            filtered_patients['doc_number'].notna() & 
            filtered_patients['doc_number'].str.contains(id_search, case=False, na=False)
        ]
    if nationality_filter != "All":
        filtered_patients = filtered_patients[filtered_patients['nationality'] == nationality_filter]
    if not filtered_patients.empty:
        st.subheader(f"Found {len(filtered_patients)} patients")
        show_cols = ['name', 'nationality', 'doc_type', 'doc_number', 'legal_status', 'timestamp']
        st.dataframe(
            filtered_patients[show_cols].rename(columns={
                'name': 'Name',
                'nationality': 'Nationality',
                'doc_type': 'Document Type',
                'doc_number': 'Document Number',
                'legal_status': 'Status',
                'timestamp': 'Last Updated'
            }),
            use_container_width=True,
            hide_index=True
        )
        selected_patient = st.selectbox("Select patient to view history", filtered_patients['name'].unique())
        patient_visits = visits_df[visits_df['patient_name'] == selected_patient]
        if not patient_visits.empty:
            st.subheader(f"Visit History for {selected_patient}")
            st.dataframe(
                patient_visits[['visit_date', 'diagnosis', 'treatment', 'cost']].rename(columns={
                    'visit_date': 'Date',
                    'diagnosis': 'Diagnosis',
                    'treatment': 'Treatment',
                    'cost': 'Cost (R)'
                }),
                use_container_width=True
            )
    else:
        st.info("No patients found matching your criteria")

# ====== RESOURCE MONITORING ======
def resource_ui():
    st.markdown('<div class="header"><h1>🏥 Resource Monitoring</h1></div>', unsafe_allow_html=True)
    st.subheader("Hospital Resources by Ward")
    for ward in resources_df['ward'].unique():
        ward_data = resources_df[resources_df['ward'] == ward].iloc[0]
        st.markdown(f"### {ward} Section")
        cols = st.columns(4)
        cols[0].metric("Beds Available", f"{ward_data['available_beds']}/{ward_data['total_beds']}")
        cols[1].markdown(f"**Doctors:**<br>{ward_data['doctors']}", unsafe_allow_html=True)
        cols[2].markdown(f"**Nurses:**<br>{ward_data['nurses']}", unsafe_allow_html=True)
        cols[3].markdown(f"**Medication:**<br>{ward_data['medications']}<br>Stock: {ward_data['medication_stock']}", unsafe_allow_html=True)

# ====== FOOTER ======
def footer_ui():
    st.markdown("---")
    footer = f"""
    <div style="text-align: center; padding: 20px; background-color: #f0f8ff; border-radius: 5px;">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <div>
                <p style="font-size: 14px; color: #003366;">© 2025 Batho Pele Initiative | National Department of Health</p>
            </div>
            <div>
                <p style="font-size: 12px; color: #666;">System Status: <span style="color: green;">● Operational</span></p>
                <p style="font-size: 12px; color: #666;">Last Updated: {datetime.now(SA_TIMEZONE).strftime('%Y-%m-%d %H:%M:%S')}</p>
            </div>
        </div>
        <div style="margin-top: 10px;">
            <p style="font-size: 12px; color: #666;">For support, contact: <a href="mailto:support@bathopele.gov.za">support@bathopele.gov.za</a></p>
        </div>
    </div>
    """
    st.markdown(footer, unsafe_allow_html=True)

# ====== MAIN ROUTING ======
if st.session_state.page == "dashboard":
    dashboard_ui()
elif st.session_state.page == "patient_intake":
    intake_ui()
elif st.session_state.page == "patient_search":
    search_ui()
elif st.session_state.page == "resource_monitoring":
    resource_ui()
footer_ui()