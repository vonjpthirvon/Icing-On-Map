# Icing On Map

Streamlit-sovellus, joka visualisoi jään kertymistä sääasemilla Suomessa. Sovellus hakee jäätämishavaintodataa FMI:n OpenData-rajapinnasta, laskee jään kertymän ja näyttää tulokset interaktiivisella kartalla ja kuvaajina.

## Ominaisuudet

- Valitse asemat ja aikaväli
- Näyttää jään kertymä kartalla havaintoasemilla millimetreinä kertynyttä jäätä (Folium)
- Yksittäisten asemien kertymäkuvaajan voi saada myös esille aikasarjana (Matplotlib)
- Automaattinen datan haku ja suodatus

## Lähteitä:
- FMI OpenData API: http://opendata.fmi.fi
- Jään kertymän laskenta perustuu julkaisuun: https://doi.org/10.1175/JAM2535.1

## Asennus

## Asennus Conda-ympäristöllä

Voit luoda ja aktivoida conda-ympäristön seuraavilla komennoilla:

```bash
# Luo uusi conda-ympäristö
conda env create -f environment.yml

# Aktivoi ympäristö
conda activate icing-on-map-env

## Asennus pip-ympäristöllä

Voit luoda ja aktivoida virtuaaliympäristön sekä asentaa riippuvuudet seuraavasti:

```bash
# Luo virtuaaliympäristö (valinnainen mutta suositeltava)
python -m venv venv
source venv/bin/activate  # tai Windowsissa: venv\Scripts\activate

# Asenna riippuvuudet
pip install -r requirements.txt


## Käyttö

```bash
streamlit run main.py

## Asennus Conda-ympäristöllä

Voit luoda ja aktivoida conda-ympäristön seuraavilla komennoilla:

```bash
# Luo uusi conda-ympäristö
conda env create -f environment.yml

# Aktivoi ympäristö
conda activate icing-on-map-env
```