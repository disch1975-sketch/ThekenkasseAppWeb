import requests
from datetime import datetime
import os
from supabase import create_client

supabase_url = os.environ["SUPABASE_URL"]
supabase_key = os.environ["SUPABASE_KEY"]

supabase = create_client(supabase_url, supabase_key)

ligen = ["BK","A1","A2","B1","B2","B3","C1","C2"]

datum = datetime.today().strftime("%d.%m.%Y")

for liga in ligen:

    filename = f"{liga}-Tabelle-HP-{datum}.jpg"
    url = f"http://www.dartligafulda.de/wp-content/uploads/{filename}"

    print("Lade:", url)

    r = requests.get(url)

    if r.status_code == 200:

        with open(filename,"wb") as f:
            f.write(r.content)

        with open(filename,"rb") as f:
            supabase.storage.from_("tabellen").upload(filename,f,{"upsert":True})

        os.remove(filename)

        print("Hochgeladen:", filename)

    else:
        print("Nicht gefunden:", filename)
