from PyQt6.QtWidgets import QMainWindow
from gui import Ui_MainWindow


class Logic(QMainWindow):
    """
    The Logic class handles the functionality of a calculator and an area module.
    It manages user inputs, dynamic interface updates, and calculations.
    """

    def __init__(self) -> None:
        """
        Initialize the Logic class, set up the GUI, and connect all signals to their respective slots.
        """
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.area_visible: bool = False
        self.ui.areaFrame.hide()
        self.setFixedSize(300, 375)
        self.connect_calculator_buttons()
        self.setup_area_module()
        self.ui.modeButton.clicked.connect(self.toggle_mode)

    def connect_calculator_buttons(self) -> None:
        """
        Connect all calculator buttons to their respective functions.
        """
        for button in [self.ui.button0, self.ui.button1, self.ui.button2, self.ui.button3,
                       self.ui.button4, self.ui.button5, self.ui.button6, self.ui.button7,
                       self.ui.button8, self.ui.button9]:
            button.clicked.connect(lambda _, b=button: self.append_to_display(b.text()))
        for button in [self.ui.addButton, self.ui.subtractButton,
                       self.ui.multiplyButton, self.ui.divideButton, self.ui.decimalButton]:
            button.clicked.connect(lambda _, b=button: self.append_to_display(b.text()))

        self.ui.equalButton.clicked.connect(self.calculate_result)
        self.ui.clearButton.clicked.connect(self.clear_display)
        self.ui.deleteButton.clicked.connect(self.delete_last_character)
        self.ui.negButton.clicked.connect(self.toggle_sign)

    def append_to_display(self, value: str) -> None:
        """
        Append a value to the display.

        :param value: The value (number or operator) to append.
        """
        current_text: str = self.ui.results.text()
        if current_text == "Error":
            self.ui.results.clear()
        self.ui.results.setText(self.ui.results.text() + value)

    def clear_display(self) -> None:
        """
        Clear the display text.
        """
        self.ui.results.clear()

    def delete_last_character(self) -> None:
        """
        Delete the last character from the display or clear if "Error" is displayed.
        """
        current_text: str = self.ui.results.text()
        if current_text == "Error":
            self.ui.results.clear()
        else:
            self.ui.results.setText(current_text[:-1])

    def toggle_sign(self) -> None:
        """
        Toggle the sign (positive/negative) of the current value in the display.
        """
        current_text: str = self.ui.results.text()
        if not current_text or current_text == "Error":
            return

        try:
            current_value: float = float(current_text)
            if current_value != 0:
                current_value = -current_value
                if current_value.is_integer():
                    current_value = int(current_value)
                self.ui.results.setText(str(current_value))
        except ValueError:
            return

    def calculate_result(self) -> None:
        """
        Evaluate the expression currently displayed and update the results field.
        """
        expression: str = self.ui.results.text()
        expression = expression.replace("X", "*").replace("÷", "/")

        try:
            result = eval(expression)
            if isinstance(result, float):
                self.ui.results.setText(f"{result:.4f}".rstrip("0").rstrip("."))
            else:
                self.ui.results.setText(str(result))
        except Exception:
            self.ui.results.setText("Error")

    def toggle_mode(self) -> None:
        """
        Toggle the visibility of the area module and adjust the window size.
        """
        self.area_visible = not self.area_visible

        if self.area_visible:
            self.ui.areaFrame.show()
            self.setFixedSize(475, 375)
        else:
            self.ui.areaFrame.hide()
            self.setFixedSize(300, 375)

    def setup_area_module(self) -> None:
        """
        Set up the area module with its input fields and connect signals for dynamic updates and calculations.
        """
        self.ui.comboBox.clear()
        self.ui.comboBox.addItems(["Select a shape:", "Square", "Rectangle", "Triangle", "Circle"])
        self.ui.comboBox.setCurrentIndex(0)
        self.ui.comboBox.currentIndexChanged.connect(self.update_inputs)
        self.ui.enterButton.clicked.connect(self.calculate_area)
        self.hide_all_inputs()

    def hide_all_inputs(self) -> None:
        """
        Hide all input fields and labels in the area module.
        """
        self.ui.lineEdit1.hide()
        self.ui.lineEdit2.hide()
        self.ui.label1.hide()
        self.ui.label2.hide()

    def update_inputs(self) -> None:
        """
        Dynamically update input fields and labels based on the selected shape.
        """
        self.ui.areaLabel.setText("AREA")
        shape: str = self.ui.comboBox.currentText()
        self.hide_all_inputs()
        if shape == "Square":
            self.ui.label1.setText("Side Length:")
            self.ui.label1.show()
            self.ui.lineEdit1.show()
        elif shape == "Rectangle":
            self.ui.label1.setText("Length:")
            self.ui.label2.setText("Width:")
            self.ui.label1.show()
            self.ui.label2.show()
            self.ui.lineEdit1.show()
            self.ui.lineEdit2.show()
        elif shape == "Triangle":
            self.ui.label1.setText("Base:")
            self.ui.label2.setText("Height:")
            self.ui.label1.show()
            self.ui.label2.show()
            self.ui.lineEdit1.show()
            self.ui.lineEdit2.show()
        elif shape == "Circle":
            self.ui.label1.setText("Radius:")
            self.ui.label1.show()
            self.ui.lineEdit1.show()

    def calculate_area(self) -> None:
        """
        Calculate and display the area of the selected shape based on user input.
        """
        shape: str = self.ui.comboBox.currentText()

        try:
            if shape == "Square":
                side = float(self.ui.lineEdit1.text())
                area = side ** 2
            elif shape == "Rectangle":
                length = float(self.ui.lineEdit1.text())
                width = float(self.ui.lineEdit2.text())
                area = length * width
            elif shape == "Triangle":
                base = float(self.ui.lineEdit1.text())
                height = float(self.ui.lineEdit2.text())
                area = 0.5 * base * height
            elif shape == "Circle":
                radius = float(self.ui.lineEdit1.text())
                area = 3.14159 * radius ** 2
            else:
                self.ui.results.setText("Select a valid shape")
                return
            self.ui.results.setText(f"{area:.4f}".rstrip("0").rstrip("."))
        except ValueError:
            self.ui.results.setText("Invalid input!")
