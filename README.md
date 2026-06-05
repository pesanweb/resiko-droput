# Proyek Akhir: Student Dropout Prediction - Perusahaan Edutech

## Informasi Proyek
- **Nama**: [Andy Yulianto]
- **Email**: [rinovannet@gmail.com]
- **ID Dicoding**: [andyid]
- **Dataset**: [data.csv](data/data.csv)
- **Deploy App**: [Deteksi Resiko Dropout](https://resiko-droput.streamlit.app/)

---

## 1. Business Understanding

### Latar Belakang
Perusahaan Edutech menghadapi masalah **tingginya angka dropout** (mahasiswa keluar sebelum menyelesaikan studi). Hal ini menyebabkan:
- Kehilangan pendapatan dari biaya kuliah
- Reputasi institusi yang terganggu
- Pemborosan sumber daya pendidikan
- Target akreditasi sulit tercapai

### Permasalahan Bisnis
1. **Identifikasi Dini**: Bagaimana cara mengidentifikasi mahasiswa yang berisiko dropout sejak awal?
2. **Faktor Penyebab**: Faktor apa saja yang paling mempengaruhi keputusan mahasiswa untuk keluar?
3. **Intervensi**: Strategi apa yang efektif untuk mencegah dropout?

### Tujuan Proyek
1. Menganalisis faktor-faktor penyebab dropout mahasiswa
2. Membangun model machine learning untuk memprediksi risiko dropout
3. Menyediakan dashboard monitoring untuk pihak manajemen
4. Memberikan rekomendasi action items yang dapat diimplementasikan

---

## 2. Data Understanding

### Deskripsi Dataset
Dataset berisi informasi mahasiswa dengan **4.424 baris** dan **37 kolom**. Sumber data dari UCI Machine Learning Repository.

### Variabel Kategori

| Kategori | Variabel | Deskripsi |
|----------|----------|-----------|
| **Demografi** | Marital_status, Gender, Age_at_enrollment, Nationality | Informasi personal mahasiswa |
| **Akademik** | Admission_grade, Previous_qualification_grade | Nilai masuk dan kualifikasi sebelumnya |
| **Kurikulum** | Course, Curricular_units_1st/2nd_sem_* | Mata kuliah dan satuan kredit |
| **Finansial** | Debtor, Tuition_fees_up_to_date, Scholarship_holder | Status keuangan mahasiswa |
| **Sosial** | Displaced, Educational_special_needs, International | Status sosial dan kebutuhan khusus |
| **Makro** | Unemployment_rate, Inflation_rate, GDP | Kondisi ekonomi makro |
| **Target** | Status | **Dropout**, **Graduate**, atau **Enrolled** |

### Distribusi Target
- **Graduate**: ~50% (2.207 mahasiswa)
- **Dropout**: ~33% (1.421 mahasiswa)
- **Enrolled**: ~17% (794 mahasiswa)

### Pendekatan Klasifikasi
**Penting**: Model menggunakan **binary classification** (Dropout vs Graduate):
- **Training data**: Hanya mahasiswa dengan status **Dropout** (1.421) dan **Graduate** (2.207)
- **Data Enrolled** (794 mahasiswa): **Tidak digunakan untuk training**, hanya untuk inferensi/prediksi
- **Alasan**: Enrolled adalah status sementara, bukan outcome akhir yang valid untuk pelatihan model prediksi dropout

**Catatan**: Kode prodi (Course) adalah anonim dari dataset UCI untuk privasi. Mapping nama prodi ada di `queries/dashboard_queries.sql`.

---

## 3. Solusi Machine Learning

### Algoritma yang Digunakan

| Algoritma | Peran | Alasan |
|-----------|-------|--------|
| **Logistic Regression** | Terbaik | Akurasi 92.01%, interpretasi mudah |
| **Random Forest** | Perbandingan | Feature importance, robust terhadap outlier |

**Klasifikasi Binary**: Model memprediksi 2 kelas saja (Dropout vs Graduate). Data Enrolled digunakan untuk inferensi/prediksi kemungkinan status akhir mahasiswa.

**Best Model**: Logistic Regression (92.01% accuracy)

### Mengapa Logistic Regression Dipilih?

1. **Akurasi Lebih Tinggi**: 92.01% vs Random Forest 90.77%
2. **Interpretasi Mudah**: Koefisien model mudah dipahami
3. **Cepat**: Training dan prediksi lebih cepat
4. **Cocok untuk Binary Classification**: Efektif membedakan Dropout vs Graduate
5. **Probabilitas**: Memberikan probabilitas dropout yang dapat diandalkan

### Pipeline Machine Learning

```
┌─────────────────────────────────────────────────────────────┐
│                    ML PIPELINE                              │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1. DATA LOADING                                            │
│     Load dataset dari URL (4424 data)                       │
│                                                             │
│  2. FILTERING DATA                                          │
│     - Filter: hanya Dropout & Graduate untuk training       │
│     - Simpan data Enrolled untuk inferensi                  │
│     - Data training: 3628 mahasiswa                         │
│                                                             │
│  3. EDA & UNDERSTANDING                                     │
│     Analisis distribusi, korelasi, faktor dominan           │
│                                                             │
│  4. PREPROCESSING                                           │
│     - Encode variabel target (binary: Dropout/Graduate)     │
│     - Feature scaling (StandardScaler)                      │
│     - Train-test split (80/20)                              │
│                                                             │
│  5. MODELING                                                │
│     - Logistic Regression (terbaik - 92.01%)                │
│     - Random Forest (perbandingan - 90.77%)                 │
│                                                             │
│  6. EVALUATION                                              │
│     - Accuracy, Precision, Recall, F1-Score                 │
│     - Confusion Matrix (2x2)                                │
│     - Feature Importance                                    │
│                                                             │
│  7. INFERENSI (Opsional)                                    │
│     - Prediksi status akhir mahasiswa Enrolled              │
│     - Identifikasi mahasiswa berisiko dropout               │
│                                                             │
│  8. DEPLOYMENT                                              │
│     - Streamlit App (prototype prediksi)                    │
│     - Metabase Dashboard (monitoring)                       │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Feature Importance (Top 5)

| Rank | Fitur | Penjelasan |
|------|-------|------------|
| 1 | Curricular_units_2nd_sem_approved | Unit lulus semester 2 |
| 2 | Curricular_units_1st_sem_approved | Unit lulus semester 1 |
| 3 | Tuition_fees_up_to_date | Keterlambatan pembayaran |
| 4 | Debtor | Status berutang |
| 5 | Scholarship_holder | Status beasiswa |

---

## 4. Business Dashboard (Metabase)

### Yang Ditampilkan di Dashboard

| No | Dashboard | Tujuan |
|----|-----------|--------|
| 1 | Distribusi Status | Ringkasan jumlah Dropout/Graduate/Enrolled |
| 2 | Faktor Finansial | Pengaruh debitur, pembayaran, beasiswa |
| 3 | Performa Akademik | Rata-rata nilai & unit lulus per status |
| 4 | Per Program Studi | Dropout rate per prodi |
| 5 | Per Usia | Kelompok usia paling berisiko |
| 6 | Per Gender | Perbandingan laki-laki vs perempuan |
| 7 | Pengaruh Beasiswa | Dampak beasiswa terhadap retensi |
| 8 | Pengaruh Debitur | Dampak status berutang |
| 9 | Unit Gagal | Analisis kegagalan per semester |
| 10 | Early Warning | Identifikasi mahasiswa berisiko |
| 11 | Komparasi | Perbedaan dropout vs graduate |
| 12 | Kondisi Ekonomi | Dampak GDP terhadap dropout |

### Akses Dashboard
- **URL**: http://localhost:3000
- **Email**: `root@mail.com`
- **Password**: `root123`

### Cara Membuat Dashboard
1. Buka Metabase → Login
2. Klik **+ New** → **SQL Query**
3. Copy-paste query dari `queries/dashboard_queries.sql`
4. Klik **Run** → **Save** → Beri nama card
5. Klik **+ New** → **Dashboard** → Tambahkan card

### Export/Import Database

```bash
# Export data PostgreSQL
docker exec student-postgres pg_dump -U postgres student_dropout > backup_student.sql

# Export Metabase (dashboard & pengaturan)
docker cp metabase:/metabase.db/metabase.db.mv.db ./

# Restore data PostgreSQL
docker exec -i student-postgres psql -U postgres student_dropout < backup_student.sql

# Restore Metabase
docker cp ./metabase.db.mv.db metabase:/metabase.db/metabase.db.mv.db
docker restart metabase
```

**Catatan**: Jika sulit export Metabase, cukup simpan query SQL di `queries/dashboard_queries.sql`. Dashboard bisa di-recreate kapan saja.

---

## 5. Prototype Machine Learning (Streamlit)

### UI Yang Dibuat

| Komponen | Deskripsi |
|----------|-----------|
| **Header** | Judul aplikasi dengan ikon |
| **Sidebar Input** | Form input terpisah per kategori (Tab) |
| **Hasil Prediksi** | Status, probabilitas, tingkat risiko |
| **Risk Assessment** | Faktor risiko detail + rekomendasi |
| **Feature Importance** | Grafik fitur paling berpengaruh |
| **Statistik Dataset** | Ringkasan data mahasiswa |

### Fitur UI

1. **Input Form Terpisah**
   - Tab Demografi (status nikah, gender, usia)
   - Tab Akademik (nilai masuk, unit semester)
   - Tab Finansial (debitur, pembayaran, beasiswa)
   - Tab Ekonomi (pengangguran, inflasi, GDP)

2. **Prediksi Real-time**
   - Status: Dropout / Graduate (binary classification)
   - Probabilitas: 0-100%
   - Tingkat Risiko: RENDAH / SEDANG / TINGGI

3. **Risk Assessment**
   - Faktor risiko yang teridentifikasi
   - Rekomendasi intervensi (segera & jangka panjang)

4. **Visualisasi**
   - Bar chart feature importance
   - Grafik distribusi status mahasiswa

### Akses Streamlit
- **Lokal**: http://localhost:8501
- **Online**: https://your-app.streamlit.app

---

## 6. Menjalankan Sistem

### Tahap 1: Persiapan Environment
```bash
conda activate customer-segmentation-dicoding
conda install -c conda-forge pandas numpy matplotlib seaborn scikit-learn=1.3.2 jupyter joblib streamlit sqlalchemy psycopg2 -y
pip install psycopg2-binary
```

### Tahap 2: Training Model
```bash
jupyter notebook notebook.ipynb
```
Jalankan semua cell dari atas ke bawah.

### Tahap 3: Import Data ke PostgreSQL
Jalankan cell "Import data ke PostgreSQL" di notebook.

### Tahap 4: Jalankan Streamlit
```bash
streamlit run app.py
```

### Tahap 5: Buat Dashboard Metabase
1. Buka http://localhost:3000
2. Login: `root@mail.com` / `root123`
3. Buat SQL Query → Save ke Dashboard

---

## 7. Deploy ke Internet

### Streamlit Cloud (GRATIS)
1. Push ke GitHub
2. Buka https://share.streamlit.io
3. Login dengan GitHub
4. Klik **New app** → Pilih repository → Deploy

### Hasil Deploy
- URL: `https://resiko-droput.streamlit.app/`
- Bisa diakses dari mana saja

---

## 8. Kesimpulan

### Hasil Analisis

**Pendekatan Klasifikasi:**
- Model dilatih menggunakan **binary classification** (Dropout vs Graduate)
- Data Enrolled (status sementara) **tidak digunakan untuk training**
- Data Enrolled digunakan untuk **inferensi/prediksi** kemungkinan status akhir

**Faktor utama yang mempengaruhi dropout:**

1. **Finansial**: Status debitur dan keterlambatan biaya kuliah adalah prediktor terkuat
2. **Akademik**: Jumlah satuan kredit yang tidak lulus di semester 1 dan 2
3. **Beasiswa**: Mahasiswa dengan beasiswa memiliki risiko dropout lebih rendah
4. **Nilai Masuk**: Admission grade yang rendah berkorelasi dengan dropout

### Performa Model

| Metrik | Logistic Regression | Random Forest |
|--------|---------------------|---------------|
| Accuracy | **92.01%** | 90.77% |

**Best Model**: Logistic Regression (92.01% accuracy)

**Best Model**: Logistic Regression (92.01% accuracy)

### Rekomendasi Action Items

**Berdasarkan hasil analisis**, mahasiswa dengan status debitur + biaya kuliah tidak tertib memiliki probabilitas dropout tertinggi (>70%). Selain itu, mahasiswa yang tidak lulus ≥ 2 unit di semester 1 juga menunjukkan risiko tinggi. Oleh karena itu, rekomendasi berikut diurutkan berdasarkan prioritas dampak:

#### **PRIORITAS 1 — TINGGI (Dampak Langsung pada Dropout Rate)**

| No | Rekomendasi | Dasar Data | Implementasi Praktis | Target Dampak |
|----|-------------|------------|---------------------|---------------|
| 1 | **Program Beasiswa Darurat untuk Debitur** | Mahasiswa dengan `Debtor=1` dan `Tuition_fees_up_to_date=0` memiliki dropout rate >70% | Buat skema beasiswa darurat khusus untuk mahasiswa berprestasi (GPA >2.5) yang memiliki tunggakan. Proses: verifikasi data keuangan → wawancara → persetujuan dalam 2 minggu | Kurangi dropout finansial 40-50% |
| 2 | **Skema Cicilan Khusus** | Data menunjukkan keterlambatan pembayaran berkorelasi kuat dengan dropout | Tawarkan cicilan 3-6 bulan untuk mahasiswa dengan tunggakan >1 bulan. Implementasi: kerjasama dengan bank mitra untuk skema pinjaman lunak | Kurangi tunggakan 60% dalam 1 semester |
| 3 | **Early Warning System Akademik** | Mahasiswa dengan `Curricular_units_1st_sem_approved < 4` memiliki risiko dropout 3x lebih tinggi | Sistem otomatis yang mengirim alert ke dosen pembimbing ketika mahasiswa tidak lulus ≥2 unit di semester 1. Proses: integrasi SIAKUN → notifikasi → konseling dalam 1 minggu | Identifikasi 90% mahasiswa berisiko sebelum semester 3 |

#### **PRIORITAS 2 — SEDANG (Pencegahan Jangka Menengah)**

| No | Rekomendasi | Dasar Data | Implementasi Praktis | Target Dampak |
|----|-------------|------------|---------------------|---------------|
| 4 | **Program Mentor Akademik** | Mahasiswa dengan `Admission_grade < 120` dan `Curricular_units_2nd_sem_approved < 4` cenderung dropout | Pairing mahasiswa berisiko dengan mentor (mahasiswa senior berprestasi). Implementasi: 2x pertemuan/bulan, fokus pada mata kuliah yang gagal | Tingkatkan kelulusan unit 25-30% |
| 5 | **Perluasan Program Beasiswa Berprestasi** | Data menunjukkan `Scholarship_holder=1` memiliki dropout rate <15% (vs 45% non-beasiswa) | Tambah kuota beasiswa 20% untuk mahasiswa dengan GPA >3.0 dan penghasilan keluarga <UMR. Proses: seleksi setiap awal semester | Kurangi dropout 15-20% pada kelompok berprestasi |
| 6 | **Monitoring Real-time Dashboard** | Data historis menunjukkan pola dropout bisa dideteksi sejak semester 1 | Deploy dashboard Metabase untuk monitoring mingguan. KPI: dropout rate per prodi, jumlah mahasiswa berisiko, efektivitas intervensi | Response time intervensi dari 1 bulan ke 1 minggu |

#### **PRIORITAS 3 — RENDAH (Optimasi Jangka Panjang)**

| No | Rekomendasi | Dasar Data | Implementasi Praktis | Target Dampak |
|----|-------------|------------|---------------------|---------------|
| 7 | **Evaluasi Kurikulum Prodi** | Beberapa prodi memiliki dropout rate >50% (berdasarkan analisis per Course) | Review kurikulum prodi dengan dropout rate tertinggi. Implementasi: survei mahasiswa dropout → identifikasi mata kuliah bermasalah → revisi kurikulum | Kurangi dropout prodi bermasalah 30% dalam 2 tahun |
| 8 | **Program Konseling Holistik** | Faktor non-akademik (usia, status pernikahan) juga berkontribusi pada dropout | Sediakan konseling psikologis dan karir untuk mahasiswa berisiko. Implementasi: kerjasama dengan psikolog kampus, 1x/bulan | Peningkatan retensi 10-15% |

#### **Cara Menggunakan Model Prediksi**

1. **Input data mahasiswa** ke Streamlit app (https://resiko-droput.streamlit.app/)
2. **Lihat hasil prediksi**: status (Dropout/Graduate), probabilitas, tingkat risiko
3. **Ambil tindakan** berdasarkan tingkat risiko:
   - **Risiko Tinggi (>60%)**: Intervensi segera (beasiswa darurat + konseling)
   - **Risiko Sedang (30-60%)**: Monitoring ketat + mentor akademik
   - **Risiko Rendah (<30%)**: Monitoring rutin

#### **Metrik Keberhasilan**

| Metrik | Baseline | Target 6 Bulan | Target 1 Tahun |
|--------|----------|----------------|----------------|
| Dropout Rate | 32% | 25% | 20% |
| Identifikasi Dini | 0% | 70% | 90% |
| Response Time Intervensi | 1 bulan | 2 minggu | 1 minggu |
| Retensi Mahasiswa Berisiko | 0% | 40% | 60% |

---

## 9. Visualisasi Data

| Bagian | Visualisasi | Tujuan |
|--------|-------------|--------|
| EDA | Bar chart distribusi status | Melihat proporsi Dropout/Graduate |
| EDA | Box plot nilai per status | Membandingkan performa akademik |
| EDA | Heatmap korelasi | Melihat hubungan antar fitur |
| EDA | Crosstab faktor finansial | Analisis pengaruh keuangan |
| Model | Confusion matrix | Evaluasi performa klasifikasi |
| Model | Feature importance | Faktor paling berpengaruh |
| Model | Perbandingan model | Logistic vs Random Forest |
| Streamlit | Risk assessment | Identifikasi risiko mahasiswa |
| Streamlit | Grafik feature importance | Visualisasi faktor dominan |
| Streamlit | Statistik dataset | Ringkasan data |

---

## 10. Troubleshooting

| Masalah | Solusi |
|---------|--------|
| `ImportError: DLL load failed` | Jalankan cell install di notebook |
| `ModuleNotFoundError` | Jalankan cell pertama notebook |
| `streamlit` tidak dikenal | `pip install streamlit` |
| `psycopg2` error | `pip install psycopg2-binary` |
| `function round() does not exist` | Query sudah fix dengan `::numeric` cast |
| Query error `near "data"` | Gunakan `"data"` dengan quote |
| Tabel data tidak ada | Jalankan cell import di notebook |
| Docker error port | `docker stop` lalu `docker-compose up -d` |
| `docker cp` metabase error | Gunakan `metabase:/metabase.db/metabase.db.mv.db` (bukan student-metabase) |
| Model belum tersimpan | Jalankan cell terakhir notebook |

---

## 11. File Structure

```
a590_proyek_akhir/
├── README.md                 # Dokumentasi proyek
├── app.py                    # Aplikasi Streamlit (production-ready)
├── notebook.ipynb            # Notebook analisis & training
├── requirements.txt          # Dependencies (untuk Streamlit Cloud)
├── .streamlit/
│   └── config.toml           # Konfigurasi Streamlit
├── data/
│   └── data.csv              # Dataset mahasiswa
├── model/
│   ├── model_dropout.pkl     # Model Binary Classification (Dropout vs Graduate)
│   ├── scaler.pkl            # Scaler
│   └── label_encoders.pkl    # Label encoder (binary: Dropout/Graduate)

```

---

## 12. Referensi

1. [UCI Student Dropout Dataset](https://archive.ics.uci.edu/ml/datasets/student+performance)
2. [Scikit-learn Documentation](https://scikit-learn.org/)
3. [Streamlit Documentation](https://docs.streamlit.io/)
4. [Streamlit Cloud Deployment](https://docs.streamlit.io/streamlit-community-cloud/deploy-your-app)
5. [Metabase Documentation](https://www.metabase.com/docs/)
6. [Pandas Documentation](https://pandas.pydata.org/)
