"""
Test cases for the XML Builder module
"""

import pytest
from datetime import date
from decimal import Decimal
from xml.etree.ElementTree import fromstring

from persephone.xml_builder import (
    XMLBuilder,
    Request,
    Response,
    Osev,
    Vymera,
    Pestovani,
    Aplikace,
    Sklizen,
    Pastva,
    RozsahDat,
    TypRequest,
    RezimVolani,
    RozsahKod,
    TypPlodiny,
    TypAplikace,
    DobaZapraveni,
    MernaJednotka,
    MetodaZivin,
    TypProduktu,
)


class TestXMLBuilder:
    """Test cases for XMLBuilder class"""

    def setup_method(self):
        """Set up test fixtures"""
        self.builder = XMLBuilder()

    def test_basic_request_xml_generation(self):
        """Test basic request XML generation"""
        # Create a simple request
        vymera = Vymera(vymera=Decimal("10.50"), platnost_od=date(2025, 1, 1))

        osev = Osev(
            zkod="TEST01",
            ctverec="A1",
            id_pozemek="POZEMEK001",
            platnost_od=date(2025, 1, 1),
            vymery=[vymera],
        )

        request = Request(
            typ=TypRequest.K,
            obdobi_od=date(2025, 1, 1),
            obdobi_do=date(2025, 12, 31),
            osevy=[osev],
        )

        # Generate XML
        xml = self.builder.build_request_xml(request)

        # Verify XML structure
        assert "<?xml version=" in xml
        assert "<Request>" in xml
        assert "<Typ>K</Typ>" in xml
        assert "<ObdobiOd>2025-01-01</ObdobiOd>" in xml
        assert "<ObdobiDo>2025-12-31</ObdobiDo>" in xml
        assert "<Osevy>" in xml
        assert "<Osev>" in xml
        assert "<Zkod>TEST01</Zkod>" in xml
        assert "<Ctverec>A1</Ctverec>" in xml
        assert "<IdPozemek>POZEMEK001</IdPozemek>" in xml
        assert "<Vymery>" in xml
        assert "<Vymera>10.50</Vymera>" in xml

    def test_response_xml_generation(self):
        """Test response XML generation"""
        response = Response(guid_podani="12345678-1234-1234-1234-123456789012")

        xml = self.builder.build_response_xml(response)

        assert "<?xml version=" in xml
        assert "<Response>" in xml
        assert "<GuidPodani>12345678-1234-1234-1234-123456789012</GuidPodani>" in xml

    def test_complex_request_with_all_elements(self):
        """Test complex request with all possible elements"""
        # Create test data with all elements
        vymera = Vymera(
            vymera=Decimal("15.75"),
            platnost_od=date(2025, 1, 1),
            platnost_do=date(2025, 12, 31),
        )

        pestovani = Pestovani(
            id_pestovani="PEST001",
            id_plodina=123,
            viceleta=False,
            zahajeni_pestovani=date(2025, 3, 15),
            platnost_od=date(2025, 3, 15),
            id_uzitkovy_smer=456,
            hosp_rok=2025,
            typ_plodiny=TypPlodiny.HLA,
            ukonceni_pestovani=date(2025, 10, 15),
            platnost_do=date(2025, 10, 15),
        )

        osev = Osev(
            zkod="TEST01",
            ctverec="A1",
            id_pozemek="POZEMEK001",
            nazev_pozemek="Test Field",
            platnost_od=date(2025, 1, 1),
            platnost_do=date(2025, 12, 31),
            vymery=[vymera],
            pestovani=[pestovani],
        )

        aplikace = Aplikace(
            typ=TypAplikace.H,
            dat_aplikace_zahajeni=date(2025, 4, 1),
            id_plodina=123,
            vymera_plodiny=Decimal("15.75"),
            vymera_aplikace=Decimal("15.75"),
            dat_zapraveni_ukonceni=date(2025, 4, 2),
            doba_zapraveni=DobaZapraveni.H24,
            id_pestovani="PEST001",
            id_pozemek="POZEMEK001",
            mnozstvi_celkem=Decimal("1500.500"),
            mnozstvi_ha=Decimal("95.270"),
            merna_jednotka=MernaJednotka.KG,
            id_hnojivo=789,
            metoda_zivin=MetodaZivin.O,
            privod_n=Decimal("12.50"),
            privod_p=Decimal("8.25"),
            privod_k=Decimal("15.00"),
            rozklad_slamy=True,
        )

        sklizen = Sklizen(
            id_pestovani="PEST001",
            id_produkt=111,
            hosp_rok=2025,
            vymera_sklizne=Decimal("15.750"),
            merna_jednotka=MernaJednotka.T,
            typ_produktu=TypProduktu.H,
            mnozstvi_celkem=Decimal("125.500"),
            mnozstvi_ha=Decimal("7.970"),
            susina=85,
        )

        pastva = Pastva(
            id_pozemek="POZEMEK002",
            id_druh_zvirat="CATTLE",
            pocet_ks=Decimal("25.000"),
            pocet_dj=Decimal("20.500"),
            pastva_od=date(2025, 5, 1),
            pastva_do=date(2025, 9, 30),
            id_kategorie_zvirat=222,
            pocet_hod_pastva=8,
            vymera_pastvy=Decimal("12.50"),
            mnozstvi_ha=Decimal("2.500"),
            merna_jednotka=MernaJednotka.T,
            id_hnojivo=333,
            nazev_hnojivo="Test Manure",
            metoda_zivin=MetodaZivin.P,
            privod_n=Decimal("5.25"),
            privod_p=Decimal("3.10"),
            privod_k=Decimal("7.85"),
        )

        rozsah_dat = [RozsahDat(kod=RozsahKod.O), RozsahDat(kod=RozsahKod.H)]

        request = Request(
            typ=TypRequest.S,
            hosp_rok=2025,
            rezim_volani=RezimVolani.T,
            rozsah_dat=rozsah_dat,
            osevy=[osev],
            aplikace=[aplikace],
            sklizne=[sklizen],
            pastvy=[pastva],
        )

        # Generate XML
        xml = self.builder.build_request_xml(request)

        # Parse XML to verify it's valid
        root = fromstring(xml.encode("utf-8"))
        assert root.tag == "Request"

        # Verify main elements
        assert root.find("Typ").text == "S"
        assert root.find("HospRok").text == "2025"
        assert root.find("RezimVolani").text == "T"

        # Verify RozsahDat
        rozsah_elem = root.find("RozsahDat")
        assert rozsah_elem is not None
        kod_elements = rozsah_elem.findall("Kod")
        assert len(kod_elements) == 2
        assert kod_elements[0].text == "O"
        assert kod_elements[1].text == "H"

        # Verify Osevy structure
        osevy_elem = root.find("Osevy")
        assert osevy_elem is not None
        osev_elem = osevy_elem.find("Osev")
        assert osev_elem.find("Zkod").text == "TEST01"
        assert osev_elem.find("NazevPozemek").text == "Test Field"

        # Verify Vymery
        vymery_elem = osev_elem.find("Vymery")
        vymera_elem = vymery_elem.find("Vymera")
        assert vymera_elem.find("Vymera").text == "15.75"
        assert vymera_elem.find("PlatnostOd").text == "2025-01-01"
        assert vymera_elem.find("PlatnostDo").text == "2025-12-31"

        # Verify Pestovani
        pestovani_elem = osev_elem.find("Pestovani")
        assert pestovani_elem.find("IdPestovani").text == "PEST001"
        assert pestovani_elem.find("IdPlodina").text == "123"
        assert pestovani_elem.find("Viceleta").text == "false"
        assert pestovani_elem.find("TypPlodiny").text == "HLA"

        # Verify Aplikace
        aplikace_parent = root.find("Aplikace")
        aplikace_elem = aplikace_parent.find("Aplikace")
        assert aplikace_elem.find("Typ").text == "H"
        assert aplikace_elem.find("DobaZapraveni").text == "24"
        assert aplikace_elem.find("MnozstviCelkem").text == "1500.500"
        assert aplikace_elem.find("MnozstviHa").text == "95.270"
        assert aplikace_elem.find("MernaJednotka").text == "kg"
        assert aplikace_elem.find("MetodaZivin").text == "O"
        assert aplikace_elem.find("PrivodN").text == "12.50"
        assert aplikace_elem.find("RozkladSlamy").text == "true"

        # Verify Sklizne
        sklizne_parent = root.find("Sklizne")
        sklizen_elem = sklizne_parent.find("Sklizen")
        assert sklizen_elem.find("IdPestovani").text == "PEST001"
        assert sklizen_elem.find("TypProduktu").text == "H"
        assert sklizen_elem.find("VymeraSklizne").text == "15.750"
        assert sklizen_elem.find("MernaJednotka").text == "t"
        assert sklizen_elem.find("Susina").text == "85"

        # Verify Pastvy
        pastvy_parent = root.find("Pastvy")
        pastva_elem = pastvy_parent.find("Pastva")
        assert pastva_elem.find("IdPozemek").text == "POZEMEK002"
        assert pastva_elem.find("IdDruhZvirat").text == "CATTLE"
        assert pastva_elem.find("PocetKs").text == "25.000"
        assert pastva_elem.find("PocetDJ").text == "20.500"
        assert pastva_elem.find("VymeraPastvy").text == "12.50"
        assert pastva_elem.find("MetodaZivin").text == "P"

    def test_decimal_precision(self):
        """Test that decimal values are rounded to correct precision"""
        vymera = Vymera(
            vymera=Decimal("10.123456"),  # Should be rounded to 2 places
            platnost_od=date(2025, 1, 1),
        )

        assert vymera.vymera == Decimal("10.12")

        aplikace = Aplikace(
            typ=TypAplikace.H,
            dat_aplikace_zahajeni=date(2025, 4, 1),
            id_plodina=123,
            vymera_plodiny=Decimal("15.999"),  # Should be rounded to 2 places
            vymera_aplikace=Decimal("15.999"),  # Should be rounded to 2 places
            mnozstvi_celkem=Decimal("1500.12345"),  # Should be rounded to 3 places
            mnozstvi_ha=Decimal("95.12345"),  # Should be rounded to 3 places
            privod_n=Decimal("12.999"),  # Should be rounded to 2 places
        )

        assert aplikace.vymera_plodiny == Decimal("16.00")
        assert aplikace.vymera_aplikace == Decimal("16.00")
        assert aplikace.mnozstvi_celkem == Decimal("1500.123")
        assert aplikace.mnozstvi_ha == Decimal("95.123")
        assert aplikace.privod_n == Decimal("13.00")

    def test_enum_values_in_xml(self):
        """Test that enum values are correctly converted to strings in XML"""
        osev = Osev(
            zkod="TEST01",
            ctverec="A1",
            id_pozemek="POZEMEK001",
            platnost_od=date(2025, 1, 1),
            vymery=[Vymera(vymera=Decimal("10.50"), platnost_od=date(2025, 1, 1))],
        )

        request = Request(
            typ=TypRequest.K,  # Should become "K"
            rezim_volani=RezimVolani.T,  # Should become "T"
            osevy=[osev],
        )

        xml = self.builder.build_request_xml(request)

        # Verify enum values are converted to their string representations
        assert "<Typ>K</Typ>" in xml
        assert "<RezimVolani>T</RezimVolani>" in xml

    def test_optional_elements_not_included_when_none(self):
        """Test that optional elements are not included in XML when None"""
        osev = Osev(
            zkod="TEST01",
            ctverec="A1",
            id_pozemek="POZEMEK001",
            platnost_od=date(2025, 1, 1),
            vymery=[Vymera(vymera=Decimal("10.50"), platnost_od=date(2025, 1, 1))],
            nazev_pozemek=None,  # Optional, should not appear in XML
            platnost_do=None,  # Optional, should not appear in XML
        )

        request = Request(
            typ=TypRequest.K,
            osevy=[osev],
            obdobi_od=None,  # Optional, should not appear in XML
            hosp_rok=None,  # Optional, should not appear in XML
        )

        xml = self.builder.build_request_xml(request)

        # Verify optional elements are not present
        assert "<NazevPozemek>" not in xml
        assert "<PlatnostDo>" not in xml
        assert "<ObdobiOd>" not in xml
        assert "<HospRok>" not in xml

    def test_boolean_values_conversion(self):
        """Test that boolean values are converted to lowercase strings"""
        pestovani = Pestovani(
            id_pestovani="PEST001",
            id_plodina=123,
            viceleta=True,  # Should become "true"
            zahajeni_pestovani=date(2025, 3, 15),
            platnost_od=date(2025, 3, 15),
        )

        osev = Osev(
            zkod="TEST01",
            ctverec="A1",
            id_pozemek="POZEMEK001",
            platnost_od=date(2025, 1, 1),
            vymery=[Vymera(vymera=Decimal("10.50"), platnost_od=date(2025, 1, 1))],
            pestovani=[pestovani],
        )

        aplikace = Aplikace(
            typ=TypAplikace.H,
            dat_aplikace_zahajeni=date(2025, 4, 1),
            id_plodina=123,
            vymera_plodiny=Decimal("15.75"),
            vymera_aplikace=Decimal("15.75"),
            rozklad_slamy=False,  # Should become "false"
        )

        request = Request(typ=TypRequest.K, osevy=[osev], aplikace=[aplikace])

        xml = self.builder.build_request_xml(request)

        # Verify boolean values
        assert "<Viceleta>true</Viceleta>" in xml
        assert "<RozkladSlamy>false</RozkladSlamy>" in xml

    def test_date_formatting(self):
        """Test that dates are formatted correctly as YYYY-MM-DD"""
        osev = Osev(
            zkod="TEST01",
            ctverec="A1",
            id_pozemek="POZEMEK001",
            platnost_od=date(2025, 1, 15),  # Should become "2025-01-15"
            vymery=[
                Vymera(
                    vymera=Decimal("10.50"),
                    platnost_od=date(2025, 2, 28),  # Should become "2025-02-28"
                    platnost_do=date(2025, 12, 31),  # Should become "2025-12-31"
                )
            ],
        )

        request = Request(
            typ=TypRequest.K,
            obdobi_od=date(2025, 3, 1),  # Should become "2025-03-01"
            obdobi_do=date(2025, 11, 30),  # Should become "2025-11-30"
            osevy=[osev],
        )

        xml = self.builder.build_request_xml(request)

        # Verify date formatting
        assert "<ObdobiOd>2025-03-01</ObdobiOd>" in xml
        assert "<ObdobiDo>2025-11-30</ObdobiDo>" in xml
        assert "<PlatnostOd>2025-01-15</PlatnostOd>" in xml
        assert "<PlatnostOd>2025-02-28</PlatnostOd>" in xml
        assert "<PlatnostDo>2025-12-31</PlatnostDo>" in xml

    def test_empty_collections_not_included(self):
        """Test that empty collections don't create parent elements"""
        osev = Osev(
            zkod="TEST01",
            ctverec="A1",
            id_pozemek="POZEMEK001",
            platnost_od=date(2025, 1, 1),
            vymery=[Vymera(vymera=Decimal("10.50"), platnost_od=date(2025, 1, 1))],
            pestovani=[],  # Empty list
        )

        request = Request(
            typ=TypRequest.K,
            osevy=[osev],
            aplikace=[],  # Empty list, should not create <Aplikace> element
            sklizne=[],  # Empty list, should not create <Sklizne> element
            pastvy=[],  # Empty list, should not create <Pastvy> element
        )

        xml = self.builder.build_request_xml(request)

        # Verify empty collections don't create parent elements
        assert "<Aplikace>" not in xml
        assert "<Sklizne>" not in xml
        assert "<Pastvy>" not in xml

    def test_xml_well_formed(self):
        """Test that generated XML is well-formed and parseable"""
        osev = Osev(
            zkod="TEST01",
            ctverec="A1",
            id_pozemek="POZEMEK001",
            platnost_od=date(2025, 1, 1),
            vymery=[Vymera(vymera=Decimal("10.50"), platnost_od=date(2025, 1, 1))],
        )

        request = Request(typ=TypRequest.K, osevy=[osev])

        xml = self.builder.build_request_xml(request)

        # Should be able to parse without errors
        try:
            root = fromstring(xml.encode("utf-8"))
            assert root.tag == "Request"
        except Exception as e:
            pytest.fail(f"Generated XML is not well-formed: {e}")

    def test_response_xml_well_formed(self):
        """Test that response XML is well-formed"""
        response = Response(guid_podani="test-guid-123")
        xml = self.builder.build_response_xml(response)

        try:
            root = fromstring(xml.encode("utf-8"))
            assert root.tag == "Response"
            assert root.find("GuidPodani").text == "test-guid-123"
        except Exception as e:
            pytest.fail(f"Generated response XML is not well-formed: {e}")
