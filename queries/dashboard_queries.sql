-- ============================================================
-- METABASE DASHBOARD QUERIES
-- Student Dropout Prediction - Perusahaan Edutech
-- ============================================================
-- NOTE: Dataset dari UCI Machine Learning Repository
--       Kode prodi (Course) adalah anonim, bukan nama asli
--       Mapping di bawah bersifat ilustrasi berdasarkan kode
--
-- PENTING - PENDEKATAN KLASSIFIKASI:
-- - Model dilatih menggunakan BINARY CLASSIFICATION (Dropout vs Graduate)
-- - Data Enrolled TIDAK digunakan untuk training, hanya untuk inferensi
-- - Dashboard queries di bawah menggunakan SELURUH data (termasuk Enrolled)
--   untuk analisis eksplorasi dan monitoring


-- ============================================================
-- QUERY 1: RINGKASAN KESELURUHAN
-- Tujuan: Melihat distribusi status mahasiswa
-- ============================================================
SELECT 
    "Status",
    COUNT(*) as "Jumlah_Mahasiswa",
    ROUND(COUNT(*)::numeric * 100.0 / (SELECT COUNT(*) FROM "data"), 2) as "Persentase"
FROM "data"
GROUP BY "Status"
ORDER BY "Jumlah_Mahasiswa" DESC;


-- ============================================================
-- QUERY 2: DROPOUT RATE - FAKTOR FINANSIAL
-- Tujuan: Menganalisis pengaruh faktor finansial terhadap dropout
-- ============================================================
SELECT 
    CASE WHEN "Debtor" = 1 THEN 'Berutang' ELSE 'Tidak Berutang' END as "Status_Debitur",
    CASE WHEN "Tuition_fees_up_to_date" = 1 THEN 'Tertib' ELSE 'Tidak Tertib' END as "Status_Pembayaran",
    CASE WHEN "Scholarship_holder" = 1 THEN 'Punya Beasiswa' ELSE 'Tidak Ada Beasiswa' END as "Status_Beasiswa",
    "Status" as "Status_Mahasiswa",
    COUNT(*) as "Jumlah"
FROM "data"
GROUP BY "Debtor", "Tuition_fees_up_to_date", "Scholarship_holder", "Status"
ORDER BY "Debtor", "Tuition_fees_up_to_date", "Scholarship_holder", "Status";


-- ============================================================
-- QUERY 3: PERFORMA AKADEMIK PER STATUS
-- Tujuan: Membandingkan rata-rata performa akademik per status
-- ============================================================
SELECT 
    "Status",
    ROUND(AVG("Admission_grade")::numeric, 2) as "Rata_Nilai_Masuk",
    ROUND(AVG("Curricular_units_1st_sem_grade")::numeric, 2) as "Rata_Nilai_Sem1",
    ROUND(AVG("Curricular_units_2nd_sem_grade")::numeric, 2) as "Rata_Nilai_Sem2",
    ROUND(AVG("Curricular_units_1st_sem_approved")::numeric, 2) as "Rata_Unit_Lulus_Sem1",
    ROUND(AVG("Curricular_units_2nd_sem_approved")::numeric, 2) as "Rata_Unit_Lulus_Sem2"
FROM "data"
GROUP BY "Status";


-- ============================================================
-- QUERY 4: DROPOUT PER PROGRAM STUDI (SUDAH DIBERI NAMA)
-- Tujuan: Mengetahui prodi mana yang dropout rate tertinggi
-- Catatan: Kode prodi dari dataset UCI adalah anonim
--          Mapping di bawah bersifat ilustrasi
-- ============================================================
SELECT 
    "Course" as "Kode_Prodi",
    CASE 
        WHEN "Course" = 33 THEN 'Teknologi Informasi'
        WHEN "Course" = 171 THEN 'Teknik Biomedis'
        WHEN "Course" = 8014 THEN 'Manajemen Bisnis'
        WHEN "Course" = 9070 THEN 'Pendidikan'
        WHEN "Course" = 9085 THEN 'Jurnalistik'
        WHEN "Course" = 9119 THEN 'Keperawatan'
        WHEN "Course" = 9130 THEN 'Biologi'
        WHEN "Course" = 9147 THEN 'Hukum'
        WHEN "Course" = 9238 THEN 'Teknik Informatika'
        WHEN "Course" = 9254 THEN 'Ekonomi'
        WHEN "Course" = 9500 THEN 'Sistem Informasi'
        WHEN "Course" = 9556 THEN 'Komunikasi'
        WHEN "Course" = 9670 THEN 'Psikologi'
        WHEN "Course" = 9773 THEN 'Administrasi Bisnis'
        WHEN "Course" = 9853 THEN 'Manajemen Olahraga'
        WHEN "Course" = 9991 THEN 'Hubungan Internasional'
        ELSE 'Prodi Lainnya (' || "Course" || ')'
    END as "Nama_Prodi",
    COUNT(*) as "Total_Mahasiswa",
    SUM(CASE WHEN "Status" = 'Dropout' THEN 1 ELSE 0 END) as "Jumlah_Dropout",
    ROUND(SUM(CASE WHEN "Status" = 'Dropout' THEN 1 ELSE 0 END)::numeric * 100.0 / COUNT(*), 2) as "Dropout_Rate_Persen"
