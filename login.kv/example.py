from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.checkbox import CheckBox
from kivy.uix.label import Label

class LoginScreen(BoxLayout):

    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        self.orientation = 'vertical'

        # Create the password TextInput (initially of type 'password')
        self.password_input = TextInput(hint_text="Password", password=True, multiline=False)
        self.add_widget(self.password_input)

        # Create a horizontal layout for the "Show Password" checkbox and label
        show_password_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=40)

        # Add the checkbox
        self.show_password_checkbox = CheckBox(size_hint_x=None, width=40)
        self.show_password_checkbox.bind(active=self.on_checkbox_active)
        show_password_layout.add_widget(self.show_password_checkbox)

        # Add the label next to the checkbox
        show_password_layout.add_widget(Label(text="Show Password"))

        # Add the show password layout to the main layout
        self.add_widget(show_password_layout)

    # Method to toggle password visibility
    def on_checkbox_active(self, checkbox, value):
        if value:  # If checkbox is checked
            self.password_input.password = False  # Show the password as plain text
        else:  # If checkbox is unchecked
            self.password_input.password = True  # Hide the password

class MyApp(App):
    def build(self):
        return LoginScreen()

if __name__ == '__main__':
    MyApp().run()
