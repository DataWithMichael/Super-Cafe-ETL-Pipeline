from etl.db_utils import connect_db

def test_local():
    print("🔹 Testing Local DB...")
    try:
        with connect_db() as conn:
            cur = conn.cursor()
            cur.execute("SELECT 1;")
            print("✅ Local DB connection works!")
    except Exception as e:
        print("❌ Local DB connection failed:", e)

# def test_redshift():
#     print("🔹 Testing AWS Redshift...")
#     try:
#         with connect_redshift() as conn:
#             cur = conn.cursor()
#             cur.execute("SELECT current_database();")
#             db_name = cur.fetchone()[0]
#             print(f"✅ Redshift connection works! Connected to: {db_name}")
#     except Exception as e:
#         print("❌ Redshift connection failed:", e)

if __name__ == "__main__":
    test_local()
    # test_redshift()
