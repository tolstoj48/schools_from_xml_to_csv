"""
Číselník pro SkolaDruhTyp:
http://stistko.uiv.cz/katalog/cslnk.asp?aad=&aak=&aap=on&idc=AKDT&ciselnik=Druhy+a+typy+%9Akol+a+%9Akolsk%FDch+za%F8%EDzen%ED+%28nov%E9%29&poznamka=
Jde o číselník typu školy
"""

# Importing the required libraries
import xml.etree.ElementTree as Xet
import pandas as pd
import sys

class XmlToCsvConverter:
    def __init__(self, source_file, address = None) -> None:
        self.cols = ["skola_nazev_typu", "skola_druh_typ", "zrizovatel", "ulice", "obec", "obec_2"]
        self.rows = []
        self.address = address
        # Parsing the XML file
        self.xmlparse = Xet.parse(source_file)
        self.root = self.xmlparse.getroot()
        self.subjekty = self.root.findall("PravniSubjekt")
   
    def append_row(self, skola_nazev_typu, skola_druh_typ, zrizovatel, adr_1, adr_2, adr_3):
        self.rows.append({
            "skola_nazev_typu": skola_nazev_typu,
            "skola_druh_typ": skola_druh_typ,
            "zrizovatel": zrizovatel,
            "ulice": adr_1,
            "obec": adr_2,
            "obec_2": adr_3
        })
    
    def convert(self):
        for subjekt in self.subjekty:
            zarizeni = subjekt.findall("SkolyZarizeni")
            reditelstvi = subjekt.find("Reditelstvi")
            reditelstvi_nazev = reditelstvi.find("RedPlnyNazev")
            zrizovatel = reditelstvi_nazev.text
            for skola in zarizeni :
                konkretni_skoly = skola.findall("SkolaZarizeni")
                for konkretni_skola in konkretni_skoly:
                    skola_nazev_typu = konkretni_skola.find("SkolaPlnyNazev").text
                    skola_druh_typ = konkretni_skola.find("SkolaDruhTyp").text
                    # TO DO: There might be more places
                    misto = konkretni_skola.find("SkolaMistaVykonuCinnosti").find("SkolaMistoVykonuCinnosti")
                    adr_1 = misto.find("MistoAdresa1").text
                    adr_2 = misto.find("MistoAdresa2").text
                    adr_3 = misto.find("MistoAdresa3").text
                    if self.address:
                        if adr_2.find(self.address) >= 0:
                            self.append_row(skola_nazev_typu, skola_druh_typ, zrizovatel, adr_1, adr_2, adr_3)
                    else:
                        self.append_row(skola_nazev_typu, skola_druh_typ, zrizovatel, adr_1, adr_2, adr_3)
                    df = pd.DataFrame(self.rows, columns=self.cols)
  
                    # Writing dataframe to csv
                    df.to_csv('output.csv')

if __name__ == "__main__":
    try:
        if len(sys.argv) == 3:
            converter = XmlToCsvConverter(sys.argv[1], sys.argv[2])
        elif len(sys.argv) == 2:
            converter = XmlToCsvConverter(sys.argv[1])
        elif len(sys.argv) > 3:
            raise SystemExit(2)
        converter.convert()
    except FileNotFoundError:
        print("The file doesn´t exist!")
    except SystemExit:
        print("Don´t send more then two arguments, please: 1. name of the source file, 2. address")