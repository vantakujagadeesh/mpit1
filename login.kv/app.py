from kivymd.app import MDApp 
from kivy.uix.image import Image
from kivymd.uix.textfield import MDTextField
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup 
from kivy.properties import StringProperty
from kivy.core.window import Window
from kivy.uix.scrollview import ScrollView
from kivy.graphics import Color, Rectangle
from kivymd.theming import ThemeManager
import sqlite3
from database import Database

# Initialize database
db = Database()

class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        self.theme_cls = ThemeManager()

        layout = FloatLayout()
        background = Image(source='pic.jpeg', allow_stretch=True, keep_ratio=False)
        layout.add_widget(background)
    
        label=Label(text='Farmers App', font_size=32, size_hint=(1, 0.2),pos_hint={"center_y":.8})
        layout.add_widget(label)
    
        self.username_input = MDTextField(
            hint_text="USERNAME",
            multiline=False,
            icon_right='account',
            font_size="20dp",
            size_hint_x=.85,
            pos_hint={'center_x':.5,'center_y':.65},
            write_tab=False
        )
        layout.add_widget(self.username_input)

        self.password_input = MDTextField(
            hint_text="PASSWORD",
            password=True,
            multiline=False,
            icon_right='eye-off',
            font_size="20dp",
            size_hint_x=.85,
            pos_hint={'center_x':.5,'center_y':.5},
            write_tab=False
        )
        self.password_input.bind(on_touch_down=self.toggle_password_visibility)
        layout.add_widget(self.password_input)

        button = Button(text='Login', size_hint=(.3, 0.05),background_color="lightgreen", pos_hint={'center_x': 0.8, 'center_y': 0.42})
        button.bind(on_press=self.login)
        layout.add_widget(button)

        label_1=Label(text='Do not have an account?', font_size=32, size_hint=(1, 0.2),pos_hint={"center_y":.35})
        layout.add_widget(label_1)

        register_button = Button(text='Register', size_hint=(.3, 0.05),background_color="lightgreen",pos_hint={"center_x": 0.5,"center_y":0.27})
        register_button.bind(on_press=self.register)
        layout.add_widget(register_button)
        self.add_widget(layout)

    def login(self, instance):
        username = self.username_input.text
        password = self.password_input.text

        if db.verify_user(username, password):
            self.manager.current = 'menu'
            self.manager.get_screen('menu').current_user = username
            self.username_input.text = ''
            self.password_input.text = ''
        else:
            popup = Popup(title='Login Failed', 
                         content=Label(text='Invalid username or password'), 
                         size_hint=(0.8, 0.3))
            popup.open()

    def register(self, instance):
        self.manager.current = 'register'
        self.username_input.text = ''
        self.password_input.text = ''

    def toggle_password_visibility(self, instance, touch):
        if instance.collide_point(*touch.pos):
            instance.password = not instance.password
            instance.icon_right = 'eye' if instance.password else 'eye-off'

