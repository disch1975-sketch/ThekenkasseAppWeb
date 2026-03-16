import requests
from datetime import datetime, timedelta
import os
from supabase import create_client

# Supabase Verbindung
supabase_url = os.environ["SUPABASE_URL"]
supabase_key = os.environ["SUPABASE_KEY"]

supabase = create_client(supabase_url, supabase_key)

ligen = ["BK","A1","A2","B1","B2","B3","C1","C2"]
max_tage_zurueck = 50

print("Lade vorhandene Dateien aus Supabase...")

# vorhandene Dateien im Bucket laden
try:
    bucket_files = supabase.storage.from_("tabellen").list()
    vorhandene_dateien = [f["name"] for f in bucket_files]
except Exception as e:
    print("Fehler beim Laden:", e)
    vorhandene_dateien = []

print("Gefundene Dateien:", len(vorhandene_dateien))


for liga in ligen:

    print("\n---- Prüfe Liga:", liga, "----")

    gefunden = False

    for tage in range(max_tage_zurueck):

        datum = (datetime.today() - timedelta(days=tage)).strftime("%d.%m.%Y")

        filename = f"{liga}-Tabelle-HP-{datum}.jpg"
        url = f"http://www.dartligafulda.de/wp-content/uploads/{filename}"

        print("Prüfe:", url)

        try:
            r = requests.get(url, timeout=10)
        except:
            continue

        # prüfen ob Bild existiert und nicht leer ist
        if r.status_code == 200 and len(r.content) > 1000:

            print("Download erfolgreich:", filename)

            # alte Tabellen dieser Liga löschen
            zu_loeschen = [f for f in vorhandene_dateien if f.startswith(liga)]

            if zu_loeschen:
                print("Lösche alte Tabellen:", zu_loeschen)
                try:
                    supabase.storage.from_("tabellen").remove(zu_loeschen)
                except Exception as e:
                    print("Fehler beim Löschen:", e)

            # Bild lokal speichern
            with open(filename, "wb") as f:
                f.write(r.content)

            # Upload zu Supabase
            try:
                with open(filename, "rb") as f:
                    supabase.storage.from_("tabellen").upload(
                        path=filename,
                        file=f,
                        file_options={
                            "content-type": "image/jpeg",
                            "upsert": "true"
                        }
                    )

                print("Neu hochgeladen:", filename)

            except Exception as e:
                print("Upload Fehler:", e)

            # lokale Datei löschen
            os.remove(filename)

            gefunden = True
            break

    if not gefunden:
        print("Keine Tabelle gefunden für Liga:", liga)

print("\nScript beendet.")
