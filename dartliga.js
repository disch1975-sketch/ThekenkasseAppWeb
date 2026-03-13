window.dartLiga = {

    findeBild: async function (code) {

        const url = "https://www.dartligafulda.de/wp-content/uploads/";

        const heute = new Date();

        for (let i = 0; i < 14; i++) {

            let d = new Date();
            d.setDate(heute.getDate() - i);

            let tag = String(d.getDate()).padStart(2, '0');
            let monat = String(d.getMonth() + 1).padStart(2, '0');
            let jahr = d.getFullYear();

            let datum = tag + "." + monat + "." + jahr;

            let bild = `${url}${code}-Tabelle-HP-${datum}.jpg`;

            let ok = await new Promise(resolve => {

                let img = new Image();

                img.onload = () => resolve(true);
                img.onerror = () => resolve(false);

                img.src = bild;

            });

            if (ok) {

                return {
                    url: bild,
                    datum: datum
                };

            }

        }

        return null;

    }

};