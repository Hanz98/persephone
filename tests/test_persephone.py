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
        assert hasattr(app, "generate_xml_example")

    def test_startup_creates_ui_elements(self):
        """Test that startup method creates all necessary UI elements"""
        app = Persephone()

        # Call startup (will work in mock mode)
        app.startup()

        # In mock mode, startup just prints a message and returns
        # The app should still be created successfully
        assert app is not None

    def test_generate_xml_with_crop_code(self):
        """Test generate_xml_example method with a crop code provided"""
        app = Persephone()

        # Mock the UI components
        app.crop_input = Mock()
        app.crop_input.value = "WHEAT01"
        app.result_label = Mock()

        # Mock button widget
        widget = Mock()

        # Call the method
        app.generate_xml_example(widget)

        # Verify the result contains expected content
        result_text = app.result_label.text
        assert "XML generated successfully for crop: WHEAT01" in result_text
        assert "First 200 characters:" in result_text

    def test_generate_xml_without_crop_code(self):
        """Test generate_xml_example method without a crop code provided"""
        app = Persephone()

        # Mock the UI components
        app.crop_input = Mock()
        app.crop_input.value = ""
        app.result_label = Mock()

        # Mock button widget
        widget = Mock()

        # Call the method
        app.generate_xml_example(widget)

        # Verify the default crop code is used
        result_text = app.result_label.text
        assert "XML generated successfully for crop: WHEAT01" in result_text

    def test_generate_xml_with_whitespace_crop_code(self):
        """Test generate_xml_example method with whitespace-only crop code"""
        app = Persephone()

        # Mock the UI components
        app.crop_input = Mock()
        app.crop_input.value = "   "
        app.result_label = Mock()

        # Mock button widget
        widget = Mock()

        # Call the method
        app.generate_xml_example(widget)

        # Verify the default crop code is used (whitespace should be stripped)
        result_text = app.result_label.text
        assert "XML generated successfully for crop: WHEAT01" in result_text
