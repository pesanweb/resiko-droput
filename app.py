import streamlit as st
import pandas as pd
import numpy as np
import joblib
import os
from pathlib import Path

# ============================================================
# KONFIGURASI HALAMAN
# ============================================================
st.set_page_config(
    page_title="Student Dropout Prediction",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# CUSTOM CSS
# ============================================================
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 0;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #666;
        text-align: center;
        margin-top: 0;
    }
    .metric-card {
        background-color: #f0f2f6;
        border-radius: 10px;
        padding: 20px;
        text-align: center;
    }
    .risk-high {
        background-color: #ff4b4b;
        color: white;
        padding: 10px;
        border-radius: 5px;
        text-align: center;
        font-weight: bold;
    }
    .risk-medium {
        background-color: #ffa726;
        color: white;
        padding: 10px;
        border-radius: 5px;
        text-align: center;
        font-weight: bold;
    }
    .risk-low {
        background-color: #66bb6a;
        color: white;
        padding: 10px;
        border-radius: 5px;
        text-align: center;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)


# ============================================================
# LOAD MODEL
# ============================================================
@st.cache_resource
def load_model():
    """Load model, scaler, dan label encoder dari folder model/"""
    model_path = Path('model/model_dropout.pkl')
    scaler_path = Path('model/scaler.pkl')
    encoder_path = Path('model/label_encoders.pkl')
    
    if not all([model_path.exists(), scaler_path.exists(), encoder_path.exists()]):
        return None, None, None
    
    model = joblib.load(model_path)
    scaler = joblib.load(scaler_path)
    label_encoders = joblib.load(encoder_path)
    return model, scaler, label_encoders


# ============================================================
# LOAD DATA
# ============================================================
@st.cache_data
def load_data():
    """Load dataset untuk statistik"""
    try:
        df = pd.read_csv('data/data.csv', sep=';')
        return df
    except Exception:
        return None


# ============================================================
# HEADER
# ============================================================
st.markdown('<h1 class="main-header">🎓 Student Dropout Prediction</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Sistem Prediksi Risiko Dropout Mahasiswa menggunakan Machine Learning</p>', unsafe_allow_html=True)
st.markdown("---")


# ============================================================
# LOAD MODEL & DATA
# ============================================================
model, scaler, label_encoders = load_model()
df = load_data()


# ============================================================
# SIDEBAR - INPUT DATA
# ============================================================
st.sidebar.image("https://img.icons8.com/color/96/000000/student-male.png", width=80)
st.sidebar.header("📋 Input Data Mahasiswa")

# Tab untuk input
tab_input = st.sidebar.tabs(["Demografi", "Akademik", "Finansial", "Ekonomi"])

with tab_input[0]:
    st.subheader("Data Demografi")
    
    marital_status = st.selectbox(
        "Status Pernikahan",
        options=[1, 2, 3, 4, 5, 6],
        format_func=lambda x: {
            1: "Single", 2: "Married", 3: "Widower",
            4: "Divorced", 5: "Facto Union", 6: "Legally Separated"
        }.get(x, str(x))
    )
    
    gender = st.selectbox(
        "Jenis Kelamin",
        options=[0, 1],
        format_func=lambda x: "Perempuan" if x == 0 else "Laki-laki"
    )
    
    age = st.number_input("Usia saat Pendaftaran", min_value=17, max_value=70, value=20)
    
    international = st.selectbox(
        "Status Internasional",
        options=[0, 1],
        format_func=lambda x: "Tidak" if x == 0 else "Ya"
    )