class RegisterScreen(Screen):
    def __init__(self, **kwargs):
        super(RegisterScreen, self).__init__(**kwargs)
        self.theme_cls = ThemeManager()

        layout = FloatLayout()
        background = Image(source='registration.jpeg', allow_stretch=True, keep_ratio=False)
        layout.add_widget(background)

        

        label_2=Label(text='Register Here', font_size=40, size_hint=(1, 0.2),pos_hint={"center_x": 0.5,"center_y":0.8})
        layout.add_widget(label_2)

        self.username_input = MDTextField(
            hint_text="CHOOSE A USERNAME",                             
            multiline=False,
            icon_right='account',
            font_size="20dp",
            size_hint_x=.85,
            pos_hint={'center_x':.5,'center_y':.65},
            
            write_tab=False)
        layout.add_widget(self.username_input)

        self.password_input = MDTextField(
            hint_text="CREATE A PASSWORD",
            password=True,
            multiline=False,
            icon_right='eye-off',
            font_size="20dp",
            size_hint_x=.85,
            pos_hint={'center_x':.5,'center_y':.5},
            write_tab=False
        )
        self.password_input.bind(on_touch_down=self.toggle_password_visibility)
        layout.add_widget(self.password_input)

        register_button = Button(text='Register', size_hint=(.3, 0.05),background_color="green",pos_hint={'center_x': 0.8, 'center_y': 0.42})
        register_button.bind(on_press=self.register)
        layout.add_widget(register_button)

        back_button = Button(text='Home', size_hint=(.3, 0.05),background_color="green",pos_hint={'center_x': 0.8, 'center_y': 0.9})
        back_button.bind(on_press=self.back_to_login)
        layout.add_widget(back_button)

        self.add_widget(layout)

    def register(self, instance):
        username = self.username_input.text
        password = self.password_input.text

        if not username or not password:
            popup = Popup(title='Registration Failed', 
                         content=Label(text='Please fill the required information'), 
                         size_hint=(0.8, 0.3))
            popup.open()
        elif db.add_user(username, password):
            popup = Popup(title='Registration Successful', 
                         content=Label(text='You can now login'), 
                         size_hint=(0.8, 0.3))
            popup.open()
            self.manager.current = 'login'
            self.username_input.text = ''
            self.password_input.text = ''
        else:
            popup = Popup(title='Registration Failed', 
                         content=Label(text='User already exists'), 
                         size_hint=(0.8, 0.3))
            popup.open()

    def back_to_login(self, instance):
        self.manager.current = 'login'
        self.username_input.text = ''
        self.password_input.text = ''

    def toggle_password_visibility(self, instance, touch):
        if instance.collide_point(*touch.pos):
            instance.password = not instance.password
            instance.icon_right = 'eye' if instance.password else 'eye-off'

class MenuScreen(Screen):
    current_user = StringProperty(None)

    def __init__(self, **kwargs):
        super(MenuScreen, self).__init__(**kwargs)

        # Main layout with white background
        main_layout = BoxLayout(orientation='vertical', padding=20, spacing=20)
        
        # Add white background
        with main_layout.canvas.before:
            Color(1, 1, 1, 1)  # RGB values for white
            self.rect = Rectangle(size=main_layout.size, pos=main_layout.pos)
        
        main_layout.bind(size=self._update_rect, pos=self._update_rect)

        # Welcome label with black text
        self.welcome_label = Label(
            text='Welcome, ',
            font_size=35,
            size_hint=(1, 0.2),
            color=(0, 0, 0, 1)  # Black text color
        )
        main_layout.add_widget(self.welcome_label)

        # Create two horizontal layouts for button pairs with increased height
        top_buttons = BoxLayout(orientation='horizontal', spacing=20, size_hint=(1, 0.3))  # Increased height
        bottom_buttons = BoxLayout(orientation='horizontal', spacing=20, size_hint=(1, 0.3))  # Increased height

        # First row of buttons
        add_crop_button = Button(
            text='Add Crop\nInformation', 
            size_hint=(0.5, 1),
            background_color="lightgreen",
            font_size=30,  # Increased font size
            halign='center'
        )
        add_crop_button.bind(on_press=self.go_to_add_crop)
        top_buttons.add_widget(add_crop_button)

        predict_crop_button = Button(
            text='Predict your\nCrop', 
            size_hint=(0.5, 1),
            background_color="lightgreen",
            font_size=30,  # Increased font size
            halign='center'
        )
        predict_crop_button.bind(on_press=self.go_to_view_crops)
        top_buttons.add_widget(predict_crop_button)

        # Second row of buttons
        check_prices_button = Button(
            text='Check Market\nPrices', 
            size_hint=(0.5, 1),
            background_color="lightgreen",
            font_size=30,  # Increased font size
            halign='center'
        )
        check_prices_button.bind(on_press=self.go_to_check_prices)
        bottom_buttons.add_widget(check_prices_button)

        logout_button = Button(
            text='Logout', 
            size_hint=(0.5, 1),
            background_color="lightgreen",
            font_size=30,  # Increased font size
            halign='center'
        )
        logout_button.bind(on_press=self.logout)
        bottom_buttons.add_widget(logout_button)

        # Add button layouts to main layout
        main_layout.add_widget(top_buttons)
        main_layout.add_widget(bottom_buttons)

        self.add_widget(main_layout)

    def _update_rect(self, instance, value):
        """Update the background rectangle size and position"""
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def on_enter(self):
        self.welcome_label.text = f'Welcome, {self.current_user}!'

    def go_to_add_crop(self, instance):
        self.manager.current = 'add_crop'

    def go_to_view_crops(self, instance):
        self.manager.current = 'view_crops'

    def go_to_check_prices(self, instance):
        self.manager.current = 'check_prices'

    def logout(self, instance):
        self.manager.current = 'login'

