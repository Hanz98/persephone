"""
XML Builder for EH_PEH02A Agricultural Data Service
"""

from dataclasses import dataclass, field
from datetime import date
from decimal import Decimal
from enum import Enum
from typing import List, Optional, Union
from xml.etree.ElementTree import Element, SubElement, tostring


class TypRequest(Enum):
    """Request type enumeration"""

    K = "K"  # Control data
    S = "S"  # Statistics data
    B = "B"  # Balance data


class RezimVolani(Enum):
    """Call mode enumeration"""

    P = "P"  # Production call
    T = "T"  # Test call


class RozsahKod(Enum):
    """Data scope code enumeration"""

    OSEVY = "O"  # Crops
    HNOJIVA = "H"  # Fertilizer applications
    PASTVY = "P"  # Grazing
    SKLIZNE = "S"  # Harvests


class TypPlodiny(Enum):
    """Crop type enumeration"""

    HLA = "HLA"  # Main crop
    VED = "VED"  # Secondary crop
    POM = "POM"  # Helper crop
    POD = "POD"  # Undersown crop
    KRY = "KRY"  # Cover crop


class TypAplikace(Enum):
    """Application type enumeration"""

    H = "H"  # Fertilization
    K = "K"  # Sludge
    P = "P"  # Grazing (as manure application)
    S = "S"  # Auxiliary soil substances/biostimulants/substrates


class DobaZapraveni(Enum):
    """Cultivation time enumeration"""

    IHNED = "I"  # Immediately with application
    H12 = "12"  # Up to 12 hours after application
    H24 = "24"  # 12 to 24 hours after application
    H48 = "48"  # 24 to 48 hours after application
    H48_PLUS = "48+"  # More than 48 hours after application


class MernaJednotka(Enum):
    """Measurement unit enumeration"""

    T = "t"  # Tons
    KG = "kg"  # Kilograms
    L = "l"  # Liters


class MetodaZivin(Enum):
    """Nutrient method enumeration"""

    PRVKOVA = "P"  # Elemental form
    OXIDOVA = "O"  # Oxide form


class TypProduktu(Enum):
    """Product type enumeration"""

    H = "H"  # Main
    V = "V"  # Secondary


@dataclass
class RozsahDat:
    """Data scope definition"""

    kod: RozsahKod


@dataclass
class Vymera:
    """Area measurement"""

    vymera: Decimal
    platnost_od: date
    platnost_do: Optional[date] = None

    def __post_init__(self) -> None:
        # Ensure 2 decimal places precision
        self.vymera = round(self.vymera, 2)


@dataclass
class Pestovani:
    """Crop cultivation data"""

    id_pestovani: str
    id_plodina: int
    viceleta: bool
    zahajeni_pestovani: date
    platnost_od: date
    id_uzitkovy_smer: Optional[int] = None
    hosp_rok: Optional[int] = None
    typ_plodiny: Optional[TypPlodiny] = None
    ukonceni_pestovani: Optional[date] = None
    platnost_do: Optional[date] = None


@dataclass
class Osev:
    """Crop data"""

    zkod: str
    ctverec: str
    id_pozemek: str
    platnost_od: date
    vymery: List[Vymera]
    nazev_pozemek: Optional[str] = None
    platnost_do: Optional[date] = None
    pestovani: List[Pestovani] = field(default_factory=list)


