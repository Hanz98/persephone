#!/usr/bin/env python3
"""
Example usage of the EH_PEH02A XML Builder

This script demonstrates how to create and generate XML for agricultural data
according to the Czech Ministry specification.
"""

from datetime import date
from decimal import Decimal
from persephone.xml_builder import (
    XMLBuilder, Request, Response, Osev, Vymera, Pestovani, 
    Aplikace, Sklizen, Pastva, RozsahDat,
    TypRequest, RezimVolani, RozsahKod, TypPlodiny, TypAplikace,
    DobaZapraveni, MernaJednotka, MetodaZivin, TypProduktu
)


def create_sample_request() -> Request:
    """Create a sample request with realistic agricultural data"""
    
    # Create area measurements
    vymera1 = Vymera(
        vymera=Decimal("15.75"),
        platnost_od=date(2025, 1, 1),
        platnost_do=date(2025, 12, 31)
    )
    
    vymera2 = Vymera(
        vymera=Decimal("12.50"),
        platnost_od=date(2025, 1, 1)
    )
    
    # Create crop cultivation data
    pestovani_wheat = Pestovani(
        id_pestovani="WHEAT_2025_001",
        id_plodina=111,  # Wheat ID from ministry catalog
        viceleta=False,
        zahajeni_pestovani=date(2025, 3, 15),
        platnost_od=date(2025, 3, 15),
        id_uzitkovy_smer=1,  # Food grain
        hosp_rok=2025,
        typ_plodiny=TypPlodiny.HLA,  # Main crop
        ukonceni_pestovani=date(2025, 8, 31),
        platnost_do=date(2025, 8, 31)
    )
    
    pestovani_cover = Pestovani(
        id_pestovani="COVER_2025_001", 
        id_plodina=234,  # Cover crop ID
        viceleta=False,
        zahajeni_pestovani=date(2025, 9, 1),
        platnost_od=date(2025, 9, 1),
        typ_plodiny=TypPlodiny.KRY,  # Cover crop
        ukonceni_pestovani=date(2025, 11, 30),
        platnost_do=date(2025, 11, 30)
    )
    
    # Create field/crop data
    osev1 = Osev(
        zkod="FIELD_A_2025",
        ctverec="A1",
        id_pozemek="CZ_LPIS_12345",
        nazev_pozemek="Severní pole - pšenice",
        platnost_od=date(2025, 1, 1),
        platnost_do=date(2025, 12, 31),
        vymery=[vymera1],
        pestovani=[pestovani_wheat, pestovani_cover]
    )
    
    osev2 = Osev(
        zkod="FIELD_B_2025",
        ctverec="B2", 
        id_pozemek="CZ_LPIS_12346",
        nazev_pozemek="Jižní pole - pastva",
        platnost_od=date(2025, 1, 1),
        vymery=[vymera2]
    )
    
    # Create fertilizer application
    aplikace_nitrogen = Aplikace(
        typ=TypAplikace.H,  # Fertilization
        dat_aplikace_zahajeni=date(2025, 4, 15),
        id_plodina=111,  # Wheat
        vymera_plodiny=Decimal("15.75"),
        vymera_aplikace=Decimal("15.75"),
        dat_zapraveni_ukonceni=date(2025, 4, 16),
        doba_zapraveni=DobaZapraveni.H24,
        id_pestovani="WHEAT_2025_001",
        id_pozemek="CZ_LPIS_12345",
        mnozstvi_celkem=Decimal("1200.000"),
        mnozstvi_ha=Decimal("76.190"),
        merna_jednotka=MernaJednotka.KG,
        id_hnojivo=1001,  # Nitrogen fertilizer ID
        metoda_zivin=MetodaZivin.O,  # Oxide form
        privod_n=Decimal("30.00"),
        privod_p=Decimal("0.00"),
        privod_k=Decimal("0.00"),
        rozklad_slamy=False
    )
    
    # Create manure application
    aplikace_manure = Aplikace(
        typ=TypAplikace.H,  # Fertilization
        dat_aplikace_zahajeni=date(2025, 3, 1),
        id_plodina=111,  # Wheat
        vymera_plodiny=Decimal("15.75"),
        vymera_aplikace=Decimal("15.75"),
        doba_zapraveni=DobaZapraveni.I,  # Immediately
        id_pestovani="WHEAT_2025_001",
        id_pozemek="CZ_LPIS_12345",
        mnozstvi_celkem=Decimal("15.750"),
        mnozstvi_ha=Decimal("1.000"),
        merna_jednotka=MernaJednotka.T,
        nazev_hnojivo="Chlévský hnůj skot",
        kategorie_n=1,
        druh_hnojiva=115,  # Farmyard manure
        metoda_zivin=MetodaZivin.O,
        privod_n=Decimal("4.50"),
        privod_p=Decimal("2.10"),
        privod_k=Decimal("5.80"),
        privod_ca=Decimal("3.20"),
        rozklad_slamy=False
    )
    
    # Create harvest data
    sklizen_wheat = Sklizen(
        id_pestovani="WHEAT_2025_001",
        id_produkt=2001,  # Wheat grain product ID
        hosp_rok=2025,
        vymera_sklizne=Decimal("15.750"),
        merna_jednotka=MernaJednotka.T,
        typ_produktu=TypProduktu.H,  # Main product
        mnozstvi_celkem=Decimal("94.500"),
        mnozstvi_ha=Decimal("6.000"),
        susina=86  # 86% dry matter
    )
    
    sklizen_straw = Sklizen(
        id_pestovani="WHEAT_2025_001",
        id_produkt=2002,  # Wheat straw product ID
        hosp_rok=2025,
        vymera_sklizne=Decimal("15.750"),
        merna_jednotka=MernaJednotka.T,
        typ_produktu=TypProduktu.V,  # Secondary product
        mnozstvi_celkem=Decimal("47.250"),
        mnozstvi_ha=Decimal("3.000"),
        susina=85
    )
    
    # Create grazing data
    pastva_cattle = Pastva(
        id_pozemek="CZ_LPIS_12346",
        id_druh_zvirat="CATTLE",
        pocet_ks=Decimal("20.000"),
        pocet_dj=Decimal("20.000"),  # 1 DJ per cattle
        pastva_od=date(2025, 5, 1),
        pastva_do=date(2025, 10, 31),
        id_kategorie_zvirat=101,  # Adult cattle category
        pocet_hod_pastva=12,  # 12 hours per day
        vymera_pastvy=Decimal("12.50"),
        mnozstvi_ha=Decimal("25.000"),  # kg of manure per ha
        merna_jednotka=MernaJednotka.KG,
        nazev_hnojivo="Výkaly skot pastva",
        metoda_zivin=MetodaZivin.P,  # Elemental form
        privod_n=Decimal("0.45"),
        privod_p=Decimal("0.11"),
        privod_k=Decimal("0.40")
    )
    
    # Define data scope
    rozsah_dat = [
        RozsahDat(kod=RozsahKod.O),  # Crops
        RozsahDat(kod=RozsahKod.H),  # Applications
        RozsahDat(kod=RozsahKod.S),  # Harvests
        RozsahDat(kod=RozsahKod.P)   # Grazing
    ]
    
    # Create the main request
    request = Request(
        typ=TypRequest.S,  # Statistics data
        hosp_rok=2025,
        rezim_volani=RezimVolani.T,  # Test mode
        rozsah_dat=rozsah_dat,
        osevy=[osev1, osev2],
        aplikace=[aplikace_nitrogen, aplikace_manure],
        sklizne=[sklizen_wheat, sklizen_straw],
        pastvy=[pastva_cattle]
    )
    
    return request


