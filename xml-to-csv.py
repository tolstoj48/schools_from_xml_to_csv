import xml.etree.ElementTree as Xet
import pandas as pd
import sys


class XmlToCsvConverter:
    def __init__(self, source_file, address=None) -> None:
        self.cols = ["skola_nazev_typu", "skola_druh_typ",
                     "zrizovatel", "ulice", "obec", "obec_2"]
        self.rows = []
        self.address = address
        self.xmlparse = Xet.parse(source_file)
        self.root = self.xmlparse.getroot()
        self.subjekty = self.root.findall("PravniSubjekt")

    def append_row(self, skola_nazev_typu, skola_druh_typ, zrizovatel, adr_1, adr_2, adr_3):
        try:
            self.rows.append({
                "skola_nazev_typu": skola_nazev_typu,
                "skola_druh_typ": skola_druh_typ,
                "zrizovatel": zrizovatel,
                "ulice": adr_1,
                "obec": adr_2,
                "obec_2": adr_3
            })
        except Exception as e:
            print(
                f"Something went wrong with the appending of the results to the list: {e}")
            sys.exit(1)

    def convert(self):
        try:
            for subjekt in self.subjekty:
                zarizeni = subjekt.findall("SkolyZarizeni")
                reditelstvi = subjekt.find("Reditelstvi")
                reditelstvi_nazev = reditelstvi.find("RedPlnyNazev")
                zrizovatel = reditelstvi_nazev.text
                for skola in zarizeni:
                    konkretni_skoly = skola.findall("SkolaZarizeni")
                    for konkretni_skola in konkretni_skoly:
                        skola_nazev_typu = konkretni_skola.find(
                            "SkolaPlnyNazev").text
                        skola_druh_typ = konkretni_skola.find(
                            "SkolaDruhTyp").text
                        misto = konkretni_skola.find("SkolaMistaVykonuCinnosti").find(
                            "SkolaMistoVykonuCinnosti")
                        adr_1 = misto.find("MistoAdresa1").text
                        adr_2 = misto.find("MistoAdresa2").text
                        if misto.find("MistoAdresa3").text:
                            adr_3 = misto.find("MistoAdresa3").text
                        else:
                            adr_3 = ""
                        # Searching base on user city/village name or postcode
                        if self.address:
                            if adr_2.find(self.address) >= 0 or adr_3.find(self.address) >= 0:
                                self.append_row(
                                    skola_nazev_typu, skola_druh_typ, zrizovatel, adr_1, adr_2, adr_3)
                        # Simple conversion of xml to csv
                        else:
                            self.append_row(
                                skola_nazev_typu, skola_druh_typ, zrizovatel, adr_1, adr_2, adr_3)
                        # Pandas dataframe
                        df = pd.DataFrame(self.rows, columns=self.cols)
                        # Writing dataframe to csv
                        df.to_csv('output.csv')
        except Exception as e:
            print(f"Something went wrong in the converter method: {e}")


if __name__ == "__main__":
    try:
        # Two arguments provided by the user - search base on city/village/postcode
        if len(sys.argv) == 3:
            converter = XmlToCsvConverter(sys.argv[1], sys.argv[2])
        # One argument provided by the user - simple conversion
        elif len(sys.argv) == 2:
            converter = XmlToCsvConverter(sys.argv[1])
        # More arguments - rase error
        elif len(sys.argv) > 3:
            raise SystemExit(2)
        # Conversion itself
        converter.convert()
    except FileNotFoundError:
        print("The file doesn´t exist!")
    except SystemExit as ex:
        if SystemExit == 2:
            print(
                "Don´t send more then two arguments, please: 1. name of the source file, 2. address")
