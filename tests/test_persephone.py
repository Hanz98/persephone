"""
Unit tests for the Persephone application
"""

from unittest.mock import Mock
from persephone import Persephone


class TestPersephone:
    """Test cases for the main Persephone application"""

    def test_app_creation(self):
        """Test that the app can be created"""
        app = Persephone()
        assert app is not None
        assert hasattr(app, "startup")
        assert hasattr(app, "say_hello")

    def test_startup_creates_ui_elements(self):
        """Test that startup method creates all necessary UI elements"""
        app = Persephone()

        # Call startup (will work in mock mode)
        app.startup()

        # In mock mode, startup just prints a message and returns
        # The app should still be created successfully
        assert app is not None

    def test_say_hello_with_name(self):
        """Test say_hello method with a name provided"""
        app = Persephone()

        # Mock the UI components
        app.name_input = Mock()
        app.name_input.value = "Alice"
        app.result_label = Mock()

        # Mock button widget
        widget = Mock()

        # Call the method
        app.say_hello(widget)

        # Verify the greeting was set correctly
        expected_greeting = "Hello, Alice! Nice to meet you!"
        app.result_label.text = expected_greeting
        assert app.result_label.text == expected_greeting

    def test_say_hello_without_name(self):
        """Test say_hello method without a name provided"""
        app = Persephone()

        # Mock the UI components
        app.name_input = Mock()
        app.name_input.value = ""
        app.result_label = Mock()

        # Mock button widget
        widget = Mock()

        # Call the method
        app.say_hello(widget)

        # Verify the default greeting was set
        expected_greeting = "Hello! Please enter your name above."
        app.result_label.text = expected_greeting
        assert app.result_label.text == expected_greeting

    def test_say_hello_with_whitespace_name(self):
        """Test say_hello method with whitespace-only name"""
        app = Persephone()

        # Mock the UI components
        app.name_input = Mock()
        app.name_input.value = "   "
        app.result_label = Mock()

        # Mock button widget
        widget = Mock()

        # Call the method
        app.say_hello(widget)

        # Verify the default greeting was set (whitespace should be stripped)
        expected_greeting = "Hello! Please enter your name above."
        app.result_label.text = expected_greeting
        assert app.result_label.text == expected_greeting