@dataclass
class Aplikace:
    """Application data"""

    typ: TypAplikace
    dat_aplikace_zahajeni: date
    id_plodina: int
    vymera_plodiny: Decimal
    vymera_aplikace: Decimal
    dat_zapraveni_ukonceni: Optional[date] = None
    doba_zapraveni: Optional[DobaZapraveni] = None
    id_pestovani: Optional[str] = None
    id_pozemek: Optional[str] = None
    mnozstvi_celkem: Optional[Decimal] = None
    mnozstvi_ha: Optional[Decimal] = None
    merna_jednotka: Optional[MernaJednotka] = None
    id_hnojivo: Optional[int] = None
    nazev_hnojivo: Optional[str] = None
    kategorie_n: Optional[int] = None
    druh_hnojiva: Optional[int] = None
    typove_id_hnojivo: Optional[int] = None
    metoda_zivin: Optional[MetodaZivin] = None
    privod_n: Optional[Decimal] = None
    privod_p: Optional[Decimal] = None
    privod_k: Optional[Decimal] = None
    privod_mg: Optional[Decimal] = None
    privod_ca: Optional[Decimal] = None
    privod_s: Optional[Decimal] = None
    rozklad_slamy: Optional[bool] = None

    def __post_init__(self) -> None:
        # Ensure proper decimal precision
        if self.vymera_plodiny is not None:
            self.vymera_plodiny = round(self.vymera_plodiny, 2)
        if self.vymera_aplikace is not None:
            self.vymera_aplikace = round(self.vymera_aplikace, 2)
        if self.mnozstvi_celkem is not None:
            self.mnozstvi_celkem = round(self.mnozstvi_celkem, 3)
        if self.mnozstvi_ha is not None:
            self.mnozstvi_ha = round(self.mnozstvi_ha, 3)
        # Round nutrient values to 2 decimal places
        for attr in [
            "privod_n",
            "privod_p",
            "privod_k",
            "privod_mg",
            "privod_ca",
            "privod_s",
        ]:
            value = getattr(self, attr)
            if value is not None:
                setattr(self, attr, round(value, 2))


@dataclass
class Sklizen:
    """Harvest data"""

    id_pestovani: str
    id_produkt: int
    hosp_rok: int
    vymera_sklizne: Decimal
    merna_jednotka: MernaJednotka
    typ_produktu: Optional[TypProduktu] = None
    mnozstvi_celkem: Optional[Decimal] = None
    mnozstvi_ha: Optional[Decimal] = None
    susina: Optional[int] = None

    def __post_init__(self) -> None:
        # Ensure proper decimal precision
        self.vymera_sklizne = round(self.vymera_sklizne, 3)
        if self.mnozstvi_celkem is not None:
            self.mnozstvi_celkem = round(self.mnozstvi_celkem, 3)
        if self.mnozstvi_ha is not None:
            self.mnozstvi_ha = round(self.mnozstvi_ha, 3)


@dataclass
class Pastva:
    """Grazing data"""

    id_pozemek: str
    id_druh_zvirat: str
    pocet_ks: Decimal
    pocet_dj: Decimal
    pastva_od: date
    pastva_do: date
    id_kategorie_zvirat: Optional[int] = None
    vlastni_kategorie_zvirat: Optional[str] = None
    pocet_hod_pastva: Optional[int] = None
    vymera_pastvy: Optional[Decimal] = None
    mnozstvi_ha: Optional[Decimal] = None
    merna_jednotka: Optional[MernaJednotka] = None
    id_hnojivo: Optional[int] = None
    nazev_hnojivo: Optional[str] = None
    metoda_zivin: Optional[MetodaZivin] = None
    privod_n: Optional[Decimal] = None
    privod_p: Optional[Decimal] = None
    privod_k: Optional[Decimal] = None

    def __post_init__(self) -> None:
        # Ensure proper decimal precision
        self.pocet_ks = round(self.pocet_ks, 3)
        self.pocet_dj = round(self.pocet_dj, 3)
        if self.vymera_pastvy is not None:
            self.vymera_pastvy = round(self.vymera_pastvy, 2)
        if self.mnozstvi_ha is not None:
            self.mnozstvi_ha = round(self.mnozstvi_ha, 3)
        # Round nutrient values to 2 decimal places
        for attr in ["privod_n", "privod_p", "privod_k"]:
            value = getattr(self, attr)
            if value is not None:
                setattr(self, attr, round(value, 2))


@dataclass
class Request:
    """Main request data structure"""

    typ: TypRequest
    osevy: List[Osev]
    obdobi_od: Optional[date] = None
    obdobi_do: Optional[date] = None
    hosp_rok: Optional[int] = None
    rezim_volani: Optional[RezimVolani] = None
    rozsah_dat: List[RozsahDat] = field(default_factory=list)
    aplikace: List[Aplikace] = field(default_factory=list)
    sklizne: List[Sklizen] = field(default_factory=list)
    pastvy: List[Pastva] = field(default_factory=list)


@dataclass
class Response:
    """Response data structure"""

    guid_podani: str


