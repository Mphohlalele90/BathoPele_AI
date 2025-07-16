# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import streamlit as st
import pandas as pd
import hashlib
from datetime import datetime, timedelta
import pytz
import random

SA_TIMEZONE = pytz.timezone('Africa/Johannesburg')
TODAY = datetime.now(SA_TIMEZONE).strftime("%Y-%m-%d")

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

def staff_list():
    wards = [
        ("Medical Ward", "Dr N Dwarka", "Nurse Thembi Molekwa"),
        ("Surgical Ward", "Dr GO Matlaga", "Nurse Yvette Hendricks"),
        ("Maternity Ward", "Dr BB Mbambela", "Nurse Jabu Ntuli"),
        ("ICU", "Dr KF Kleinhans", "Nurse Sipho Radebe"),
        ("Emergency Unit", "Dr M Gule", "Nurse Lindiwe Nkosi"),
        ("Pediatric Ward", "Dr TS Moreki", "Nurse Katlego Mahlangu"),
    ]
    staff = []
    firstnames = [
        "Zanele","Lerato","Ahmed","David","Keitumetse","Naledi","Siphesihle","Farhana","Kabelo","Ridwaan","Thabang",
        "Ntombi","Ayanda","Peter","Priya","Tumelo","Vivian","Moeketsi","Mmabatho","Imran","Charity","Thato","Zukiswa",
        "Mapaseka","Rahim","Nomvula","Tshepo","Michael","Ziyaad","Nobuhle","Odirile","Julia","Craig","Karabo","Vuyani",
        "Naledi","Kabelo","Tumi","Yusuf","Sibusiso","Nokwanda","Yanga","Felix","Bontle","Lindokuhle","Reitumetse",
        "Pumza","Ahmed","Banele","Neo","Leruo","Vanessa","Mandla","Anathi"
    ]
    surnames = [
        "Mkhize","Moeketsi","Ismail","Mokoena","Phiri","Lebelo","Zuma","Essop","Ncube","Patel","Lephoko","Ngobese",
        "Khumalo","Madzinga","Reddy","Seboko","Nyathi","Mashilo","Maleka","Osman","Ramohapi","Mahlangu","Maqubela",
        "Mphahlele","Akbar","Sithebe","Kekana","Ntuli","Omar","Sibanda","Lekaota","Mohlomi","Petersen","Baloyi",
        "Mzimela","Molefe","Mohale","Mangera","Ngcobo","Cele","Mdletshe","Mahlangu","Tlhapi","Mbatha","Mfenyana",
        "Moosa","Xulu","Sibeko","Maake","Pillay","Zungu","Moyo"
    ]
    nurse_first = [
        "Andile","Grace","Mpho","Precious","Jeanette","Koketso","Linda","Thuli","Mary","Palesa","Connie","Dineo",
        "Lebohang","Karabo","Mavis","Reshoketswe","Nokuthula","Nandi","Lillian","Tshidi","Teboho","Portia","Khumo",
        "Rethabile","Zandile","Prudence","Sithole","Ndlovu","Sekoati","Dlamini","Seakamela","Madikizela","Govender",
        "Mofokeng","Ramoroka","Motsoeneng","Morake","Mosothoane","Moloi","Selepe","Mokwena","Modiba","Majozi",
        "Maseko"
    ]
    nurse_surnames = [
        "Sithole","Ndlovu","Sekoati","Dlamini","Seakamela","Madikizela","Govender","Mofokeng","Ramoroka","Motsoeneng",
        "Morake","Mosothoane","Moloi","Selepe","Mokwena","Modiba","Majozi","Maseko","Maponya","Kgosi","Rametsi",
        "Motlhabane","Modise","Moiloa","Nkuna","Nene","Mokgotsi","Masinga","Letsoalo","Chirwa","Kgokong","Mabe",
        "Ntshangase","Mhlongo","Mohale","Sibiya","Motsoeneng","Morake","Mosothoane","Moloi","Selepe","Mokwena",
        "Modiba","Majozi","Maseko"
    ]
    for ward, first_doc, first_nurse in wards:
        staff.append({"name": first_doc, "type": "Doctor", "department": ward})
        for i in range(9):
            staff.append({
                "name": f"Dr {random.choice(firstnames)} {random.choice(surnames)}",
                "type": "Doctor",
                "department": ward
            })
        staff.append({"name": first_nurse, "type": "Nurse", "department": ward})
        for i in range(59):
            staff.append({
                "name": f"Nurse {random.choice(nurse_first)} {random.choice(nurse_surnames)}",
                "type": "Nurse",
                "department": ward
            })
    return staff