FROM "data"
GROUP BY "Course"
ORDER BY "Dropout_Rate_Persen" DESC;


-- ============================================================
-- QUERY 5: DROPOUT PER KELOMPOK USIA
-- Tujuan: Mengetahui kelompok usia mana yang paling berisiko
-- ============================================================
SELECT 
    CASE 
        WHEN "Age_at_enrollment" < 20 THEN '1. < 20 tahun'
        WHEN "Age_at_enrollment" BETWEEN 20 AND 25 THEN '2. 20-25 tahun'
        WHEN "Age_at_enrollment" BETWEEN 26 AND 30 THEN '3. 26-30 tahun'
        WHEN "Age_at_enrollment" BETWEEN 31 AND 40 THEN '4. 31-40 tahun'
        ELSE '5. > 40 tahun'
    END as "Kelompok_Umur",
    COUNT(*) as "Total",
    SUM(CASE WHEN "Status" = 'Dropout' THEN 1 ELSE 0 END) as "Jumlah_Dropout",
    ROUND(SUM(CASE WHEN "Status" = 'Dropout' THEN 1 ELSE 0 END)::numeric * 100.0 / COUNT(*), 2) as "Dropout_Rate_Persen"
FROM "data"
GROUP BY "Kelompok_Umur"
ORDER BY MIN("Age_at_enrollment");


-- ============================================================
-- QUERY 6: DROPOUT PER JENIS KELAMIN
-- Tujuan: Membandingkan dropout rate laki-laki vs perempuan
-- ============================================================
SELECT 
    CASE WHEN "Gender" = 0 THEN 'Perempuan' ELSE 'Laki-laki' END as "Jenis_Kelamin",
    COUNT(*) as "Total",
    SUM(CASE WHEN "Status" = 'Dropout' THEN 1 ELSE 0 END) as "Jumlah_Dropout",
    ROUND(SUM(CASE WHEN "Status" = 'Dropout' THEN 1 ELSE 0 END)::numeric * 100.0 / COUNT(*), 2) as "Dropout_Rate_Persen"
FROM "data"
GROUP BY "Gender";


-- ============================================================
-- QUERY 7: PENGARUH BEASISWA
-- Tujuan: Mengukur dampak beasiswa terhadap retensi mahasiswa
-- ============================================================
SELECT 
    CASE WHEN "Scholarship_holder" = 1 THEN 'Punya Beasiswa' ELSE 'Tidak Ada Beasiswa' END as "Status_Beasiswa",
    COUNT(*) as "Total",
    SUM(CASE WHEN "Status" = 'Dropout' THEN 1 ELSE 0 END) as "Jumlah_Dropout",
    ROUND(SUM(CASE WHEN "Status" = 'Dropout' THEN 1 ELSE 0 END)::numeric * 100.0 / COUNT(*), 2) as "Dropout_Rate_Persen"
FROM "data"
GROUP BY "Scholarship_holder";


-- ============================================================
-- QUERY 8: PENGARUH STATUS DEBITUR
-- Tujuan: Mengukur dampak status berutang terhadap dropout
-- ============================================================
SELECT 
    CASE WHEN "Debtor" = 1 THEN 'Berutang (Debitur)' ELSE 'Tidak Berutang' END as "Status_Debitur",
    COUNT(*) as "Total",
    SUM(CASE WHEN "Status" = 'Dropout' THEN 1 ELSE 0 END) as "Jumlah_Dropout",
    ROUND(SUM(CASE WHEN "Status" = 'Dropout' THEN 1 ELSE 0 END)::numeric * 100.0 / COUNT(*), 2) as "Dropout_Rate_Persen"
FROM "data"
GROUP BY "Debtor";


-- ============================================================
-- QUERY 9: ANALISIS KEGAGALAN UNIT PER SEMESTER
-- Tujuan: Membandingkan jumlah unit yang gagal antara semester 1 dan 2
-- ============================================================
SELECT 
    "Status",
    ROUND(AVG("Curricular_units_1st_sem_enrolled" - "Curricular_units_1st_sem_approved")::numeric, 2) as "Rata_Unit_Gagal_Sem1",
    ROUND(AVG("Curricular_units_2nd_sem_enrolled" - "Curricular_units_2nd_sem_approved")::numeric, 2) as "Rata_Unit_Gagal_Sem2",
    ROUND(AVG("Curricular_units_1st_sem_without_evaluations")::numeric, 2) as "Rata_Tanpa_Evaluasi_Sem1",
    ROUND(AVG("Curricular_units_2nd_sem_without_evaluations")::numeric, 2) as "Rata_Tanpa_Evaluasi_Sem2"