with tab_input[1]:
    st.subheader("Data Akademik")
    
    admission_grade = st.slider("Nilai Masuk (Admission Grade)", 0.0, 200.0, 120.0)
    previous_qualification_grade = st.slider("Nilai Kualifikasi Sebelumnya", 0.0, 200.0, 130.0)
    
    st.markdown("**Semester 1**")
    sem1_enrolled = st.number_input("Unit Diambil Sem 1", min_value=0, max_value=10, value=6)
    sem1_approved = st.number_input("Unit Lulus Sem 1", min_value=0, max_value=10, value=5)
    sem1_grade = st.slider("Rata-rata Nilai Sem 1", 0.0, 20.0, 12.0)
    
    st.markdown("**Semester 2**")
    sem2_enrolled = st.number_input("Unit Diambil Sem 2", min_value=0, max_value=10, value=6)
    sem2_approved = st.number_input("Unit Lulus Sem 2", min_value=0, max_value=10, value=5)
    sem2_grade = st.slider("Rata-rata Nilai Sem 2", 0.0, 20.0, 12.0)

with tab_input[2]:
    st.subheader("Data Finansial")
    
    debtor = st.selectbox(
        "Status Debitur",
        options=[0, 1],
        format_func=lambda x: "Tidak" if x == 0 else "Ya (Berutang)"
    )
    
    tuition_fees_up_to_date = st.selectbox(
        "Biaya Kuliah Tertib",
        options=[0, 1],
        format_func=lambda x: "Tidak Tertib" if x == 0 else "Tertib"
    )
    
    scholarship_holder = st.selectbox(
        "Penerima Beasiswa",
        options=[0, 1],
        format_func=lambda x: "Tidak" if x == 0 else "Ya"
    )

with tab_input[3]:
    st.subheader("Kondisi Ekonomi")
    
    unemployment_rate = st.slider("Tingkat Pengangguran (%)", 0.0, 20.0, 10.0)
    inflation_rate = st.slider("Tingkat Inflasi (%)", -5.0, 15.0, 1.0)
    gdp = st.slider("GDP", -10.0, 10.0, 0.0)


# ============================================================
# TOMBOL PREDIKSI
# ============================================================
st.sidebar.markdown("---")
predict_button = st.sidebar.button("🔮 Prediksi Dropout", type="primary", use_container_width=True)


# ============================================================
# KONTEN UTAMA
# ============================================================

# Cek apakah model tersedia
if model is None:
    st.error("⚠️ **Model belum dilatih!**")
    st.info("""
    **Langkah untuk melatih model:**
    1. Buka terminal di folder `a590_proyek_akhir`
    2. Jalankan: `jupyter notebook notebook.ipynb`
    3. Jalankan semua cell dari atas ke bawah
    4. Setelah selesai, jalankan: `streamlit run app.py`
    """)
    st.stop()