def random_patient(pid):
    # Mixture of SA, Foreign, Illegal, with docs and legal status
    names = ["Thabo", "Ayesha", "Maria", "Jean-Paul", "Sibongile", "Chipo", "Ahmed", "Fatima", "Peter", "Linda", "Nomsa", "Sipho", "Anna", "Blessing", "Zanele", "Samuel", "Musa", "Grace", "John", "Nadia"]
    surnames = ["Radebe", "Khan", "Gonzalez", "Mbatha", "Mokoena", "Chirwa", "Sibanda", "Patel", "Smith", "Dlamini", "Ndlovu", "Ntuli", "Brown", "Molefe", "Mthembu", "Mugabe", "Moyo", "Naidoo", "Botha", "Nkosi"]
    diags = [
        "Severe Malaria", "Tuberculosis (Pulmonary)", "Labor & Delivery (Complicated)", "Appendicitis", "Stroke (Ischemic)",
        "Hypertension", "Type 2 Diabetes", "Asthma", "Eclampsia", "Severe Pneumonia",
        "Common Infections", "Mental Health", "Diabetic Ketoacidosis (DKA)", "Meningitis (Bacterial)"
    ]
    wards = ["Emergency Unit", "Medical Ward", "Maternity Ward", "Surgical Ward", "ICU", "Pediatric Ward"]
    name = f"{random.choice(names)} {random.choice(surnames)}"
    diag = random.choice(diags)
    ward = random.choice(wards)
    admit_days_ago = random.randint(0, 59)
    admission_date = (datetime.now(SA_TIMEZONE) - timedelta(days=admit_days_ago)).strftime("%Y-%m-%d")
    # Mixture logic
    pat_type = random.choices(['SA', 'Foreign', 'Illegal'], weights=[0.55,0.35,0.10])[0]
    if pat_type == 'SA':
        nationality = "South African"
        doc_type = "SA ID"
        doc_number = f"SA{random.randint(1000000,9999999)}"
        legal_status = "Legal"
        result = "Verification successful."
    elif pat_type == 'Foreign':
        nationality = random.choice(["Zimbabwean", "Malawian", "Mozambican", "Pakistani", "Other"])
        doc_type = random.choice(["Passport", "Asylum Seeker Permit", "Refugee Status Document"])
        doc_number = f"F{random.randint(1000000,9999999)}"
        legal_status = "Legal"
        result = "Verification successful."
    else: # Illegal
        nationality = random.choice(["Zimbabwean", "Malawian", "Mozambican", "Pakistani", "Other"])
        doc_type = random.choice(["Unknown", "Forged Passport", "SA ID"])
        doc_number = f"X{random.randint(1000000,9999999)}"
        legal_status = "Illegal"
        result = "Patient flagged for referral to Home Affairs."
    timestamp = (datetime.now(SA_TIMEZONE) - timedelta(days=admit_days_ago)).strftime('%Y-%m-%d %H:%M:%S')
    return {
        "patient_id": f"P{1000+pid}",
        "name": name,
        "admission_date": admission_date,
        "discharge_date": None,
        "diagnosis": diag,
        "ward": ward,
        "nationality": nationality,
        "doc_type": doc_type,
        "doc_number": doc_number,
        "legal_status": legal_status,
        "result": result,
        "timestamp": timestamp
    }

if "patients_df" not in st.session_state:
    st.session_state.patients_df = pd.DataFrame(columns=[
        'patient_id', 'name', 'doc_number', 'doc_type', 'nationality', 'result', 'legal_status', 'timestamp', 'admission_status', 'ward'
    ])
if "visits_df" not in st.session_state:
    st.session_state.visits_df = pd.DataFrame(columns=[
        'patient_id', 'name', 'visit_date', 'diagnosis', 'treatment', 'cost', 'hospital', 'ward', 'meds_prescribed', 'admitted', 'discharged'
    ])
if "admissions_df" not in st.session_state:
    base = [
        {"patient_id": "P1001", "name": "Thabo Radebe", "admission_date": TODAY, "discharge_date": None, "diagnosis": "Severe Malaria", "ward": "Emergency Unit",
         "nationality": "South African", "doc_type": "SA ID", "doc_number": "SA1234567", "legal_status": "Legal", "result": "Verification successful.",
         "timestamp": datetime.now(SA_TIMEZONE).strftime('%Y-%m-%d %H:%M:%S')},
        {"patient_id": "P1002", "name": "Ayesha Khan", "admission_date": TODAY, "discharge_date": None, "diagnosis": "Tuberculosis (Pulmonary)", "ward": "Medical Ward",
         "nationality": "Pakistani", "doc_type": "Passport", "doc_number": "F2345678", "legal_status": "Legal", "result": "Verification successful.",
         "timestamp": datetime.now(SA_TIMEZONE).strftime('%Y-%m-%d %H:%M:%S')},
        {"patient_id": "P1003", "name": "Maria Gonzalez", "admission_date": TODAY, "discharge_date": None, "diagnosis": "Labor & Delivery (Complicated)", "ward": "Maternity Ward",
         "nationality": "Malawian", "doc_type": "Forged Passport", "doc_number": "X3456789", "legal_status": "Illegal", "result": "Patient flagged for referral to Home Affairs.",
         "timestamp": datetime.now(SA_TIMEZONE).strftime('%Y-%m-%d %H:%M:%S')},
        {"patient_id": "P1004", "name": "Jean-Paul Mbatha", "admission_date": TODAY, "discharge_date": None, "diagnosis": "Appendicitis", "ward": "Surgical Ward",
         "nationality": "South African", "doc_type": "SA ID", "doc_number": "SA4567890", "legal_status": "Legal", "result": "Verification successful.",
         "timestamp": datetime.now(SA_TIMEZONE).strftime('%Y-%m-%d %H:%M:%S')},
        {"patient_id": "P1005", "name": "Sibongile Mokoena", "admission_date": TODAY, "discharge_date": None, "diagnosis": "Stroke (Ischemic)", "ward": "ICU",
         "nationality": "Zimbabwean", "doc_type": "Unknown", "doc_number": "X5678901", "legal_status": "Illegal", "result": "Patient flagged for referral to Home Affairs.",
         "timestamp": datetime.now(SA_TIMEZONE).strftime('%Y-%m-%d %H:%M:%S')},
    ]
    for i in range(6, 201):
        base.append(random_patient(i))
    st.session_state.admissions_df = pd.DataFrame(base)
    ward_counts = st.session_state.admissions_df[st.session_state.admissions_df['discharge_date'].isnull()].groupby('ward').size().to_dict()
else:
    ward_counts = st.session_state.admissions_df[st.session_state.admissions_df['discharge_date'].isnull()].groupby('ward').size().to_dict()

# Ensure patients_df has all the fields populated for admitted patients
for _, row in st.session_state.admissions_df.iterrows():
    if row["patient_id"] not in st.session_state.patients_df["patient_id"].values:
        st.session_state.patients_df.loc[len(st.session_state.patients_df)] = [
            row["patient_id"], row["name"], row.get("doc_number",""), row.get("doc_type",""),
            row.get("nationality",""), row.get("result",""), row.get("legal_status",""),
            row.get("timestamp",""), "Yes", row["ward"]
        ]