FROM "data"
GROUP BY "Status";


-- ============================================================
-- QUERY 10: IDENTIFIKASI MAHASISWA BERISIKO TINGGI
-- Tujuan: Menemukan mahasiswa dengan kombinasi faktor risiko tinggi
-- ============================================================
SELECT 
    "Debtor",
    "Tuition_fees_up_to_date",
    "Scholarship_holder",
    "Curricular_units_1st_sem_approved",
    "Curricular_units_2nd_sem_approved",
    "Admission_grade",
    CASE 
        WHEN "Debtor" = 1 AND "Tuition_fees_up_to_date" = 0 THEN 'SANGAT TINGGI'
        WHEN "Debtor" = 1 OR "Tuition_fees_up_to_date" = 0 THEN 'TINGGI'
        WHEN "Curricular_units_1st_sem_approved" < 4 THEN 'SEDANG'
        ELSE 'RENDAH'
    END as "Tingkat_Risiko"
FROM "data"
WHERE "Status" = 'Dropout'
ORDER BY 
    CASE 
        WHEN "Debtor" = 1 AND "Tuition_fees_up_to_date" = 0 THEN 1
        WHEN "Debtor" = 1 OR "Tuition_fees_up_to_date" = 0 THEN 2
        WHEN "Curricular_units_1st_sem_approved" < 4 THEN 3
        ELSE 4
    END
LIMIT 50;


-- ============================================================
-- QUERY 11: PERBANDINGAN DROPOUT VS GRADUATE
-- Tujuan: Komparasi statistik antara mahasiswa dropout dan graduate
-- ============================================================
SELECT 
    'Dropout' as "Kategori",
    COUNT(*) as "Jumlah",
    ROUND(AVG("Age_at_enrollment")::numeric, 1) as "Rata_Usia",
    ROUND(AVG("Admission_grade")::numeric, 1) as "Rata_Nilai_Masuk",
    ROUND(AVG("Curricular_units_1st_sem_approved")::numeric, 1) as "Rata_Unit_Lulus_Sem1",
    ROUND(AVG("Curricular_units_2nd_sem_approved")::numeric, 1) as "Rata_Unit_Lulus_Sem2",
    ROUND(AVG("Debtor")::numeric * 100, 1) as "Persen_Debitur",
    ROUND(AVG("Scholarship_holder")::numeric * 100, 1) as "Persen_Beasiswa"
FROM "data" WHERE "Status" = 'Dropout'
UNION ALL
SELECT 
    'Graduate' as "Kategori",
    COUNT(*) as "Jumlah",
    ROUND(AVG("Age_at_enrollment")::numeric, 1) as "Rata_Usia",
    ROUND(AVG("Admission_grade")::numeric, 1) as "Rata_Nilai_Masuk",
    ROUND(AVG("Curricular_units_1st_sem_approved")::numeric, 1) as "Rata_Unit_Lulus_Sem1",
    ROUND(AVG("Curricular_units_2nd_sem_approved")::numeric, 1) as "Rata_Unit_Lulus_Sem2",
    ROUND(AVG("Debtor")::numeric * 100, 1) as "Persen_Debitur",
    ROUND(AVG("Scholarship_holder")::numeric * 100, 1) as "Persen_Beasiswa"
FROM "data" WHERE "Status" = 'Graduate';


-- ============================================================
-- QUERY 12: PENGARUH KONDISI EKONOMI
-- Tujuan: Menganalisis apakah kondisi ekonomi mempengaruhi dropout
-- ============================================================
SELECT 
    CASE 
        WHEN "GDP" < 0 THEN '1. Resesi (GDP < 0)'
        WHEN "GDP" BETWEEN 0 AND 2 THEN '2. Stabil (GDP 0-2)'
        ELSE '3. Tumbuh (GDP > 2)'
    END as "Kondisi_Ekonomi",
    COUNT(*) as "Total",
    SUM(CASE WHEN "Status" = 'Dropout' THEN 1 ELSE 0 END) as "Jumlah_Dropout",
    ROUND(SUM(CASE WHEN "Status" = 'Dropout' THEN 1 ELSE 0 END)::numeric * 100.0 / COUNT(*), 2) as "Dropout_Rate_Persen"
FROM "data"
GROUP BY "Kondisi_Ekonomi"
ORDER BY "Dropout_Rate_Persen" DESC;
