"""
Persephone - Cross-platform GUI application
Main application module
"""

from typing import TYPE_CHECKING, Any, Optional

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
            self.name_input: Optional[Any] = None
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

        # Create a welcome label
        welcome_label = toga.Label(  # type: ignore
            "Welcome to Persephone!",
            style=Pack(  # type: ignore
                padding=(0, 0, 10, 0),
                text_align="center",
                font_size=20,
                font_weight="bold",
            ),
        )

        # Create description label
        description_label = toga.Label(  # type: ignore
            "A cross-platform GUI application built with Python and Toga.",
            style=Pack(padding=(0, 0, 20, 0), text_align="center"),  # type: ignore
        )

        # Create input field
        self.name_input = toga.TextInput(  # type: ignore
            placeholder="Enter your name", style=Pack(padding=(0, 0, 10, 0))  # type: ignore
        )

        # Create button
        greet_button = toga.Button(  # type: ignore
            "Say Hello", on_press=self.say_hello, style=Pack(padding=(0, 0, 10, 0))  # type: ignore
        )

        # Create result label
        self.result_label = toga.Label(  # type: ignore
            "", style=Pack(padding=(0, 0, 10, 0), text_align="center", font_size=16)  # type: ignore
        )

        # Add all components to the main box
        main_box.add(welcome_label)  # type: ignore
        main_box.add(description_label)  # type: ignore
        main_box.add(self.name_input)  # type: ignore
        main_box.add(greet_button)  # type: ignore
        main_box.add(self.result_label)  # type: ignore

        # Create the main window
        self.main_window = toga.MainWindow(title=self.formal_name)  # type: ignore
        self.main_window.content = main_box  # type: ignore
        self.main_window.show()  # type: ignore

    def say_hello(self, widget: object = None) -> None:
        """Handle the say hello button press"""
        if not TOGA_AVAILABLE:
            # Mock behavior for testing
            if not hasattr(self, "result_label") or self.result_label is None:
                self.result_label = MockWidget()
            if not hasattr(self, "name_input") or self.name_input is None:
                self.name_input = MockWidget()

            name = getattr(self.name_input, "value", "").strip()
            if name:
                greeting = f"Hello, {name}! Nice to meet you!"
            else:
                greeting = "Hello! Please enter your name above."

            self.result_label.text = greeting
            print(f"Mock mode: {greeting}")
            return

        name = getattr(self.name_input, "value", "").strip()
        if name:
            greeting = f"Hello, {name}! Nice to meet you!"
        else:
            greeting = "Hello! Please enter your name above."

        if hasattr(self, "result_label") and self.result_label:
            self.result_label.text = greeting


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