if "resource_state" not in st.session_state:
    st.session_state.resource_state = {
        "wards": {
            "Emergency Unit": {"total_beds": 80, "available_beds": 80-ward_counts.get("Emergency Unit",0)},
            "Surgical Ward": {"total_beds": 60, "available_beds": 60-ward_counts.get("Surgical Ward",0)},
            "Medical Ward": {"total_beds": 100, "available_beds": 100-ward_counts.get("Medical Ward",0)},
            "Pediatric Ward": {"total_beds": 40, "available_beds": 40-ward_counts.get("Pediatric Ward",0)},
            "Maternity Ward": {"total_beds": 50, "available_beds": 50-ward_counts.get("Maternity Ward",0)},
            "ICU": {"total_beds": 30, "available_beds": 30-ward_counts.get("ICU",0)},
        },
        "medications": {
            "Paracetamol": 1200, "Amoxicillin": 800, "Ibuprofen": 650, "Metformin": 500, "Lisinopril": 300,
            "Ventolin Inhaler": 150, "Ceftriaxone Injection": 100, "Diazepam": 200, "ORS Sachets": 300,
            "Co-trimoxazole Syrup": 120, "Oxytocin": 200, "Morphine": 100, "Calpol": 300, "Antibiotics": 400,
            "Artemether": 150, "IV Fluids": 400, "Normal Saline": 600, "Potassium Chloride": 150,
            "Azithromycin": 200, "Cefazolin": 120, "Aspirin": 500, "Atorvastatin": 300, "Enoxaparin": 100,
            "Pethidine": 80, "Rifampicin": 300, "Isoniazid": 200, "Pyrazinamide": 200, "Ethambutol": 200,
            "Salbutamol": 180, "Prednisone": 120, "Magnesium Sulfate": 100, "Labetalol": 100, "Dexamethasone": 80,
        },
        "staff": staff_list(),
        "clocked_in": []
    }
    st.session_state.resource_state["clocked_in"] = []
    staff = st.session_state.resource_state["staff"]
    doctors = [s for s in staff if s["type"]=="Doctor"][:10]
    nurses = [s for s in staff if s["type"]=="Nurse"][:10]
    for s in doctors+nurses:
        st.session_state.resource_state["clocked_in"].append({
            "name": s["name"],
            "type": s["type"],
            "department": s["department"],
            "clock_time": "07:30"
        })

patients_df = st.session_state.patients_df
visits_df = st.session_state.visits_df
admissions_df = st.session_state.admissions_df
resource_state = st.session_state.resource_state

if "page" not in st.session_state:
    st.session_state.page = "dashboard"
if "sidebar_filter" not in st.session_state:
    st.session_state.sidebar_filter = None

