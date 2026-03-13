import requests
from datetime import datetime, timedelta
import os
from supabase import create_client

# Supabase Verbindung
supabase_url = os.environ["SUPABASE_URL"]
supabase_key = os.environ["SUPABASE_KEY"]
supabase = create_client(supabase_url, supabase_key)

ligen = ["BK","A1","A2","B1","B2","B3","C1","C2"]
max_tage_zurueck = 60

for liga in ligen:
    gefunden = False
    for tage in range(max_tage_zurueck):
        datum = (datetime.today() - timedelta(days=tage)).strftime("%d.%m.%Y")
        filename = f"{liga}-Tabelle-HP-{datum}.jpg"
        url = f"http://www.dartligafulda.de/wp-content/uploads/{filename}"
        
        print("Prüfe:", url)
        r = requests.get(url)
        if r.status_code == 200:
            # Bild lokal speichern
            with open(filename, "wb") as f:
                f.write(r.content)

            # Alte Datei in Supabase löschen, falls vorhanden
            try:
                supabase.storage.from_("tabellen").remove([filename])
                print("Altes Bild gelöscht:", filename)
            except:
                pass  # falls Datei noch nicht existiert

            # Bild hochladen
            with open(filename, "rb") as f:
                supabase.storage.from_("tabellen").upload(filename, f)
            
            os.remove(filename)
            print("Hochgeladen:", filename)
            gefunden = True
            break
    if not gefunden:
        print("Kein Bild gefunden für Liga:", liga)
