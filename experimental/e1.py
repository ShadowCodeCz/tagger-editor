import sys
from PyQt6.QtWidgets import QApplication, QFrame, QVBoxLayout, QLineEdit, QPushButton, QScrollArea, QWidget, QHBoxLayout
from PyQt6.QtCore import Qt


class TagEditor(QFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.init_ui()

    def init_ui(self):
        self.layout = QVBoxLayout()

        # Scroll Area Settings
        self.scroll_area = QScrollArea()
        self.scroll_area_widget_contents = QWidget()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area_widget_contents.setLayout(self.layout)
        self.scroll_area.setWidget(self.scroll_area_widget_contents)

        # Add Tag Button
        self.add_tag_button = QPushButton("Přidat tag")
        self.add_tag_button.clicked.connect(self.add_tag_line)

        self.layout.addWidget(self.add_tag_button)
        self.setLayout(self.layout)

    def add_tag_line(self, event):
        # Line Edit for the tag
        line_edit = QLineEdit()
        line_edit.setText('')

        # Remove Button for each tag line
        remove_button = QPushButton("Odstranit")
        remove_button.clicked.connect(lambda: self.remove_tag_line(line_edit, remove_button))

        # Horizontal layout for the tag line
        h_layout = QHBoxLayout()
        h_layout.addWidget(line_edit)
        h_layout.addWidget(remove_button)

        # Insert the new tag line at the second to last position (above the add button)
        self.layout.insertLayout(self.layout.count() - 1, h_layout)

    # def remove_tag_line(self, line_edit, remove_button):
    #     # Remove tag line from the layout
    #     for i in reversed(range(self.layout.count())):
    #         widget = self.layout.itemAt(i).widget()
    #         if widget == line_edit or widget == remove_button:
    #             widget.deleteLater()
    #             self.layout.removeItem(self.layout.itemAt(i))

    def remove_tag_line(self, line_edit, remove_button):
        # Find the parent layout of the line_edit and remove_button
        parent_layout = None
        for i in range(self.layout.count()):
            layout = self.layout.itemAt(i)
            if layout is not None:
                layout_widget = layout.itemAt(0)  # Get the first item in the horizontal layout
                if layout_widget is not None and (
                        layout_widget.widget() == line_edit or layout_widget.widget() == remove_button):
                    parent_layout = layout
                    break

        if parent_layout:
            # Remove all widgets in this horizontal layout
            while parent_layout.count():
                item = parent_layout.takeAt(0)
                if item.widget():
                    item.widget().deleteLater()
            # Remove the horizontal layout itself from the main layout
            self.layout.removeItem(parent_layout)

    def load_tags(self, tags):
        # Clear existing tags
        while self.layout.count() > 1:  # Keep the add tag button
            child = self.layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        # Add new tags
        for tag in tags:
            self.add_tag_line(tag)

    def get_tags(self):
        tags = []
        for i in range(self.layout.count() - 1):  # Exclude the add button
            line_edit = self.layout.itemAt(i).itemAt(0).widget()
            if isinstance(line_edit, QLineEdit):
                tags.append(line_edit.text())
        return tags



if __name__ == '__main__':
    app = QApplication(sys.argv)
    editor = TagEditor()
    editor.show()
    sys.exit(app.exec())