# ====== TREATMENT PLANS ======
TREATMENT_PLANS = {
    "Hypertension": {
        "plan": "Lifestyle changes and medication",
        "medications": [
            {"name": "Amlodipine", "dosage": "5-10 mg", "frequency": "Once daily"},
            {"name": "Hydrochlorothiazide", "dosage": "12.5-25 mg", "frequency": "Once daily"},
        ],
        "costs": {"SA Residents": 0, "Legal Immigrants": 350, "Illegal Immigrants": 800},
        "notes": "Standard protocol for hypertension. Monitor BP regularly."
    },
    "Type 2 Diabetes": {
        "plan": "Diet and medication",
        "medications": [
            {"name": "Metformin", "dosage": "500-1000 mg", "frequency": "Twice daily"},
        ],
        "costs": {"SA Residents": 0, "Legal Immigrants": 510, "Illegal Immigrants": 1150},
        "notes": "Lifestyle modification and metformin as first-line therapy."
    },
    "Asthma": {
        "plan": "Avoid triggers, regular use of inhalers",
        "medications": [
            {"name": "Salbutamol Inhaler", "dosage": "100 mcg/puff", "frequency": "As needed"},
            {"name": "Beclomethasone Inhaler", "dosage": "100-200 mcg", "frequency": "Twice daily"}
        ],
        "costs": {"SA Residents": 0, "Legal Immigrants": 270, "Illegal Immigrants": 620},
        "notes": "Educate on inhaler technique and trigger avoidance."
    },
    "Common Infections": {
        "plan": "Appropriate antibiotics",
        "medications": [
            {"name": "Amoxicillin", "dosage": "500 mg", "frequency": "3 times daily"},
            {"name": "Ciprofloxacin", "dosage": "500 mg", "frequency": "Twice daily"}
        ],
        "costs": {"SA Residents": 0, "Legal Immigrants": 190, "Illegal Immigrants": 450},
        "notes": "Review after 3 days if symptoms persist."
    },
    "Mental Health": {
        "plan": "Counseling/psychotherapy and medication if needed",
        "medications": [
            {"name": "Fluoxetine", "dosage": "20 mg", "frequency": "Once daily"},
            {"name": "Amitriptyline", "dosage": "25 mg", "frequency": "Once daily"}
        ],
        "costs": {"SA Residents": 0, "Legal Immigrants": 370, "Illegal Immigrants": 900},
        "notes": "Monitor for response and side effects. Refer to psych if needed."
    },
    "Severe Malaria": {
        "plan": "Administer IV Artemether and antipyretics. Monitor vitals every 2 hours. Blood glucose to be checked regularly.",
        "medications": [
            {"name": "Artemether", "dosage": "IV", "frequency": "As per protocol"},
            {"name": "Paracetamol", "dosage": "500mg", "frequency": "Every 6 hours"},
            {"name": "IV Fluids", "dosage": "As per protocol", "frequency": "Continuous"}
        ],
        "costs": {"SA Residents": 0, "Legal Immigrants": 950, "Illegal Immigrants": 2200},
        "notes": "Patient presented with high fever, chills, headache, and confusion. Blood smear confirmed Plasmodium falciparum."
    },
    "Tuberculosis (Pulmonary)": {
        "plan": "Start DOTS protocol. Isolate patient. Notify TB program.",
        "medications": [
            {"name": "Rifampicin", "dosage": "600mg", "frequency": "Daily"},
            {"name": "Isoniazid", "dosage": "300mg", "frequency": "Daily"},
            {"name": "Pyrazinamide", "dosage": "1500mg", "frequency": "Daily"},
            {"name": "Ethambutol", "dosage": "1200mg", "frequency": "Daily"}
        ],
        "costs": {"SA Residents": 0, "Legal Immigrants": 1200, "Illegal Immigrants": 2600},
        "notes": "Persistent cough, night sweats, and weight loss. Sputum positive for AFB."
    },
    "Labor & Delivery (Complicated)": {
        "plan": "Prep for surgery, administer spinal block, post-op monitoring and antibiotics.",
        "medications": [
            {"name": "Oxytocin", "dosage": "IV", "frequency": "As per protocol"},
            {"name": "Pethidine", "dosage": "100mg", "frequency": "As needed"},
            {"name": "Ceftriaxone", "dosage": "1g", "frequency": "Once daily"}
        ],
        "costs": {"SA Residents": 0, "Legal Immigrants": 1650, "Illegal Immigrants": 3500},
        "notes": "Labor prolonged, signs of fetal distress. Emergency C-section advised."
    },
    "Appendicitis": {
        "plan": "Prepare for emergency appendectomy. Pre-op antibiotics. Monitor vitals post-op.",
        "medications": [
            {"name": "Morphine", "dosage": "IV", "frequency": "As needed"},
            {"name": "Cefazolin", "dosage": "1g", "frequency": "Pre-op"},
            {"name": "Paracetamol", "dosage": "500mg", "frequency": "Every 6 hours"}
        ],
        "costs": {"SA Residents": 0, "Legal Immigrants": 1200, "Illegal Immigrants": 2700},
        "notes": "RLQ pain with rebound tenderness. Ultrasound confirms inflamed appendix."
    },
    "Stroke (Ischemic)": {
        "plan": "Initiate antiplatelet therapy. Begin physiotherapy and swallow assessment.",
        "medications": [
            {"name": "Aspirin", "dosage": "150mg", "frequency": "Once daily"},
            {"name": "Atorvastatin", "dosage": "40mg", "frequency": "Once daily"},
            {"name": "Enoxaparin", "dosage": "40mg", "frequency": "Once daily"}
        ],
        "costs": {"SA Residents": 0, "Legal Immigrants": 1750, "Illegal Immigrants": 3900},
        "notes": "Slurred speech, left-sided weakness. CT scan confirmed non-hemorrhagic stroke."
    },
    "Eclampsia": {
        "plan": "Administer magnesium sulfate, control BP, prepare for delivery.",
        "medications": [
            {"name": "Magnesium Sulfate", "dosage": "IV", "frequency": "As per protocol"},
            {"name": "Labetalol", "dosage": "20mg", "frequency": "IV"},
            {"name": "Oxytocin", "dosage": "IV", "frequency": "As per protocol"}
        ],
        "costs": {"SA Residents": 0, "Legal Immigrants": 1050, "Illegal Immigrants": 2200},
        "notes": "Seizure in third trimester. BP elevated at 180/110. Proteinuria detected."
    },
    "Severe Pneumonia": {
        "plan": "Admit for IV antibiotics and oxygen therapy. Monitor for respiratory distress.",
        "medications": [
            {"name": "Ceftriaxone", "dosage": "IV", "frequency": "Once daily"},
            {"name": "Azithromycin", "dosage": "500mg", "frequency": "Once daily"},
            {"name": "Oxygen", "dosage": "As needed", "frequency": "Continuous"}
        ],
        "costs": {"SA Residents": 0, "Legal Immigrants": 900, "Illegal Immigrants": 1950},
        "notes": "Crackles heard on auscultation, O₂ saturation at 86%. Chest X-ray shows consolidation."
    },
    "Diabetic Ketoacidosis (DKA)": {
        "plan": "Start insulin infusion, rehydrate with IV fluids, correct electrolyte imbalances, monitor blood gases.",
        "medications": [
            {"name": "IV Insulin", "dosage": "As per protocol", "frequency": "Continuous"},
            {"name": "Normal Saline", "dosage": "IV", "frequency": "Continuous"},
            {"name": "Potassium Chloride", "dosage": "IV", "frequency": "As needed"}
        ],
        "costs": {"SA Residents": 0, "Legal Immigrants": 1120, "Illegal Immigrants": 2500},
        "notes": "Blood sugar >25 mmol/L, ketonuria detected. Dehydration and altered mental status present."
    },
    "Meningitis (Bacterial)": {
        "plan": "Start IV antibiotics immediately. Monitor neurological status.",
        "medications": [
            {"name": "Ceftriaxone", "dosage": "2g", "frequency": "Twice daily"},
            {"name": "Dexamethasone", "dosage": "10mg", "frequency": "Once daily"},
            {"name": "Paracetamol", "dosage": "500mg", "frequency": "Every 6 hours"}
        ],
        "costs": {"SA Residents": 0, "Legal Immigrants": 1350, "Illegal Immigrants": 2900},
        "notes": "Fever, stiff neck, photophobia. Lumbar puncture confirmed bacterial infection."
    }
}

def detect_illegal_status(nationality, document_type, visa_status=None, expiry_date=None, verification_result=None):
    doc_type = document_type.lower().replace(" ", "")
    legal_docs = ["said", "passport", "asylumseekerpermit", "refugeestatusdocument", "workpermit", "studypermit", "residencypermit"]
    if nationality == "South African":
        return doc_type != "said"
    if doc_type not in legal_docs:
        return True
    if verification_result:
        if verification_result in ["Suspected Forgery", "Unverified", "Pending Manual Review"]:
            return True
    if visa_status is not None:
        if visa_status.lower() in ["expired", "missing", "invalid"]:
            return True
    if expiry_date:
        try:
            expiry = datetime.strptime(expiry_date, "%Y-%m-%d")
            if expiry < datetime.now():
                return True
        except:
            return True
    return False