# ============================================================
# PREDIKSI
# ============================================================
if predict_button:
    # Buat input dataframe
    input_data = pd.DataFrame({
        'Marital_status': [marital_status],
        'Gender': [gender],
        'Age_at_enrollment': [age],
        'International': [international],
        'Admission_grade': [admission_grade],
        'Previous_qualification_grade': [previous_qualification_grade],
        'Curricular_units_1st_sem_enrolled': [sem1_enrolled],
        'Curricular_units_1st_sem_approved': [sem1_approved],
        'Curricular_units_1st_sem_grade': [sem1_grade],
        'Curricular_units_2nd_sem_enrolled': [sem2_enrolled],
        'Curricular_units_2nd_sem_approved': [sem2_approved],
        'Curricular_units_2nd_sem_grade': [sem2_grade],
        'Debtor': [debtor],
        'Tuition_fees_up_to_date': [tuition_fees_up_to_date],
        'Scholarship_holder': [scholarship_holder],
        'Unemployment_rate': [unemployment_rate],
        'Inflation_rate': [inflation_rate],
        'GDP': [gdp]
    })
    
    # Scaling fitur numerik
    numerical_cols = [
        'Age_at_enrollment', 'Admission_grade', 'Previous_qualification_grade',
        'Curricular_units_1st_sem_enrolled', 'Curricular_units_1st_sem_approved',
        'Curricular_units_1st_sem_grade', 'Curricular_units_2nd_sem_enrolled',
        'Curricular_units_2nd_sem_approved', 'Curricular_units_2nd_sem_grade',
        'Unemployment_rate', 'Inflation_rate', 'GDP'
    ]
    
    input_data[numerical_cols] = scaler.transform(input_data[numerical_cols])
    
    # Prediksi
    prediction = model.predict(input_data)
    probability = model.predict_proba(input_data)
    
    # Ambil probabilitas dropout
    classes = list(label_encoders.classes_)
    dropout_idx = classes.index('Dropout') if 'Dropout' in classes else 0
    dropout_prob = probability[0][dropout_idx]
    
    # Tentukan tingkat risiko
    if dropout_prob > 0.6:
        risk_level = "TINGGI"
        risk_color = "red"
        risk_emoji = "🔴"
    elif dropout_prob > 0.3:
        risk_level = "SEDANG"
        risk_color = "orange"
        risk_emoji = "🟡"
    else:
        risk_level = "RENDAH"
        risk_color = "green"
        risk_emoji = "🟢"
    
    # ============================================================
    # TAMPILKAN HASIL
    # ============================================================
    st.markdown("## 📊 Hasil Prediksi")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            label="Status Prediksi",
            value=prediction[0],
            delta=None
        )
    
    with col2:
        st.metric(
            label="Probabilitas Dropout",
            value=f"{dropout_prob*100:.1f}%",
            delta=None
        )
    
    with col3:
        st.metric(
            label="Tingkat Risiko",
            value=f"{risk_emoji} {risk_level}",
            delta=None
        )
    
    # ============================================================
    # RISK ASSESSMENT
    # ============================================================
    st.markdown("---")
    
    if prediction[0] == 'Dropout':
        st.markdown(f'<div class="risk-high">🚨 RISIKO TINGGI: Mahasiswa ini berisiko tinggi untuk dropout!</div>', unsafe_allow_html=True)
        
        st.markdown("### ⚠️ Faktor Risiko yang Teridentifikasi")
        
        risk_factors = []
        if debtor == 1:
            risk_factors.append("💰 **Status Debitur**: Mahasiswa memiliki utang")
        if tuition_fees_up_to_date == 0:
            risk_factors.append("💳 **Biaya Tidak Tertib**: Pembayaran kuliah terlambat")
        if scholarship_holder == 0:
            risk_factors.append("🎓 **Tidak Ada Beasiswa**: Tidak mendapat bantuan biaya")
        if sem1_approved < sem1_enrolled * 0.7:
            risk_factors.append("📚 **Unit Lulus Rendah Sem 1**: Hanya {} dari {} unit lulus".format(sem1_approved, sem1_enrolled))
        if sem2_approved < sem2_enrolled * 0.7:
            risk_factors.append("📚 **Unit Lulus Rendah Sem 2**: Hanya {} dari {} unit lulus".format(sem2_approved, sem2_enrolled))
        if sem1_grade < 10:
            risk_factors.append("📉 **Nilai Sem 1 Rendah**: Rata-rata hanya {:.1f}".format(sem1_grade))
        if sem2_grade < 10:
            risk_factors.append("📉 **Nilai Sem 2 Rendah**: Rata-rata hanya {:.1f}".format(sem2_grade))
        if admission_grade < 120:
            risk_factors.append("📝 **Nilai Masuk Rendah**: Admission grade {:.1f}".format(admission_grade))
        
        for factor in risk_factors:
            st.warning(factor)
        
        st.markdown("### 💡 Rekomendasi Intervensi")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.info("""
            **Langkah Segera:**
            1. Jadwalkan konseling akademik
            2. Evaluasi untuk program bantuan finansial
            3. Monitoring perkembangan setiap 2 minggu
            """)
        
        with col2:
            st.info("""
            **Langkah Jangka Panjang:**
            1. Sediakan bimbingan belajar
            2. Daftarkan program beasiswa
            3. Komunikasi dengan orang tua/wali
            """)
    
    elif prediction[0] == 'Graduate':
        st.markdown(f'<div class="risk-low">✅ RISIKO RENDAH: Mahasiswa ini diprediksi akan lulus!</div>', unsafe_allow_html=True)
        
        st.markdown("### ✅ Faktor Pendukung")
        
        if scholarship_holder == 1:
            st.success("🎓 **Penerima Beasiswa**: Memiliki bantuan biaya")
        if tuition_fees_up_to_date == 1:
            st.success("💳 **Biaya Tertib**: Pembayaran kuliah lancar")
        if sem1_approved >= sem1_enrolled * 0.8:
            st.success("📚 **Unit Lulus Sem 1 Baik**: {} dari {} unit lulus".format(sem1_approved, sem1_enrolled))
        if sem2_approved >= sem2_enrolled * 0.8:
            st.success("📚 **Unit Lulus Sem 2 Baik**: {} dari {} unit lulus".format(sem2_approved, sem2_enrolled))
        if sem1_grade >= 12:
            st.success("📈 **Nilai Sem 1 Baik**: Rata-rata {:.1f}".format(sem1_grade))
        if sem2_grade >= 12:
            st.success("📈 **Nilai Sem 2 Baik**: Rata-rata {:.1f}".format(sem2_grade))
    
    else:
        st.markdown(f'<div class="risk-medium">⏳ STATUS ENROLLED: Mahasiswa ini masih terdaftar</div>', unsafe_allow_html=True)
        st.warning("Monitor perkembangan akademik secara berkala.")
    
    # ============================================================
    # FEATURE IMPORTANCE
    # ============================================================
    if hasattr(model, 'feature_importances_'):
        st.markdown("---")
        st.markdown("### 📈 Faktor Paling Berpengaruh")
        
        feature_names = [
            'Marital_status', 'Gender', 'Age_at_enrollment', 'International',
            'Admission_grade', 'Previous_qualification_grade',
            'Curricular_units_1st_sem_enrolled', 'Curricular_units_1st_sem_approved',
            'Curricular_units_1st_sem_grade', 'Curricular_units_2nd_sem_enrolled',
            'Curricular_units_2nd_sem_approved', 'Curricular_units_2nd_sem_grade',
            'Debtor', 'Tuition_fees_up_to_date', 'Scholarship_holder',
            'Unemployment_rate', 'Inflation_rate', 'GDP'
        ]
        
        importance_df = pd.DataFrame({
            'Feature': feature_names,
            'Importance': model.feature_importances_
        }).sort_values('Importance', ascending=False).head(10)
        
        st.bar_chart(importance_df.set_index('Feature'))


