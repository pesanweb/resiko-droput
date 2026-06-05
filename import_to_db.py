"""
Script untuk import data CSV ke PostgreSQL
Jalankan: python import_to_db.py
"""

import pandas as pd
from sqlalchemy import create_engine, text
import sys

# Koneksi ke PostgreSQL
DB_HOST = "localhost"
DB_PORT = "5432"
DB_USER = "postgres"
DB_PASSWORD = "mysecretpassword"
DB_NAME = "student_dropout"

def create_connection():
    """Buat koneksi ke PostgreSQL"""
    try:
        engine = create_engine(f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")
        print(f"✅ Berhasil terhubung ke database {DB_NAME}")
        return engine
    except Exception as e:
        print(f"❌ Gagal terhubung ke database: {e}")
        print("\nPastikan Docker sudah jalan:")
        print("  docker-compose up -d")
        sys.exit(1)

def create_table(engine):
    """Buat tabel data di PostgreSQL"""
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS "data" (
        "Marital_status" INTEGER,
        "Application_mode" INTEGER,
        "Application_order" INTEGER,
        "Course" INTEGER,
        "Daytime_evening_attendance" INTEGER,
        "Previous_qualification" INTEGER,
        "Previous_qualification_grade" FLOAT,
        "Nacionality" INTEGER,
        "Mothers_qualification" INTEGER,
        "Fathers_qualification" INTEGER,
        "Mothers_occupation" INTEGER,
        "Fathers_occupation" INTEGER,
        "Admission_grade" FLOAT,
        "Displaced" INTEGER,
        "Educational_special_needs" INTEGER,
        "Debtor" INTEGER,
        "Tuition_fees_up_to_date" INTEGER,
        "Gender" INTEGER,
        "Scholarship_holder" INTEGER,
        "Age_at_enrollment" INTEGER,
        "International" INTEGER,
        "Curricular_units_1st_sem_credited" INTEGER,
        "Curricular_units_1st_sem_enrolled" INTEGER,
        "Curricular_units_1st_sem_evaluations" INTEGER,
        "Curricular_units_1st_sem_approved" INTEGER,
        "Curricular_units_1st_sem_grade" FLOAT,
        "Curricular_units_1st_sem_without_evaluations" INTEGER,
        "Curricular_units_2nd_sem_credited" INTEGER,
        "Curricular_units_2nd_sem_enrolled" INTEGER,
        "Curricular_units_2nd_sem_evaluations" INTEGER,
        "Curricular_units_2nd_sem_approved" INTEGER,
        "Curricular_units_2nd_sem_grade" FLOAT,
        "Curricular_units_2nd_sem_without_evaluations" INTEGER,
        "Unemployment_rate" FLOAT,
        "Inflation_rate" FLOAT,
        "GDP" FLOAT,
        "Status" VARCHAR(20)
    );
    """
    
    with engine.connect() as conn:
        conn.execute(text(create_table_sql))
        conn.commit()
    print("✅ Tabel 'data' berhasil dibuat")

def import_data(engine):
    """Import data CSV ke PostgreSQL"""
    # Load CSV
    print("📂 Loading data/data.csv...")
    df = pd.read_csv('data/data.csv', sep=';')
    print(f"   Jumlah baris: {len(df)}")
    print(f"   Kolom: {len(df.columns)}")
    
    # Drop tabel lama jika ada
    with engine.connect() as conn:
        conn.execute(text('DROP TABLE IF EXISTS "data"'))
        conn.commit()
    
    # Import ke PostgreSQL
    print("📤 Importing ke PostgreSQL...")
    df.to_sql('data', engine, if_exists='replace', index=False)
    
    # Verifikasi
    with engine.connect() as conn:
        result = conn.execute(text('SELECT COUNT(*) FROM "data"'))
        count = result.scalar()
    
    print(f"✅ Berhasil import {count} baris ke tabel 'data'")
    
    # Tampilkan distribusi status
    print("\n📊 Distribusi Status:")
    status_counts = df['Status'].value_counts()
    for status, count in status_counts.items():
        percentage = count / len(df) * 100
        print(f"   {status}: {count} ({percentage:.1f}%)")

def main():
    print("=" * 60)
    print("IMPORT DATA KE POSTGRESQL")
    print("=" * 60)
    
    # Koneksi ke database
    engine = create_connection()
    
    # Buat tabel
    create_table(engine)
    
    # Import data
    import_data(engine)
    
    print("\n" + "=" * 60)
    print("SELESAI!")
    print("=" * 60)
    print("\nSekarang buka Metabase di http://localhost:3000")
    print("Login: root@mail.com / root123")
    print("\nBuat SQL Query baru dan jalankan query dari:")
    print("  queries/dashboard_queries.sql")

if __name__ == "__main__":
    main()
