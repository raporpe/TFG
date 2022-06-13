import psycopg2
from mac_vendor_lookup import MacLookup, VendorNotFoundError
import os

def vendor(mac):
    try:
        return MacLookup().lookup(mac)
    except VendorNotFoundError:
        return None

# Get the database password from the environment variable
db_password = os.environ['DB_PASSWORD']

conn = psycopg2.connect("host=tfg-server.raporpe.dev dbname=tfg user=postgres password=" + db_password)
cur = conn.cursor()

cur.execute("SELECT distinct station_mac FROM data_frames")
rows = cur.fetchall()

not_fake = []

for row in rows:
    vnd = vendor(row[0])
    if vnd is not None:
        not_fake.append((row[0], vnd))

print(not_fake)
print(len(not_fake))