# ============================================================
# STATISTIK DATASET
# ============================================================
if df is not None:
    st.markdown("---")
    st.markdown("## 📊 Statistik Dataset")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Mahasiswa", f"{len(df):,}")
    
    with col2:
        dropout_count = len(df[df['Status'] == 'Dropout'])
        st.metric("Dropout", f"{dropout_count:,}", f"{dropout_count/len(df)*100:.1f}%")
    
    with col3:
        graduate_count = len(df[df['Status'] == 'Graduate'])
        st.metric("Lulus", f"{graduate_count:,}", f"{graduate_count/len(df)*100:.1f}%")
    
    with col4:
        enrolled_count = len(df[df['Status'] == 'Enrolled'])
        st.metric("Enrolled", f"{enrolled_count:,}", f"{enrolled_count/len(df)*100:.1f}%")
    
    # Distribusi Status
    st.markdown("### Distribusi Status Mahasiswa")
    status_counts = df['Status'].value_counts()
    st.bar_chart(status_counts)
    
    # Data Preview
    with st.expander("📋 Lihat Data Mentah"):
        st.dataframe(df.head(20), use_container_width=True)


# ============================================================
# FOOTER
# ============================================================
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #888; font-size: 0.8rem;'>
    <p>Student Dropout Prediction System | Proyek Akhir Dicoding</p>
    <p>Dibuat dengan Streamlit & Scikit-learn</p>
</div>
""", unsafe_allow_html=True)
