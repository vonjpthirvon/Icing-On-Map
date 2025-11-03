# Icing On Map

Streamlit-sovellus, joka visualisoi jään kertymistä sääasemilla Suomessa. Sovellus hakee jäätämishavaintodataa FMI:n OpenData-rajapinnasta [1], laskee jään kertymän ja näyttää tulokset interaktiivisella kartalla ja kuvaajina. Jään kertymä lasketaan menetelmällä, joka on esitetty julkaisussa [2].

Kartalla esitetään jään kokonaiskertymä millimetreinä valitun ajanjakson aikana eli kertymä loppuhetkellä. Kertymä ei ota huomioon mahdollisesti ajanjakson aikana tapahtuvaa jään sulamista.

Kartan alapuolelle on mahdollista saada näkyville jään kertymäkuvaaja valitulle ajanjaksolle. Kuvaajassa ylimmässä paneelissa on jään kertymät kahdella eri menetelmällä laskettuna: menetelmä [2] vihreä käyrä ja punainen käyrä [2] lisäksi keskiarvosuodatusta ja kynnystystä vesisateen poistamiseksi. Toinen paneeli laitteen raakasignaali MSO-taajuus (fzfreq) ja tästä laskettu 10 minuutin minimitaajuus (fz10min). Kolmas paneeli NFC (net frequency change) eli taajuuden muutoksesta lasketut hetkelliset jään kertymät yksikössä mm/1min tavallinen ja keskiarvosuodatettu. Neljäs ja alin paneelit NFC eli netto taajuuden muutokset tavallisella menetelmällä [2] sekä keskiarvosuodatuksella, respectively.

## Ominaisuudet

- Valitse asemat ja aikaväli
- Näyttää jään kertymä kartalla havaintoasemilla millimetreinä kertynyttä jäätä (Folium)
- Yksittäisten asemien kertymäkuvaajan voi saada myös esille aikasarjana (Matplotlib)
- Automaattinen datan haku ja suodatus

## Lähteitä:
- [1] FMI OpenData API: http://opendata.fmi.fi
- [2] Jään kertymän laskenta perustuu julkaisuun: https://doi.org/10.1175/JAM2535.1 "Ryerson & Ramsay (2006)"

## Asennus Conda-ympäristöllä

Voit luoda ja aktivoida conda-ympäristön seuraavilla komennoilla:

```bash
# Luo uusi conda-ympäristö
conda env create -f environment.yml

# Aktivoi ympäristö
conda activate icing-on-map-env
```
## Asennus pip-ympäristöllä

Voit luoda ja aktivoida virtuaaliympäristön sekä asentaa riippuvuudet seuraavasti:

```bash
# Luo virtuaaliympäristö (valinnainen mutta suositeltava)
python -m venv venv
source venv/bin/activate  # tai Windowsissa: venv\Scripts\activate

# Asenna riippuvuudet
pip install -r requirements.txt
```

## Käyttö

```bash
streamlit run main.py
```
avaa selaimeen http://localhost:8501 sovelman