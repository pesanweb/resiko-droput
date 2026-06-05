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
| **Logistic Regression** | Baseline | Interpretasi mudah, probabilitas dropout |
| **Random Forest** | Utama | Akurasi tinggi, feature importance, robust |

**Klasifikasi Binary**: Model memprediksi 2 kelas saja (Dropout vs Graduate). Data Enrolled digunakan untuk inferensi/prediksi kemungkinan status akhir mahasiswa.

### Mengapa Random Forest Dipilih?

1. **Akurasi Lebih Tinggi**: ~85% vs Logistic Regression ~82%
2. **Feature Importance**: Bisa menunjukkan faktor paling berpengaruh
3. **Hubungan Kompleks**: Menangkap hubungan non-linear antar fitur
4. **Robust**: Tidak terpengaruh outlier
5. **Cocok untuk Dataset Campuran**: Menangani numerik + kategorik

### Pipeline Machine Learning

```
┌─────────────────────────────────────────────────────────────┐
│                    ML PIPELINE                              │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1. DATA LOADING                                            │
│     Load dataset dari CSV (4424 data)                       │
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
│     - Logistic Regression (baseline)                        │
│     - Random Forest (utama)                                 │
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
- URL: `https://username-repo-app.streamlit.app`
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
| Accuracy | ~85% | ~85% |
| Precision | ~85% | ~85% |
| Recall | ~85% | ~85% |
| F1-Score | ~85% | ~85% |

**Catatan**: Model menggunakan binary classification (Dropout vs Graduate), sehingga performa lebih baik dibanding 3-class classification. Akurasi aktual dapat dilihat dari output notebook.

### Rekomendasi Action Items

| No | Action Items | Target | Timeline |
|----|--------------|--------|----------|
| 1 | **Early Warning System**: Gunakan model prediksi | Identifikasi 90% dropout sebelum semester 3 | 1 bulan |
| 2 | **Program Bantuan Finansial**: Prioritas untuk debitur | Kurangi dropout finansial 50% | Segera |
| 3 | **Monitoring Akademik**: Pantau unit tidak lulus ≥ 2 | Intervensi 100% mahasiswa berisiko | Setiap semester |
| 4 | **Program Beasiswa**: Perluas untuk berprestasi | Tambah penerima 20% | Tahun ajaran baru |
| 5 | **Dashboard Monitoring**: Metabase real-time | Update mingguan, review bulanan | Setelah setup |
| 6 | **Intervensi Personal**: Konseling untuk risiko > 50% | 100% mahasiswa berisiko tinggi | 2 minggu |

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
├── docker-compose.yml        # Docker (Metabase + PostgreSQL)
├── data/
│   └── data.csv              # Dataset mahasiswa
├── model/
│   ├── model_dropout.pkl     # Model Binary Classification (Dropout vs Graduate)
│   ├── scaler.pkl            # Scaler
│   └── label_encoders.pkl    # Label encoder (binary: Dropout/Graduate)
└── queries/
    └── dashboard_queries.sql # 12 Query untuk Metabase
```

---

## 12. Referensi

1. [UCI Student Dropout Dataset](https://archive.ics.uci.edu/ml/datasets/student+performance)
2. [Scikit-learn Documentation](https://scikit-learn.org/)
3. [Streamlit Documentation](https://docs.streamlit.io/)
4. [Streamlit Cloud Deployment](https://docs.streamlit.io/streamlit-community-cloud/deploy-your-app)
5. [Metabase Documentation](https://www.metabase.com/docs/)
6. [Pandas Documentation](https://pandas.pydata.org/)