class AddCropScreen(Screen):
    def __init__(self, **kwargs):
        super(AddCropScreen, self).__init__(**kwargs)
        
        layout = FloatLayout()
        
        # Add white background
        with layout.canvas.before:
            Color(1, 1, 1, 1)  # RGB values for white
            self.rect = Rectangle(size=layout.size, pos=layout.pos)
        
        layout.bind(size=self._update_rect, pos=self._update_rect)

        label = Label(
            text='Crop Information', 
            font_size=32, 
            size_hint=(1, 0.9), 
            pos_hint={"center_y":.9},
            color=(0, 0, 0, 1)
        )
        layout.add_widget(label)

        grid_layout = GridLayout(cols=2, padding=60, spacing=100, pos_hint={"center_y":.3})
        
        # Existing fields
        grid_layout.add_widget(Label(
            text='Crop Type:', 
            height=50, 
            width=300, 
            size_hint=(None,None),
            color=(0, 0, 0, 1)
        ))
        self.crop_type_input = TextInput(
            multiline=False, 
            height=50, 
            width=300, 
            size_hint=(None,None),
            background_color=(1, 1, 1, 1),
            foreground_color=(0, 0, 0, 1)
        )
        grid_layout.add_widget(self.crop_type_input)

        grid_layout.add_widget(Label(
            text='Quantity (kg):', 
            height=50, 
            width=300, 
            size_hint=(None,None),
            color=(0, 0, 0, 1)
        ))
        self.quantity_input = TextInput(
            multiline=False, 
            input_type='number', 
            height=50, 
            width=300, 
            size_hint=(None,None),
            background_color=(1, 1, 1, 1),
            foreground_color=(0, 0, 0, 1)
        )
        grid_layout.add_widget(self.quantity_input)

        grid_layout.add_widget(Label(
            text='Location:', 
            height=50, 
            width=300, 
            size_hint=(None,None),
            color=(0, 0, 0, 1)
        ))
        self.location_input = TextInput(
            multiline=False, 
            height=50, 
            width=300, 
            size_hint=(None,None),
            background_color=(1, 1, 1, 1),
            foreground_color=(0, 0, 0, 1)
        )
        grid_layout.add_widget(self.location_input)

        # Add Predicted Price label
        grid_layout.add_widget(Label(
            text='Predicted Price / kg:', 
            height=50, 
            width=300, 
            size_hint=(None,None),
            color=(0, 0, 0, 1)
        ))
        self.predicted_price_label = Label(
            text='',  # This will show the predicted price
            height=50,
            width=300,
            size_hint=(None,None),
            color=(0, 0, 0, 1),
            halign='left'
        )
        grid_layout.add_widget(self.predicted_price_label)

        submit_button = Button(
            text='Submit',
            size_hint=(None,None),
            width=150,
            height=75,
            background_color="lightgreen"
        )
        submit_button.bind(on_press=self.submit_crop)
        grid_layout.add_widget(submit_button)

        back_button = Button(
            text='Home',
            size_hint=(None,None),
            width=150,
            height=75,
            background_color="lightgreen"
        )
        back_button.bind(on_press=self.back_to_menu)
        grid_layout.add_widget(back_button)

        layout.add_widget(grid_layout)
        self.add_widget(layout)

    def submit_crop(self, instance):
        crop_type = self.crop_type_input.text
        quantity = self.quantity_input.text
        location = self.location_input.text

        if not crop_type or not quantity or not location:
            popup = Popup(title='Error', 
                         content=Label(text='Please fill all fields'), 
                         size_hint=(0.8, 0.3))
            popup.open()
        else:
            try:
                quantity = float(quantity)
                user_id = db.get_user_id(self.manager.get_screen('menu').current_user)
                if user_id:
                    db.add_crop(user_id, crop_type, quantity, location)
                    popup = Popup(title='Success', 
                                 content=Label(text='Crop information added'), 
                                 size_hint=(0.8, 0.3))
                    popup.open()
                    self.crop_type_input.text = ''
                    self.quantity_input.text = ''
                    self.location_input.text = ''
            except ValueError:
                popup = Popup(title='Error', 
                             content=Label(text='Please enter valid numbers'), 
                             size_hint=(0.8, 0.3))
                popup.open()

    def _update_rect(self, instance, value):
        """Update the background rectangle size and position"""
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def back_to_menu(self, instance):
        self.manager.current = 'menu'