# ====== SIDEBAR ======
with st.sidebar:
    st.image("assets/Batho_pele.png", width=90)
    st.markdown(f'<div class="sidebar-welcome">Welcome {st.session_state.get("username", "")}</div>', unsafe_allow_html=True)
    st.divider()
    if st.button("🏠 Dashboard"): st.session_state.page = "dashboard"; st.rerun()
    if st.button("📋 Patient Intake"): st.session_state.page = "patient_intake"; st.rerun()
    if st.button("🛏️ Admissions"): st.session_state.page = "admissions"; st.rerun()
    if st.button("🏥 Resource Monitoring"): st.session_state.page = "resource_monitoring"; st.rerun()
    if st.button("👥 Patient Search"): st.session_state.page = "patient_search"; st.rerun()
    st.divider()
    st.markdown('<div class="section-title">Patient Metrics</div>', unsafe_allow_html=True)
    if st.button("SA Patients"): st.session_state.page = "dashboard"; st.session_state.sidebar_filter = "sa_patients"; st.rerun()
    if st.button("Foreign Nationals"): st.session_state.page = "dashboard"; st.session_state.sidebar_filter = "foreign_patients"; st.rerun()
    if st.button("Needs Referral"): st.session_state.page = "dashboard"; st.session_state.sidebar_filter = "needs_referral"; st.rerun()
    if st.button("Admitted Patients"): st.session_state.page = "dashboard"; st.session_state.sidebar_filter = "admitted_patients"; st.rerun()
    sa_patients = len(patients_df[patients_df['nationality'] == 'South African'])
    foreign_patients = len(patients_df[patients_df['nationality'] != 'South African'])
    needs_referral = len(patients_df[patients_df['legal_status'] == 'Illegal'])
    admitted_patients = len(admissions_df[pd.isnull(admissions_df['discharge_date'])])
    st.markdown(f'<div class="sidebar-metric">SA Patients: {sa_patients}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="sidebar-metric">Foreign Nationals: {foreign_patients}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="sidebar-metric">Needs Referral: {needs_referral}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="sidebar-metric">Admitted Patients: {admitted_patients}</div>', unsafe_allow_html=True)
    st.divider()
    admissions_today = len(admissions_df[(admissions_df['admission_date'] == TODAY)])
    discharged_today = len(admissions_df[(admissions_df['discharge_date'] == TODAY)])
    if st.button("Admissions Today"): st.session_state.page = "dashboard"; st.session_state.sidebar_filter = "admissions_today"; st.rerun()
    if st.button("Discharges Today"): st.session_state.page = "dashboard"; st.session_state.sidebar_filter = "discharges_today"; st.rerun()
    st.markdown(f'<div class="sidebar-metric">Admissions Today: {admissions_today}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="sidebar-metric">Discharges Today: {discharged_today}</div>', unsafe_allow_html=True)
    st.divider()
    if st.button("Logout"): st.session_state.authenticated = False; st.rerun()

# UI FUNCTIONS
def dashboard_ui():
    filter_type = st.session_state.get("sidebar_filter")
    if filter_type:
        if filter_type == "sa_patients":
            st.subheader("South African Patients")
            st.dataframe(patients_df[patients_df['nationality'] == 'South African'], use_container_width=True)
        elif filter_type == "foreign_patients":
            st.subheader("Foreign National Patients")
            st.dataframe(patients_df[patients_df['nationality'] != 'South African'], use_container_width=True)
        elif filter_type == "needs_referral":
            st.subheader("Patients Needing Referral")
            st.dataframe(patients_df[patients_df['legal_status'] == 'Illegal'], use_container_width=True)
        elif filter_type == "admissions_today":
            st.subheader("Today's Admissions")
            st.dataframe(admissions_df[admissions_df['admission_date'] == TODAY], use_container_width=True)
        elif filter_type == "discharges_today":
            st.subheader("Today's Discharges")
            st.dataframe(admissions_df[admissions_df['discharge_date'] == TODAY], use_container_width=True)
        elif filter_type == "admitted_patients":
            st.subheader("Admitted Patients")
            st.dataframe(admissions_df[pd.isnull(admissions_df['discharge_date'])], use_container_width=True)
        st.session_state.sidebar_filter = None
        return

    st.markdown('<div class="header"><h1>🏥 BathoPele_AI Hospital Dashboard</h1></div>', unsafe_allow_html=True)
    today_str = TODAY
    admissions_today = admissions_df[admissions_df['admission_date'] == today_str]
    discharges_today = admissions_df[admissions_df['discharge_date'] == today_str]
    dash_cols = st.columns(4)
    dash_cols[0].metric("Admissions Today", len(admissions_today))
    dash_cols[1].metric("Discharges Today", len(discharges_today))
    dash_cols[2].metric("Beds Available", sum([w['available_beds'] for w in resource_state['wards'].values()]))
    dash_cols[3].metric("Medications in Stock", sum(resource_state['medications'].values()))
    st.markdown('<hr>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Current Admissions (Top 3)</div>', unsafe_allow_html=True)
    top_admissions = admissions_df[pd.isnull(admissions_df['discharge_date'])].head(3)
    if not top_admissions.empty:
        st.dataframe(top_admissions[['patient_id','name','diagnosis','ward','admission_date']], use_container_width=True)
    else:
        st.info("No current admissions.")
    st.markdown('<div class="section-title">Top Diagnoses Today</div>', unsafe_allow_html=True)
    if not admissions_today.empty:
        diagnosis_count = admissions_today['diagnosis'].value_counts().head(3)
        for diag, count in diagnosis_count.items():
            st.markdown(f"- **{diag}**: {count} cases")
    else:
        st.info("No diagnoses recorded today.")