def create_sample_response() -> Response:
    """Create a sample response"""
    return Response(guid_podani="12345678-abcd-1234-efgh-123456789012")


def main():
    """Main demonstration function"""
    print("=== EH_PEH02A XML Builder Demo ===\n")
    
    # Create XML builder
    builder = XMLBuilder()
    
    # Generate request XML
    print("1. Creating sample request...")
    request = create_sample_request()
    request_xml = builder.build_request_xml(request)
    
    print("2. Request XML generated successfully!")
    print(f"   - Type: {request.typ.value}")
    print(f"   - Agricultural year: {request.hosp_rok}")
    print(f"   - Mode: {request.rezim_volani.value} (Test)")
    print(f"   - Number of fields: {len(request.osevy)}")
    print(f"   - Number of applications: {len(request.aplikace)}")
    print(f"   - Number of harvests: {len(request.sklizne)}")
    print(f"   - Number of grazing records: {len(request.pastvy)}")
    print(f"   - XML length: {len(request_xml)} characters\n")
    
    # Save request XML to file
    with open("sample_request.xml", "w", encoding="utf-8") as f:
        f.write(request_xml)
    print("3. Request XML saved to 'sample_request.xml'")
    
    # Generate response XML
    print("\n4. Creating sample response...")
    response = create_sample_response()
    response_xml = builder.build_response_xml(response)
    
    print("5. Response XML generated successfully!")
    print(f"   - Submission GUID: {response.guid_podani}")
    print(f"   - XML length: {len(response_xml)} characters\n")
    
    # Save response XML to file
    with open("sample_response.xml", "w", encoding="utf-8") as f:
        f.write(response_xml)
    print("6. Response XML saved to 'sample_response.xml'")
    
    # Show preview of request XML
    print("\n=== Request XML Preview (first 500 characters) ===")
    print(request_xml[:500] + "..." if len(request_xml) > 500 else request_xml)
    
    print("\n=== Response XML Preview ===")
    print(response_xml)
    
    print("\n=== Demo Complete ===")
    print("Check the generated XML files for complete examples.")


if __name__ == "__main__":
    main()