class ViewCropsScreen(Screen):
    def __init__(self, **kwargs):
        super(ViewCropsScreen, self).__init__(**kwargs)
        
        # Main layout with white background
        self.layout = BoxLayout(orientation='vertical', padding=20, spacing=20)
        
        # Add white background
        with self.layout.canvas.before:
            Color(1, 1, 1, 1)  # RGB values for white
            self.rect = Rectangle(size=self.layout.size, pos=self.layout.pos)
        
        self.layout.bind(size=self._update_rect, pos=self._update_rect)

        # Title label
        title_label = Label(
            text='Crop Prediction',
            font_size=35,
            size_hint=(1, 0.2),
            color=(0, 0, 0, 1)  # Black text
        )
        self.layout.add_widget(title_label)

        # Create grid layout for labels and inputs
        grid_layout = GridLayout(
            cols=2, 
            spacing=20,
            size_hint=(1, 0.6),
            padding=20
        )

        # Session
        grid_layout.add_widget(Label(
            text='Session:',
            font_size=25,
            color=(0, 0, 0, 1),
            size_hint_x=None,
            width=200
        ))
        self.session_input = TextInput(
            multiline=False,
            font_size=20,
            size_hint=(1, None),
            height=60,
            background_color=(1, 1, 1, 1),
            foreground_color=(0, 0, 0, 1)
        )
        grid_layout.add_widget(self.session_input)

        # Rainfall
        grid_layout.add_widget(Label(
            text='Rainfall (mm):',
            font_size=25,
            color=(0, 0, 0, 1),
            size_hint_x=None,
            width=200
        ))
        self.rainfall_input = TextInput(
            multiline=False,
            font_size=20,
            size_hint=(1, None),
            height=60,
            background_color=(1, 1, 1, 1),
            foreground_color=(0, 0, 0, 1)
        )
        grid_layout.add_widget(self.rainfall_input)

        # Humidity
        grid_layout.add_widget(Label(
            text='Humidity (%):',
            font_size=25,
            color=(0, 0, 0, 1),
            size_hint_x=None,
            width=200
        ))
        self.humidity_input = TextInput(
            multiline=False,
            font_size=20,
            size_hint=(1, None),
            height=60,
            background_color=(1, 1, 1, 1),
            foreground_color=(0, 0, 0, 1)
        )
        grid_layout.add_widget(self.humidity_input)

        # Soil pH
        grid_layout.add_widget(Label(
            text='Soil pH:',
            font_size=25,
            color=(0, 0, 0, 1),
            size_hint_x=None,
            width=200
        ))
        self.soil_ph_input = TextInput(
            multiline=False,
            font_size=20,
            size_hint=(1, None),
            height=60,
            background_color=(1, 1, 1, 1),
            foreground_color=(0, 0, 0, 1)
        )
        grid_layout.add_widget(self.soil_ph_input)

        # Add Predicted Crop after soil pH
        grid_layout.add_widget(Label(
            text='Predicted Crop:',
            font_size=25,
            color=(0, 0, 0, 1),
            size_hint_x=None,
            width=200
        ))
        self.predicted_crop_label = Label(
            text='',  # This will show the predicted crop
            font_size=25,
            color=(0, 0, 0, 1),
            size_hint=(1, None),
            height=60,
            halign='left'
        )
        grid_layout.add_widget(self.predicted_crop_label)

        self.layout.add_widget(grid_layout)

        # Submit button
        submit_button = Button(
            text='Submit',
            size_hint=(None, None),
            size=(200, 50),
            background_color="lightgreen",
            pos_hint={'center_x': 0.5},
            font_size=20
        )
        submit_button.bind(on_press=self.submit_data)
        self.layout.add_widget(submit_button)

        # Back button
        back_button = Button(
            text='Back to Menu',
            size_hint=(None, None),
            size=(200, 50),
            background_color="lightgreen",
            pos_hint={'center_x': 0.5},
            font_size=20
        )
        back_button.bind(on_press=self.back_to_menu)
        self.layout.add_widget(back_button)

        self.add_widget(self.layout)

    def _update_rect(self, instance, value):
        """Update the background rectangle size and position"""
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def submit_data(self, instance):
        session = self.session_input.text
        rainfall = self.rainfall_input.text
        humidity = self.humidity_input.text
        soil_ph = self.soil_ph_input.text

        if not all([session, rainfall, humidity, soil_ph]):
            popup = Popup(
                title='Error',
                content=Label(text='Please fill all fields'),
                size_hint=(0.8, 0.3)
            )
            popup.open()
        else:
            try:
                # Convert numeric values
                rainfall = float(rainfall)
                humidity = float(humidity)
                soil_ph = float(soil_ph)
                
                # Here you can add your crop prediction logic
                # For now, let's just show a sample prediction
                predicted_crop = self.predict_crop(rainfall, humidity, soil_ph)
                self.predicted_crop_label.text = predicted_crop
                
                # Add success popup
                popup = Popup(
                    title='Success',
                    content=Label(text=f'Predicted crop: {predicted_crop}'),
                    size_hint=(0.8, 0.3)
                )
                popup.open()
                
            except ValueError:
                popup = Popup(
                    title='Error',
                    content=Label(text='Please enter valid numbers'),
                    size_hint=(0.8, 0.3)
                )
                popup.open()

    def predict_crop(self, rainfall, humidity, soil_ph):
        # Add your crop prediction logic here
        # This is just a simple example
        if rainfall > 1000 and humidity > 70 and 6.0 <= soil_ph <= 7.0:
            return "Rice"
        elif rainfall > 500 and humidity > 50 and 6.5 <= soil_ph <= 7.5:
            return "Wheat"
        elif rainfall > 700 and humidity > 60 and 6.0 <= soil_ph <= 7.0:
            return "Maize"
        else:
            return "Unable to predict"

    def back_to_menu(self, instance):
        self.manager.current = 'menu'