class XMLBuilder:
    """XML Builder for EH_PEH02A service"""

    def __init__(self) -> None:
        self.encoding = "utf-8"

    def _add_element_if_not_none(
        self,
        parent: Element,
        tag: str,
        value: Union[str, int, bool, Decimal, date, Enum, None],
        enum_value: bool = False,
    ) -> None:
        """Add XML element only if value is not None"""
        if value is not None:
            if isinstance(value, bool):
                text = "true" if value else "false"
            elif isinstance(value, date):
                text = value.strftime("%Y-%m-%d")
            elif isinstance(value, Decimal):
                text = str(value)
            elif enum_value and hasattr(value, "value"):
                text = value.value
            else:
                text = str(value)

            elem = SubElement(parent, tag)
            elem.text = text

    def _build_vymery(self, parent: Element, vymery: List[Vymera]) -> None:
        """Build Vymery XML elements"""
        vymery_elem = SubElement(parent, "Vymery")
        for vymera in vymery:
            vymera_elem = SubElement(vymery_elem, "Vymera")
            self._add_element_if_not_none(vymera_elem, "Vymera", vymera.vymera)
            self._add_element_if_not_none(vymera_elem, "PlatnostOd", vymera.platnost_od)
            self._add_element_if_not_none(vymera_elem, "PlatnostDo", vymera.platnost_do)

    def _build_pestovani(
        self, parent: Element, pestovani_list: List[Pestovani]
    ) -> None:
        """Build Pestovani XML elements"""
        if not pestovani_list:
            return

        for pestovani in pestovani_list:
            pestovani_elem = SubElement(parent, "Pestovani")
            self._add_element_if_not_none(
                pestovani_elem, "IdPestovani", pestovani.id_pestovani
            )
            self._add_element_if_not_none(
                pestovani_elem, "IdPlodina", pestovani.id_plodina
            )
            self._add_element_if_not_none(
                pestovani_elem, "IdUzitkovySmer", pestovani.id_uzitkovy_smer
            )
            self._add_element_if_not_none(
                pestovani_elem, "Viceleta", pestovani.viceleta
            )
            self._add_element_if_not_none(pestovani_elem, "HospRok", pestovani.hosp_rok)
            self._add_element_if_not_none(
                pestovani_elem, "TypPlodiny", pestovani.typ_plodiny, enum_value=True
            )
            self._add_element_if_not_none(
                pestovani_elem, "ZahajeniPestovani", pestovani.zahajeni_pestovani
            )
            self._add_element_if_not_none(
                pestovani_elem, "UkonceniPestovani", pestovani.ukonceni_pestovani
            )
            self._add_element_if_not_none(
                pestovani_elem, "PlatnostOd", pestovani.platnost_od
            )
            self._add_element_if_not_none(
                pestovani_elem, "PlatnostDo", pestovani.platnost_do
            )

    def _build_osevy(self, parent: Element, osevy: List[Osev]) -> None:
        """Build Osevy XML elements"""
        osevy_elem = SubElement(parent, "Osevy")
        for osev in osevy:
            osev_elem = SubElement(osevy_elem, "Osev")
            self._add_element_if_not_none(osev_elem, "Zkod", osev.zkod)
            self._add_element_if_not_none(osev_elem, "Ctverec", osev.ctverec)
            self._add_element_if_not_none(osev_elem, "IdPozemek", osev.id_pozemek)
            self._add_element_if_not_none(osev_elem, "NazevPozemek", osev.nazev_pozemek)
            self._add_element_if_not_none(osev_elem, "PlatnostOd", osev.platnost_od)
            self._add_element_if_not_none(osev_elem, "PlatnostDo", osev.platnost_do)

            self._build_vymery(osev_elem, osev.vymery)
            self._build_pestovani(osev_elem, osev.pestovani)

    def _build_aplikace(self, parent: Element, aplikace_list: List[Aplikace]) -> None:
        """Build Aplikace XML elements"""
        if not aplikace_list:
            return

        aplikace_parent = SubElement(parent, "Aplikace")
        for aplikace in aplikace_list:
            aplikace_elem = SubElement(aplikace_parent, "Aplikace")
            self._add_element_if_not_none(
                aplikace_elem, "Typ", aplikace.typ, enum_value=True
            )
            self._add_element_if_not_none(
                aplikace_elem, "DatAplikaceZahajeni", aplikace.dat_aplikace_zahajeni
            )
            self._add_element_if_not_none(
                aplikace_elem, "DatZapraveniUkonceni", aplikace.dat_zapraveni_ukonceni
            )
            self._add_element_if_not_none(
                aplikace_elem, "DobaZapraveni", aplikace.doba_zapraveni, enum_value=True
            )
            self._add_element_if_not_none(
                aplikace_elem, "IdPestovani", aplikace.id_pestovani
            )
            self._add_element_if_not_none(
                aplikace_elem, "IdPozemek", aplikace.id_pozemek
            )
            self._add_element_if_not_none(
                aplikace_elem, "IdPlodina", aplikace.id_plodina
            )
            self._add_element_if_not_none(
                aplikace_elem, "VymeraPlodiny", aplikace.vymera_plodiny
            )
            self._add_element_if_not_none(
                aplikace_elem, "VymeraAplikace", aplikace.vymera_aplikace
            )
            self._add_element_if_not_none(
                aplikace_elem, "MnozstviCelkem", aplikace.mnozstvi_celkem
            )
            self._add_element_if_not_none(
                aplikace_elem, "MnozstviHa", aplikace.mnozstvi_ha
            )
            self._add_element_if_not_none(
                aplikace_elem, "MernaJednotka", aplikace.merna_jednotka, enum_value=True
            )
            self._add_element_if_not_none(
                aplikace_elem, "IdHnojivo", aplikace.id_hnojivo
            )
            self._add_element_if_not_none(
                aplikace_elem, "NazevHnojivo", aplikace.nazev_hnojivo
            )
            self._add_element_if_not_none(
                aplikace_elem, "KategorieN", aplikace.kategorie_n
            )
            self._add_element_if_not_none(
                aplikace_elem, "DruhHnojiva", aplikace.druh_hnojiva
            )
            self._add_element_if_not_none(
                aplikace_elem, "TypoveIdHnojivo", aplikace.typove_id_hnojivo
            )
            self._add_element_if_not_none(
                aplikace_elem, "MetodaZivin", aplikace.metoda_zivin, enum_value=True
            )
            self._add_element_if_not_none(aplikace_elem, "PrivodN", aplikace.privod_n)
            self._add_element_if_not_none(aplikace_elem, "PrivodP", aplikace.privod_p)
            self._add_element_if_not_none(aplikace_elem, "PrivodK", aplikace.privod_k)
            self._add_element_if_not_none(aplikace_elem, "PrivodMg", aplikace.privod_mg)
            self._add_element_if_not_none(aplikace_elem, "PrivodCa", aplikace.privod_ca)
            self._add_element_if_not_none(aplikace_elem, "PrivodS", aplikace.privod_s)
            self._add_element_if_not_none(
                aplikace_elem, "RozkladSlamy", aplikace.rozklad_slamy
            )

    def _build_sklizne(self, parent: Element, sklizne_list: List[Sklizen]) -> None:
        """Build Sklizne XML elements"""
        if not sklizne_list:
            return

        sklizne_parent = SubElement(parent, "Sklizne")
        for sklizen in sklizne_list:
            sklizen_elem = SubElement(sklizne_parent, "Sklizen")
            self._add_element_if_not_none(
                sklizen_elem, "IdPestovani", sklizen.id_pestovani
            )
            self._add_element_if_not_none(sklizen_elem, "IdProdukt", sklizen.id_produkt)
            self._add_element_if_not_none(
                sklizen_elem, "TypProduktu", sklizen.typ_produktu, enum_value=True
            )
            self._add_element_if_not_none(sklizen_elem, "HospRok", sklizen.hosp_rok)
            self._add_element_if_not_none(
                sklizen_elem, "VymeraSklizne", sklizen.vymera_sklizne
            )
            self._add_element_if_not_none(
                sklizen_elem, "MnozstviCelkem", sklizen.mnozstvi_celkem
            )
            self._add_element_if_not_none(
                sklizen_elem, "MnozstviHa", sklizen.mnozstvi_ha
            )
            self._add_element_if_not_none(
                sklizen_elem, "MernaJednotka", sklizen.merna_jednotka, enum_value=True
            )
            self._add_element_if_not_none(sklizen_elem, "Susina", sklizen.susina)

    def _build_pastvy(self, parent: Element, pastvy_list: List[Pastva]) -> None:
        """Build Pastvy XML elements"""
        if not pastvy_list:
            return

        pastvy_parent = SubElement(parent, "Pastvy")
        for pastva in pastvy_list:
            pastva_elem = SubElement(pastvy_parent, "Pastva")
            self._add_element_if_not_none(pastva_elem, "IdPozemek", pastva.id_pozemek)
            self._add_element_if_not_none(
                pastva_elem, "IdDruhZvirat", pastva.id_druh_zvirat
            )
            self._add_element_if_not_none(
                pastva_elem, "IdKategorieZvirat", pastva.id_kategorie_zvirat
            )
            self._add_element_if_not_none(
                pastva_elem, "VlastniKategorieZvirat", pastva.vlastni_kategorie_zvirat
            )
            self._add_element_if_not_none(pastva_elem, "PocetKs", pastva.pocet_ks)
            self._add_element_if_not_none(pastva_elem, "PocetDJ", pastva.pocet_dj)
            self._add_element_if_not_none(pastva_elem, "PastvaOd", pastva.pastva_od)
            self._add_element_if_not_none(pastva_elem, "PastvaDo", pastva.pastva_do)
            self._add_element_if_not_none(
                pastva_elem, "PocetHodPastva", pastva.pocet_hod_pastva
            )
            self._add_element_if_not_none(
                pastva_elem, "VymeraPastvy", pastva.vymera_pastvy
            )
            self._add_element_if_not_none(pastva_elem, "MnozstviHa", pastva.mnozstvi_ha)
            self._add_element_if_not_none(
                pastva_elem, "MernaJednotka", pastva.merna_jednotka, enum_value=True
            )
            self._add_element_if_not_none(pastva_elem, "IdHnojivo", pastva.id_hnojivo)
            self._add_element_if_not_none(
                pastva_elem, "NazevHnojivo", pastva.nazev_hnojivo
            )
            self._add_element_if_not_none(
                pastva_elem, "MetodaZivin", pastva.metoda_zivin, enum_value=True
            )
            self._add_element_if_not_none(pastva_elem, "PrivodN", pastva.privod_n)
            self._add_element_if_not_none(pastva_elem, "PrivodP", pastva.privod_p)
            self._add_element_if_not_none(pastva_elem, "PrivodK", pastva.privod_k)

    def build_request_xml(self, request: Request) -> str:
        """Build request XML string"""
        root = Element("Request")

        # Add main request elements
        self._add_element_if_not_none(root, "Typ", request.typ, enum_value=True)
        self._add_element_if_not_none(root, "ObdobiOd", request.obdobi_od)
        self._add_element_if_not_none(root, "ObdobiDo", request.obdobi_do)
        self._add_element_if_not_none(root, "HospRok", request.hosp_rok)
        self._add_element_if_not_none(
            root, "RezimVolani", request.rezim_volani, enum_value=True
        )

        # Add RozsahDat if present
        if request.rozsah_dat:
            rozsah_elem = SubElement(root, "RozsahDat")
            for rozsah in request.rozsah_dat:
                self._add_element_if_not_none(
                    rozsah_elem, "Kod", rozsah.kod, enum_value=True
                )

        # Build main data sections
        self._build_osevy(root, request.osevy)
        self._build_aplikace(root, request.aplikace)
        self._build_sklizne(root, request.sklizne)
        self._build_pastvy(root, request.pastvy)

        return self._format_xml(root)

    def build_response_xml(self, response: Response) -> str:
        """Build response XML string"""
        root = Element("Response")
        self._add_element_if_not_none(root, "GuidPodani", response.guid_podani)
        return self._format_xml(root)

    def _format_xml(self, root: Element) -> str:
        """Format XML with proper indentation"""
        # Use minidom for pretty printing
        from xml.dom import minidom

        rough_string = tostring(root, encoding=self.encoding)
        reparsed = minidom.parseString(rough_string)
        return reparsed.toprettyxml(indent="  ", encoding=self.encoding).decode(
            self.encoding
        )