def intake_ui():
    st.markdown('<div class="header"><h1>📋 Patient Intake</h1></div>', unsafe_allow_html=True)

    # Reset signal for next patient: only clears intake_patient, not intake_treatment
    if "reset_intake" not in st.session_state:
        st.session_state.reset_intake = False

    # If user wants to start new patient, clear form fields, but keep last treatment for invoice/record
    if st.session_state.reset_intake:
        st.session_state.intake_patient = None
        st.session_state.reset_intake = False
        # DO NOT CLEAR intake_treatment here

    # Intake form only shows if no patient intake in session
    if "intake_patient" not in st.session_state or st.session_state.intake_patient is None:
        with st.form("patient_intake_form"):
            cols = st.columns(2)
            name = cols[0].text_input("Full Name*", placeholder="First Last")
            nationality = cols[0].selectbox("Nationality*", ["South African", "Zimbabwean", "Malawian", "Mozambican", "Pakistani", "Other"])
            doc_number = cols[0].text_input("Document Number*", placeholder="ID/Passport Number")
            doc_type = cols[1].selectbox("Document Type*", ["SA ID", "Passport", "Asylum Seeker Permit", "Refugee Status Document"])
            visa_status = cols[1].selectbox("Visa/Permit Status (if foreign)", ["Valid", "Expired", "Missing", "Not Applicable"])
            expiry_date = cols[1].text_input("Expiry Date (if applicable, YYYY-MM-DD)", value="")
            verification_result = cols[0].selectbox("Manual Document Verification", ["Verified", "Suspected Forgery", "Unverified", "Pending Manual Review"])
            admission_status = cols[1].selectbox("Admit Patient?", ["No", "Yes"])
            ward = st.selectbox("Ward", list(resource_state["wards"].keys()) + ["Outpatient"])
            submitted = st.form_submit_button("Submit Patient Information")
        if submitted:
            intake_data = {
                "name": name, "nationality": nationality, "doc_number": doc_number,
                "doc_type": doc_type, "visa_status": visa_status, "expiry_date": expiry_date,
                "verification_result": verification_result, "admission_status": admission_status, "ward": ward
            }
            st.session_state.intake_patient = intake_data
            st.session_state.current_patient_id = f"P{random.randint(1000,9999)}"
            st.session_state.intake_verify = (
                (nationality != "South African" and (doc_type == "Unknown" or visa_status != "Valid" or verification_result != "Verified"))
            )
            st.rerun()
        # After submit, form does not hang! After record, buttons will show.

    # The rest of the UI (diagnosis, treatment, etc)
    if "intake_patient" in st.session_state and st.session_state.intake_patient is not None:
        intake_data = st.session_state.intake_patient
        legal_status = "Illegal" if st.session_state.intake_verify else "Legal" if intake_data['nationality'] != 'South African' else "Legal"
        result_text = "Patient flagged for referral to Home Affairs." if legal_status == "Illegal" else "Verification successful."

        diagnosis = st.selectbox("Diagnosis*", list(TREATMENT_PLANS.keys()) + ["Other"], key="diagnosis_select")
        plan_data = TREATMENT_PLANS.get(diagnosis, {})
        treatment_plan = plan_data.get("plan", "")
        meds = plan_data.get("medications", [])
        notes = plan_data.get("notes", "")
        meds_prescribed = ", ".join([med['name'] for med in meds]) if meds else ""
        if intake_data['nationality'] == 'South African':
            cost = plan_data.get("costs", {}).get("SA Residents", 0)
        elif legal_status == "Legal":
            cost = plan_data.get("costs", {}).get("Legal Immigrants", 0)
        else:
            cost = plan_data.get("costs", {}).get("Illegal Immigrants", 0)

        if diagnosis != "Other":
            st.text_area("Treatment Plan", value=treatment_plan, disabled=True)
            st.write("### Prescribed Medications")
            for med in meds:
                st.markdown(f"- **{med['name']}**: {med['dosage']} {med['frequency']}")
            doctor_notes = st.text_area("Doctor Comments", value="", key="doctor_comments")
        else:
            treatment_plan = st.text_area("Treatment Plan", value=intake_data.get("treatment_plan",""))
            meds_prescribed = st.text_input("Medication(s) Prescribed", value=intake_data.get("meds_prescribed",""))
            doctor_notes = st.text_area("Doctor Comments", value=intake_data.get("notes",""), key="doctor_comments_other")

        if intake_data['nationality'] == 'South African':
            cost_type = "South African Citizen (Free Health Care)"
        elif legal_status == "Legal":
            cost_type = "Legal Immigrant (Subsidized Payment)"
        else:
            cost_type = "Illegal Immigrant (Full Payment)"
        st.markdown(f"""
            <div class="metric-card">
            <strong>Payment Category:</strong> {cost_type}<br>
            <strong>Diagnosis:</strong> {diagnosis}<br>
            <strong>Cost:</strong> <span style="color: #003366; font-size: 1.3em;">R{cost:,.2f}</span>
            </div>
            """, unsafe_allow_html=True)

        if legal_status == "Illegal":
            st.warning("⚠️ Patient flagged for referral to Home Affairs.")

        # Confirm & Save
        if st.button("Confirm & Save Record"):
            timestamp = datetime.now(SA_TIMEZONE).strftime('%Y-%m-%d %H:%M:%S')
            patient_id = st.session_state.current_patient_id
            patients_df.loc[len(patients_df)] = [
                patient_id, intake_data["name"], intake_data["doc_number"], intake_data["doc_type"], intake_data["nationality"],
                result_text, legal_status, timestamp, intake_data["admission_status"], intake_data["ward"]
            ]
            visits_df.loc[len(visits_df)] = [
                patient_id, intake_data["name"], TODAY, diagnosis, treatment_plan, cost, "BathoPele_AI", intake_data["ward"], meds_prescribed, intake_data["admission_status"] == "Yes", False
            ]
            if intake_data["admission_status"] == "Yes" and intake_data["ward"] != "Outpatient":
                admissions_df.loc[len(admissions_df)] = [
                    patient_id, intake_data["name"], TODAY, None, diagnosis, intake_data["ward"],
                    intake_data.get("nationality", ""), intake_data.get("doc_type", ""), intake_data.get("doc_number", ""),
                    legal_status, result_text, timestamp
                ]
                resource_state["wards"][intake_data["ward"]]["available_beds"] = max(
                    0, resource_state["wards"][intake_data["ward"]]["available_beds"] - 1
                )
            for med in meds:
                med_name = med['name'].split()[0]
                if med_name in resource_state["medications"]:
                    resource_state["medications"][med_name] = max(0, resource_state["medications"][med_name] - 1)
            st.success("Patient record created and treatment saved!")

            # Save to session for invoice and record
            st.session_state.intake_treatment = {
                "patient_id": patient_id,
                "name": intake_data["name"],
                "doc_number": intake_data["doc_number"],
                "doc_type": intake_data["doc_type"],
                "nationality": intake_data["nationality"],
                "diagnosis": diagnosis,
                "ward": intake_data["ward"],
                "meds_prescribed": meds_prescribed,
                "notes": doctor_notes,   # <-- Doctor's notes are now saved!
                "cost": cost,
                "result": result_text,
                "legal_status": legal_status,
                "timestamp": timestamp
            }

            # Only clear intake_patient (to show buttons); DO NOT rerun yet!
            st.session_state.intake_patient = None
            st.success("You can now download invoice or view record below.")

    # After save, these buttons will show (if intake_treatment exists)
    if "intake_treatment" in st.session_state and st.session_state.intake_treatment:
        lp = st.session_state.intake_treatment
        invoice_text = f"""
BATHO PELE HEALTHCARE INITIATIVE
---------------------------------
Invoice Date: {TODAY}
Patient: {lp['name']}
ID: {lp['doc_number']}
---------------------------------
Diagnosis: {lp['diagnosis']}
Treatment: {TREATMENT_PLANS.get(lp['diagnosis'],{}).get('plan','')}
Medication: {lp['meds_prescribed']}
---------------------------------
TOTAL COST: R{lp['cost']:,.2f}
"""
        st.download_button(
            label="Download Invoice",
            data=invoice_text,
            file_name=f"invoice_{lp['name']}_{TODAY.replace('-','')}.txt",
            mime="text/plain"
        )
        if st.button("View Patient Record"):
            with st.expander("Patient Record Summary", expanded=True):
                st.write(f"**Patient Number:** {lp['patient_id']}")
                st.write(f"**Name:** {lp['name']}")
                st.write(f"**Document:** {lp['doc_type']} {lp['doc_number']}")
                st.write(f"**Nationality:** {lp['nationality']}")
                st.write(f"**Status:** {lp['legal_status']}")
                st.write(f"**Diagnosis:** {lp['diagnosis']}")
                st.write(f"**Ward:** {lp['ward']}")
                st.write(f"**Medications:** {lp['meds_prescribed']}")
                st.write(f"**Notes:** {lp['notes']}")
                st.write(f"**Cost:** R{lp['cost']:,.2f}")
                st.write(f"**Verification:** {lp['result']}")
                st.write(f"**Timestamp:** {lp['timestamp']}")

        # Optional: Button to start next patient (clears treatment and shows form)
        if st.button("Start Next Patient Intake"):
            st.session_state.intake_treatment = None
            st.session_state.reset_intake = True
            st.rerun()