class CheckPricesScreen(Screen):
    def __init__(self, **kwargs):
        super(CheckPricesScreen, self).__init__(**kwargs)
        
        # Main layout with white background
        layout = BoxLayout(orientation='vertical', padding=20, spacing=30)
        
        # Add white background
        with layout.canvas.before:
            Color(1, 1, 1, 1)  # RGB values for white
            self.rect = Rectangle(size=layout.size, pos=layout.pos)
        
        layout.bind(size=self._update_rect, pos=self._update_rect)

        # Title
        title_label = Label(
            text='Weather Information',
            font_size=35,
            size_hint=(1, 0.2),
            color=(0, 0, 0, 1)  # Black text
        )
        layout.add_widget(title_label)

        # Create grid layout for labels and inputs
        grid_layout = GridLayout(
            cols=2, 
            spacing=20,
            size_hint=(1, 0.6),
            padding=20
        )

        # Rainfall
        grid_layout.add_widget(Label(
            text='Rainfall (mm):',
            font_size=25,
            color=(0, 0, 0, 1),
            size_hint_x=None,
            width=200
        ))
        self.rainfall_input = TextInput(
            multiline=False,
            font_size=20,
            size_hint=(1, None),
            height=100,
            background_color=(1, 1, 1, 1),
            foreground_color=(0, 0, 0, 1)
        )
        grid_layout.add_widget(self.rainfall_input)

        # Humidity
        grid_layout.add_widget(Label(
            text='Humidity (%):',
            font_size=25,
            color=(0, 0, 0, 1),
            size_hint_x=None,
            width=200
        ))
        self.humidity_input = TextInput(
            multiline=False,
            font_size=20,
            size_hint=(1, None),
            height=100,
            background_color=(1, 1, 1, 1),
            foreground_color=(0, 0, 0, 1)
        )
        grid_layout.add_widget(self.humidity_input)

        # Temperature
        grid_layout.add_widget(Label(
            text='Temperature (°C):',
            font_size=25,
            color=(0, 0, 0, 1),
            size_hint_x=None,
            width=200
        ))
        self.temperature_input = TextInput(
            multiline=False,
            font_size=20,
            size_hint=(1, None),
            height=100,
            background_color=(1, 1, 1, 1),
            foreground_color=(0, 0, 0, 1)
        )
        grid_layout.add_widget(self.temperature_input)

        # Predicted Session
        grid_layout.add_widget(Label(
            text='Predicted Session:',
            font_size=25,
            color=(0, 0, 0, 1),
            size_hint_x=None,
            width=200
        ))
        self.predicted_session_label = Label(
            text='',  # This will show the predicted session
            font_size=25,
            color=(0, 0, 0, 1),
            size_hint=(1, None),
            height=100,
            halign='left'
        )
        grid_layout.add_widget(self.predicted_session_label)

        layout.add_widget(grid_layout)

        # Submit button
        submit_button = Button(
            text='Submit',
            size_hint=(None, None),
            size=(200, 50),
            background_color="lightgreen",
            pos_hint={'center_x': 0.5},
            font_size=20
        )
        submit_button.bind(on_press=self.submit_data)
        layout.add_widget(submit_button)

        # Back button
        back_button = Button(
            text='Back to Menu',
            size_hint=(None, None),
            size=(200, 50),
            background_color="lightgreen",
            pos_hint={'center_x': 0.5},
            font_size=20
        )
        back_button.bind(on_press=self.back_to_menu)
        layout.add_widget(back_button)

        self.add_widget(layout)

    def _update_rect(self, instance, value):
        """Update the background rectangle size and position"""
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def submit_data(self, instance):
        rainfall = self.rainfall_input.text
        humidity = self.humidity_input.text
        temperature = self.temperature_input.text

        if not all([rainfall, humidity, temperature]):
            popup = Popup(
                title='Error',
                content=Label(text='Please fill all fields'),
                size_hint=(0.8, 0.3)
            )
            popup.open()
        else:
            try:
                # Convert numeric values
                rainfall = float(rainfall)
                humidity = float(humidity)
                temperature = float(temperature)
                
                # Predict session based on weather data
                predicted_session = self.predict_session(rainfall, humidity, temperature)
                self.predicted_session_label.text = predicted_session
                
                # Add success popup
                popup = Popup(
                    title='Success',
                    content=Label(text=f'Predicted session: {predicted_session}'),
                    size_hint=(0.8, 0.3)
                )
                popup.open()
                
            except ValueError:
                popup = Popup(
                    title='Error',
                    content=Label(text='Please enter valid numbers'),
                    size_hint=(0.8, 0.3)
                )
                popup.open()

    def predict_session(self, rainfall, humidity, temperature):
        # Add your session prediction logic here
        # This is just a simple example
        if rainfall > 1000 and humidity > 70 and temperature > 25:
            return "Kharif"
        elif rainfall < 500 and humidity < 60 and temperature < 20:
            return "Rabi"
        else:
            return "Unable to predict"

    def back_to_menu(self, instance):
        self.manager.current = 'menu'

class FarmersApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Green"

    def build(self):
        db.create_tables()
        
        sm = ScreenManager(transition=FadeTransition())
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(RegisterScreen(name='register'))
        sm.add_widget(MenuScreen(name='menu'))
        sm.add_widget(AddCropScreen(name='add_crop'))
        sm.add_widget(ViewCropsScreen(name='view_crops'))
        sm.add_widget(CheckPricesScreen(name='check_prices'))
        
        return sm

if __name__ == '__main__':
    Window.size = (400, 600) 
    FarmersApp().run()
