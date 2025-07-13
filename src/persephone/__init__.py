"""
Persephone - Cross-platform GUI application
Main application module with XML Builder for EH_PEH02A service
"""

from typing import TYPE_CHECKING, Any, Optional
from datetime import date
from decimal import Decimal

if TYPE_CHECKING:
    try:
        import toga  # type: ignore
        from toga.style import Pack  # type: ignore
        from toga.style.pack import COLUMN, ROW  # type: ignore
    except ImportError:
        # For type checking when toga is not available
        toga = Any  # type: ignore
        Pack = Any  # type: ignore
        COLUMN = Any  # type: ignore
        ROW = Any  # type: ignore

try:
    import toga
    from toga.style import Pack
    from toga.style.pack import COLUMN, ROW

    TOGA_AVAILABLE = True
except ImportError:
    TOGA_AVAILABLE = False

    # Create mock classes for testing without Toga
    class MockApp:
        def __init__(self, *args: object, **kwargs: object) -> None:
            self.formal_name = "Persephone"
            self.main_window: Optional[Any] = None
            self.crop_input: Optional[Any] = None
            self.result_label: Optional[Any] = None

        def startup(self) -> None:
            pass

        def main_loop(self) -> None:
            pass

    class MockWidget:
        def __init__(self, *args: object, **kwargs: object) -> None:
            self.text = ""
            self.value = ""

    toga = type(
        "toga",
        (),
        {
            "App": MockApp,
            "MainWindow": MockWidget,
            "Box": MockWidget,
            "Label": MockWidget,
            "TextInput": MockWidget,
            "Button": MockWidget,
        },
    )()  # type: ignore

    Pack = type("Pack", (), {})  # type: ignore
    COLUMN = "column"
    ROW = "row"


class Persephone(toga.App):  # type: ignore
    """Main application class for Persephone"""

    def startup(self) -> None:
        """Initialize the application UI"""
        if not TOGA_AVAILABLE:
            print("Toga not available - running in mock mode")
            return

        # Create the main box container
        main_box = toga.Box(style=Pack(direction=COLUMN, padding=10))  # type: ignore

        # Create welcome label for XML Builder demo
        welcome_label = toga.Label(  # type: ignore
            "Persephone XML Builder for EH_PEH02A",
            style=Pack(  # type: ignore
                padding=(0, 0, 10, 0),
                text_align="center",
                font_size=20,
                font_weight="bold",
            ),
        )

        # Create description label
        description_label = toga.Label(  # type: ignore
            "Agricultural Data Service XML Builder - Generate XML for Czech Ministry",
            style=Pack(padding=(0, 0, 20, 0), text_align="center"),  # type: ignore
        )

        # Create input field for crop code
        self.crop_input = toga.TextInput(  # type: ignore
            placeholder="Enter crop code (e.g., WHEAT01)",
            style=Pack(padding=(0, 0, 10, 0)),  # type: ignore
        )

        # Create button to generate XML
        generate_button = toga.Button(  # type: ignore
            "Generate XML Example",
            on_press=self.generate_xml_example,
            style=Pack(padding=(0, 0, 10, 0)),  # type: ignore
        )

        # Create result label
        self.result_label = toga.Label(  # type: ignore
            "",
            style=Pack(
                padding=(0, 0, 10, 0), text_align="center", font_size=16
            ),  # type: ignore
        )

        # Add all components to the main box
        main_box.add(welcome_label)  # type: ignore
        main_box.add(description_label)  # type: ignore
        main_box.add(self.crop_input)  # type: ignore
        main_box.add(generate_button)  # type: ignore
        main_box.add(self.result_label)  # type: ignore

        # Create the main window
        self.main_window = toga.MainWindow(title=self.formal_name)  # type: ignore
        self.main_window.content = main_box  # type: ignore
        self.main_window.show()  # type: ignore

    def generate_xml_example(self, widget: object = None) -> None:
        """Generate XML example using the XML builder"""
        if not TOGA_AVAILABLE:
            # Mock behavior for testing
            if not hasattr(self, "result_label") or self.result_label is None:
                self.result_label = MockWidget()
            if not hasattr(self, "crop_input") or self.crop_input is None:
                self.crop_input = MockWidget()

            crop_code = getattr(self.crop_input, "value", "").strip()
            if not crop_code:
                crop_code = "WHEAT01"

            # Import the XML builder
            try:
                from .xml_builder import (
                    XMLBuilder,
                    Request,
                    Osev,
                    Vymera,
                    Pestovani,
                    TypRequest,
                    TypPlodiny,
                )

                # Create example data
                vymera = Vymera(vymera=Decimal("10.50"), platnost_od=date(2025, 1, 1))

                pestovani = Pestovani(
                    id_pestovani=f"PEST_{crop_code}",
                    id_plodina=123,
                    viceleta=False,
                    zahajeni_pestovani=date(2025, 3, 15),
                    platnost_od=date(2025, 3, 15),
                    typ_plodiny=TypPlodiny.HLA,
                )

                osev = Osev(
                    zkod=crop_code,
                    ctverec="A1",
                    id_pozemek="POZEMEK001",
                    nazev_pozemek=f"Field for {crop_code}",
                    platnost_od=date(2025, 1, 1),
                    vymery=[vymera],
                    pestovani=[pestovani],
                )

                request = Request(typ=TypRequest.S, hosp_rok=2025, osevy=[osev])

                # Generate XML
                builder = XMLBuilder()
                xml = builder.build_request_xml(request)

                message = f"XML generated successfully for crop: {crop_code}\n\nFirst 200 characters:\n{xml[:200]}..."

            except ImportError as e:
                message = f"XML Builder not available: {e}"
            except Exception as e:
                message = f"Error generating XML: {e}"

            self.result_label.text = message
            print(f"Mock mode: {message}")
            return

        crop_code = getattr(self.crop_input, "value", "").strip()
        if not crop_code:
            crop_code = "WHEAT01"

        try:
            from .xml_builder import (
                XMLBuilder,
                Request,
                Osev,
                Vymera,
                Pestovani,
                TypRequest,
                TypPlodiny,
            )

            # Create example data
            vymera = Vymera(vymera=Decimal("10.50"), platnost_od=date(2025, 1, 1))

            pestovani = Pestovani(
                id_pestovani=f"PEST_{crop_code}",
                id_plodina=123,
                viceleta=False,
                zahajeni_pestovani=date(2025, 3, 15),
                platnost_od=date(2025, 3, 15),
                typ_plodiny=TypPlodiny.HLA,
            )

            osev = Osev(
                zkod=crop_code,
                ctverec="A1",
                id_pozemek="POZEMEK001",
                nazev_pozemek=f"Field for {crop_code}",
                platnost_od=date(2025, 1, 1),
                vymery=[vymera],
                pestovani=[pestovani],
            )

            request = Request(typ=TypRequest.S, hosp_rok=2025, osevy=[osev])

            # Generate XML
            builder = XMLBuilder()
            xml = builder.build_request_xml(request)

            message = f"XML generated successfully for crop: {crop_code}\n\nFirst 200 characters:\n{xml[:200]}..."

        except Exception as e:
            message = f"Error generating XML: {e}"

        if hasattr(self, "result_label") and self.result_label:
            self.result_label.text = message


def main() -> Persephone:
    """Entry point for the application"""
    return Persephone()


if __name__ == "__main__":
    app = main()
    if TOGA_AVAILABLE:
        app.main_loop()
    else:
        print("Starting Persephone in mock mode...")
        app.startup()
        print("Persephone application created successfully!")