def admissions_ui():
    st.markdown('<div class="header"><h1>🛏️ Admissions</h1></div>', unsafe_allow_html=True)
    admitted = admissions_df[pd.isnull(admissions_df['discharge_date'])]
    if admitted.empty:
        st.info("No current admissions.")
        return
    st.dataframe(admitted[['patient_id','name','diagnosis','ward','admission_date']], use_container_width=True)
    st.markdown("### Discharge a Patient")
    discharge_options = admitted['patient_id'].tolist()
    discharge_id = st.selectbox("Select patient ID to discharge", discharge_options)
    patient_row = admitted[admitted['patient_id']==discharge_id].iloc[0]
    plan_data = TREATMENT_PLANS.get(patient_row['diagnosis'], {})
    auto_meds = ", ".join([med['name'] for med in plan_data.get('medications',[])])
    realistic_notes_map = {
        "Severe Malaria": "Patient stabilized with IV Artemether, fever controlled. Advise malaria prophylaxis and follow-up.",
        "Tuberculosis (Pulmonary)": "Completed DOTS protocol initiation, patient stable. Continue home isolation and regular sputum checks.",
        "Labor & Delivery (Complicated)": "Post-operative recovery after C-section. Ensure wound care and neonatal monitoring.",
        "Appendicitis": "Appendectomy performed successfully, patient recovering. Advise wound care and pain management.",
        "Stroke (Ischemic)": "Initiated physiotherapy, patient improving. Continue aspirin and monitor progress.",
        "Hypertension": "Blood pressure stabilized, patient educated on lifestyle modifications and medication adherence.",
        "Type 2 Diabetes": "Blood glucose controlled, patient educated on diet and medication adherence.",
        "Asthma": "Symptoms stabilized, patient educated on inhaler use and trigger avoidance.",
        "Common Infections": "Symptoms resolved, complete prescribed antibiotics.",
        "Mental Health": "Patient stable, continue follow-up with counselor/psychologist.",
        "Eclampsia": "BP controlled, post-delivery monitoring advised.",
        "Severe Pneumonia": "Symptoms improved, continue home antibiotics and monitor.",
        "Diabetic Ketoacidosis (DKA)": "DKA resolved, continue insulin and diet management.",
        "Meningitis (Bacterial)": "Symptoms resolved, monitor for neurological sequelae."
    }
    auto_notes = realistic_notes_map.get(patient_row['diagnosis'], plan_data.get('notes',''))
    discharge_meds = st.text_input("Discharge Medication", value=auto_meds)
    discharge_notes = st.text_area("Doctor's Discharge Notes", value=auto_notes)
    follow_up = st.text_area("Follow-up Instructions", value=f"Follow-up in 2 weeks for {patient_row['diagnosis']}.")
    if st.button("Confirm Discharge"):
        discharge_idx = admissions_df[admissions_df['patient_id']==discharge_id].index[0]
        admissions_df.at[discharge_idx,'discharge_date'] = TODAY
        ward = admissions_df.at[discharge_idx,'ward']
        if ward in resource_state["wards"]:
            resource_state["wards"][ward]["available_beds"] = min(
                resource_state["wards"][ward]["total_beds"], resource_state["wards"][ward]["available_beds"] + 1
            )
        for med in discharge_meds.split(", "):
            med_short = med.split()[0]
            if med_short in resource_state["medications"]:
                resource_state["medications"][med_short] = max(0, resource_state["medications"][med_short] - 1)
        st.success("Patient discharged successfully.")
        st.rerun()

