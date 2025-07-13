# EH_PEH02A XML Builder

This module provides a comprehensive XML builder for the EH_PEH02A agricultural data service according to the Czech Ministry specifications.

## Overview

The XML builder generates XML documents for agricultural data submission including:
- Crop cultivation data (Osevy)
- Fertilizer applications (Aplikace)
- Harvest data (Sklizne)
- Grazing data (Pastvy)

## Features

### Request Types
- **K (Control)**: Data for control purposes with specific time periods
- **S (Statistics)**: Data for statistics by agricultural year
- **B (Balance)**: Data for balance calculations

### Data Validation
- Automatic decimal precision rounding (2-3 decimal places as required)
- Date formatting (YYYY-MM-DD)
- Boolean conversion (true/false)
- Enum value validation
- Optional field handling

### Supported Data Types
- Crops with area measurements and cultivation details
- Fertilizer applications with nutrient content
- Harvest records with yields and dry matter content
- Grazing data with animal counts and manure calculations

## Usage

### Basic Example

```python
from datetime import date
from decimal import Decimal
from persephone.xml_builder import (
    XMLBuilder, Request, Osev, Vymera, Pestovani,
    TypRequest, TypPlodiny
)

# Create area measurement
vymera = Vymera(
    vymera=Decimal("10.50"),
    platnost_od=date(2025, 1, 1)
)

# Create crop cultivation
pestovani = Pestovani(
    id_pestovani="WHEAT_001",
    id_plodina=111,  # Wheat crop ID
    viceleta=False,
    zahajeni_pestovani=date(2025, 3, 15),
    platnost_od=date(2025, 3, 15),
    typ_plodiny=TypPlodiny.HLA  # Main crop
)

# Create field/crop record
osev = Osev(
    zkod="FIELD_A",
    ctverec="A1",
    id_pozemek="LPIS_12345",
    platnost_od=date(2025, 1, 1),
    vymery=[vymera],
    pestovani=[pestovani]
)

# Create request
request = Request(
    typ=TypRequest.S,  # Statistics
    hosp_rok=2025,
    osevy=[osev]
)

# Generate XML
builder = XMLBuilder()
xml = builder.build_request_xml(request)
print(xml)
```

### Complex Example with All Data Types

See `xml_builder_example.py` for a comprehensive example including:
- Multiple fields with different crops
- Fertilizer applications (organic and mineral)
- Harvest data (main and secondary products)
- Grazing records with nutrient calculations

## Data Classes

### Main Classes
- **Request**: Main request container
- **Response**: Service response with submission GUID
- **Osev**: Field/crop data
- **Aplikace**: Fertilizer application
- **Sklizen**: Harvest record
- **Pastva**: Grazing data

### Supporting Classes
- **Vymera**: Area measurement with validity periods
- **Pestovani**: Crop cultivation details
- **RozsahDat**: Data scope definition

### Enumerations
- **TypRequest**: Request types (K/S/B)
- **RezimVolani**: Call mode (P/T - Production/Test)
- **TypPlodiny**: Crop types (HLA/VED/POM/POD/KRY)
- **TypAplikace**: Application types (H/K/P/S)
- **MernaJednotka**: Measurement units (t/kg/l)
- **MetodaZivin**: Nutrient methods (P/O - Elemental/Oxide)

## Validation Rules

### Decimal Precision
- Area measurements: 2 decimal places
- Quantities: 3 decimal places
- Nutrient content: 2 decimal places

### Required Fields
Each data type has specific required fields according to the specification:
- **Osev**: zkod, ctverec, id_pozemek, platnost_od, vymery
- **Aplikace**: typ, dat_aplikace_zahajeni, id_plodina, vymera_plodiny, vymera_aplikace
- **Sklizen**: id_pestovani, id_produkt, hosp_rok, vymera_sklizne, merna_jednotka
- **Pastva**: id_pozemek, id_druh_zvirat, pocet_ks, pocet_dj, pastva_od, pastva_do

### Conditional Requirements
- Control data (K): requires obdobi_od and obdobi_do
- Statistics/Balance data (S/B): requires hosp_rok
- Fertilizers: require amount and unit (except plant residues)
- Harvest records: mandatory for culture R, optional otherwise

## Error Handling

The builder includes validation for:
- Missing required fields
- Invalid enum values
- Incorrect decimal precision
- Invalid date formats

## Testing

Comprehensive test suite covers:
- Basic XML generation
- Complex scenarios with all elements
- Decimal precision validation
- Enum value conversion
- Date formatting
- Boolean conversion
- Optional field handling
- XML well-formedness

Run tests with:
```bash
pytest tests/test_xml_builder.py -v
```

## Files

- `src/persephone/xml_builder.py`: Main XML builder implementation
- `tests/test_xml_builder.py`: Comprehensive test suite
- `xml_builder_example.py`: Usage examples and demonstration
- `sample_request.xml`: Generated example request XML
- `sample_response.xml`: Generated example response XML