def search_ui():
    st.markdown('<div class="header"><h1>👥 Patient Search</h1></div>', unsafe_allow_html=True)
    search_cols = st.columns(3)
    name_search = search_cols[0].text_input("Name")
    id_search = search_cols[1].text_input("ID/Passport Number")
    nationality_filter = search_cols[2].selectbox("Nationality", ["All"] + list(patients_df['nationality'].dropna().unique()))
    filtered_patients = patients_df.copy()
    admitted_patients = admissions_df[pd.isnull(admissions_df['discharge_date'])]
    admitted_patient_ids = admitted_patients['patient_id'].tolist()
    missing_adm = admitted_patients[~admitted_patients['patient_id'].isin(patients_df['patient_id'])]
    if not missing_adm.empty:
        for _, row in missing_adm.iterrows():
            patients_df.loc[len(patients_df)] = [
                row['patient_id'], row['name'], '', '', '', '', '', row['admission_date'], 'Yes', row['ward']
            ]
    if name_search:
        filtered_patients = filtered_patients[
            filtered_patients['name'].notna() & 
            filtered_patients['name'].str.contains(name_search, case=False, na=False, regex=False)
        ]
    if id_search:
        filtered_patients = filtered_patients[
            filtered_patients['doc_number'].notna() & 
            filtered_patients['doc_number'].str.contains(id_search, case=False, na=False, regex=False)
        ]
    if nationality_filter != "All":
        filtered_patients = filtered_patients[filtered_patients['nationality'] == nationality_filter]
    if not filtered_patients.empty:
        st.subheader(f"Found {len(filtered_patients)} patients")
        show_cols = ['patient_id', 'name', 'nationality', 'doc_type', 'doc_number', 'legal_status', 'admission_status', 'ward', 'timestamp']
        st.dataframe(
            filtered_patients[show_cols].rename(columns={
                'patient_id': 'Patient Number',
                'name': 'Name',
                'nationality': 'Nationality',
                'doc_type': 'Document Type',
                'doc_number': 'Document Number',
                'legal_status': 'Legal Status',
                'admission_status': 'Admitted',
                'ward': 'Ward',
                'timestamp': 'Last Updated'
            }),
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info("No patients found matching your criteria")

def resource_ui():
    st.markdown('<div class="header"><h1>🏥 Resource Monitoring</h1></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Wards and Beds Available</div>', unsafe_allow_html=True)
    wards_df = pd.DataFrame([
        {"Ward":w,"Beds Available":v['available_beds'],"Total Beds":v['total_beds']}
        for w,v in resource_state["wards"].items()
    ])
    st.dataframe(wards_df, use_container_width=True)
    st.markdown('<div class="section-title">Medication Stock Levels</div>', unsafe_allow_html=True)
    meds_df = pd.DataFrame([
        {"Medication Name":k,"Stock Units":v} for k,v in resource_state["medications"].items()
    ])
    st.dataframe(meds_df, use_container_width=True)
    st.markdown('<div class="section-title">Staff On Duty</div>', unsafe_allow_html=True)
    staff_df = pd.DataFrame(resource_state["clocked_in"])
    if not staff_df.empty:
        st.dataframe(staff_df[["name","type","department","clock_time"]], use_container_width=True)
    else:
        st.info("No staff clocked in for today.")

    st.markdown('<div class="section-title">All Staff (Doctors & Nurses)</div>', unsafe_allow_html=True)
    all_staff_df = pd.DataFrame(resource_state["staff"])
    st.dataframe(all_staff_df[["name","type","department"]], use_container_width=True)

    st.markdown('<div class="section-title">Order Medication / Staff Clock-In</div>', unsafe_allow_html=True)
    order_cols = st.columns(2)
    with order_cols[0]:
        st.subheader("Order Medication")
        med_name = st.selectbox("Medication", list(resource_state["medications"].keys()), key="med_order_name")
        qty = st.number_input("Quantity to add", min_value=1, value=10, key="med_order_qty")
        if st.button("Add Medication Stock", key="add_med_btn"):
            resource_state["medications"][med_name] += qty
            st.success(f"Added {qty} units to {med_name}.")
            st.rerun()
    with order_cols[1]:
        st.subheader("Staff Clock-In/Out")
        staff_names = [s["name"] for s in resource_state["staff"]]
        selected_staff = st.selectbox("Staff Member", staff_names, key="clock_staff")
        staff_info = next((s for s in resource_state["staff"] if s["name"] == selected_staff), None)
        department = staff_info["department"] if staff_info else ""
        staff_type = staff_info["type"] if staff_info else ""
        st.text_input("Department", value=department, disabled=True)
        st.text_input("Type", value=staff_type, disabled=True)
        clock_action = st.radio("Action", ["Clock-In", "Clock-Out"], key="clock_action")
        if st.button("Confirm Clock", key="clock_btn"):
            if clock_action == "Clock-In":
                if selected_staff not in [c["name"] for c in resource_state["clocked_in"]]:
                    resource_state["clocked_in"].append({
                        "name": selected_staff,
                        "type": staff_type,
                        "department": department,
                        "clock_time": datetime.now(SA_TIMEZONE).strftime('%H:%M')
                    })
                    st.success(f"{staff_type} {selected_staff} clocked in for {department}.")
                    st.rerun()
                else:
                    st.warning("Staff already clocked in.")
            else:
                resource_state["clocked_in"] = [c for c in resource_state["clocked_in"] if c["name"] != selected_staff]
                st.success(f"{staff_type} {selected_staff} clocked out.")
                st.rerun()

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

if st.session_state.page == "dashboard":
    dashboard_ui()
elif st.session_state.page == "patient_intake":
    intake_ui()
elif st.session_state.page == "admissions":
    admissions_ui()
elif st.session_state.page == "resource_monitoring":
    resource_ui()
elif st.session_state.page == "patient_search":
    search_ui()
footer_ui()
