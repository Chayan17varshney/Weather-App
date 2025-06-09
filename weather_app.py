import tkinter as tk
from tkinter import ttk, font
from PIL import Image, ImageTk
import requests
import json
from datetime import datetime
import math
import time
from io import BytesIO
from urllib.request import urlopen

class HyperionWeatherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Hyperion Weather")
        self.root.geometry("1200x800")
        self.root.minsize(1000, 700)
        self.root.configure(bg='#0a0e21')
        
        # API Configuration
        self.api_key = "001a467a84ef1eaa0d5a46972cca0c10"
        self.base_url = "http://api.openweathermap.org/data/2.5/weather?"
        self.forecast_url = "http://api.openweathermap.org/data/2.5/forecast?"
        self.air_pollution_url = "http://api.openweathermap.org/data/2.5/air_pollution?"
        
        # UI Configuration
        self.current_theme = 'dark'
        self.themes = {
            'dark': {
                'bg': '#0a0e21',
                'card': '#1a1f37',
                'text': '#ffffff',
                'accent': '#4d79ff',
                'secondary': '#2d3250'
            },
            'light': {
                'bg': '#f5f7ff',
                'card': '#ffffff',
                'text': '#2d3250',
                'accent': '#4d79ff',
                'secondary': '#e6e9f5'
            }
        }
        
        self.setup_ui()
        self.load_icons()
        self.create_weather_cards()
        self.create_navigation()
        
        # Default location
        self.update_weather("Delhi")
    
    def setup_ui(self):
        # Main container with gradient background
        self.main_container = tk.Canvas(
            self.root,
            bg=self.themes[self.current_theme]['bg'],
            highlightthickness=0
        )
        self.main_container.pack(fill=tk.BOTH, expand=True)
        
        # Header
        self.header_frame = tk.Frame(
            self.main_container,
            bg=self.themes[self.current_theme]['bg']
        )
        self.header_frame.pack(pady=20, padx=40, fill=tk.X)
        
        # Search bar
        self.search_var = tk.StringVar()
        self.search_entry = tk.Entry(
            self.header_frame,
            textvariable=self.search_var,
            font=('Segoe UI', 14),
            bg=self.themes[self.current_theme]['secondary'],
            fg=self.themes[self.current_theme]['text'],
            insertbackground=self.themes[self.current_theme]['text'],
            relief=tk.FLAT,
            width=30
        )
        self.search_entry.pack(side=tk.LEFT, padx=(0, 10))
        
        search_btn = tk.Button(
            self.header_frame,
            text="Search",
            command=lambda: self.update_weather(self.search_var.get()),
            bg=self.themes[self.current_theme]['accent'],
            fg='white',
            relief=tk.FLAT,
            font=('Segoe UI', 12)
        )
        search_btn.pack(side=tk.LEFT)
        
        # Theme toggle
        self.theme_btn = tk.Button(
            self.header_frame,
            text="☀️" if self.current_theme == 'dark' else "🌙",
            command=self.toggle_theme,
            bg=self.themes[self.current_theme]['secondary'],
            fg=self.themes[self.current_theme]['text'],
            relief=tk.FLAT,
            font=('Segoe UI', 12)
        )
        self.theme_btn.pack(side=tk.RIGHT)
    
    def load_icons(self):
        # Weather icons mapping
        self.weather_icons = {
            '01d': '☀️', '01n': '🌙',  # Clear sky
            '02d': '⛅', '02n': '⛅',  # Few clouds
            '03d': '☁️', '03n': '☁️',  # Scattered clouds
            '04d': '☁️', '04n': '☁️',  # Broken clouds
            '09d': '🌧️', '09n': '🌧️',  # Shower rain
            '10d': '🌦️', '10n': '🌦️',  # Rain
            '11d': '⚡', '11n': '⚡',  # Thunderstorm
            '13d': '❄️', '13n': '❄️',  # Snow
            '50d': '🌫️', '50n': '🌫️'   # Mist
        }
        
        # Load custom icons from web
        try:
            icon_url = "https://openweathermap.org/img/wn/{}@2x.png"
            self.custom_icons = {}
            for code in ['01d', '01n', '02d', '02n', '03d', '03n', 
                        '04d', '04n', '09d', '09n', '10d', '10n',
                        '11d', '11n', '13d', '13n', '50d', '50n']:
                with urlopen(icon_url.format(code)) as u:
                    image_data = u.read()
                image = Image.open(BytesIO(image_data))
                self.custom_icons[code] = ImageTk.PhotoImage(image)
        except:
            self.custom_icons = None
    
    def create_weather_cards(self):
        # Current weather card
        self.current_weather_frame = tk.Frame(
            self.main_container,
            bg=self.themes[self.current_theme]['card'],
            padx=20,
            pady=20,
            relief=tk.FLAT,
            bd=0
        )
        self.current_weather_frame.pack(pady=20, padx=40, fill=tk.X)
        
        # Left side - main weather info
        self.weather_left = tk.Frame(
            self.current_weather_frame,
            bg=self.themes[self.current_theme]['card']
        )
        self.weather_left.pack(side=tk.LEFT, fill=tk.Y)
        
        self.location_label = tk.Label(
            self.weather_left,
            font=('Segoe UI', 24, 'bold'),
            bg=self.themes[self.current_theme]['card'],
            fg=self.themes[self.current_theme]['text']
        )
        self.location_label.pack(anchor='w')
        
        self.date_label = tk.Label(
            self.weather_left,
            font=('Segoe UI', 12),
            bg=self.themes[self.current_theme]['card'],
            fg=self.themes[self.current_theme]['text']
        )
        self.date_label.pack(anchor='w', pady=(0, 20))
        
        self.temp_label = tk.Label(
            self.weather_left,
            font=('Segoe UI', 72, 'bold'),
            bg=self.themes[self.current_theme]['card'],
            fg=self.themes[self.current_theme]['text']
        )
        self.temp_label.pack(anchor='w')
        
        self.weather_desc_label = tk.Label(
            self.weather_left,
            font=('Segoe UI', 18),
            bg=self.themes[self.current_theme]['card'],
            fg=self.themes[self.current_theme]['text']
        )
        self.weather_desc_label.pack(anchor='w', pady=(0, 20))
        
        # Right side - additional weather info
        self.weather_right = tk.Frame(
            self.current_weather_frame,
            bg=self.themes[self.current_theme]['card']
        )
        self.weather_right.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.weather_icon_label = tk.Label(
            self.weather_right,
            font=('Segoe UI', 72),
            bg=self.themes[self.current_theme]['card'],
            fg=self.themes[self.current_theme]['text']
        )
        self.weather_icon_label.pack(anchor='e')
        
        # Additional info grid
        self.info_grid = tk.Frame(
            self.weather_right,
            bg=self.themes[self.current_theme]['card']
        )
        self.info_grid.pack(anchor='e', pady=(20, 0))
        
        # Create info labels
        self.feels_like_label = self.create_info_label("Feels like", "N/A")
        self.humidity_label = self.create_info_label("Humidity", "N/A")
        self.wind_label = self.create_info_label("Wind", "N/A")
        self.pressure_label = self.create_info_label("Pressure", "N/A")
        self.visibility_label = self.create_info_label("Visibility", "N/A")
        self.sunrise_label = self.create_info_label("Sunrise", "N/A")
        self.sunset_label = self.create_info_label("Sunset", "N/A")
        
        # Forecast container
        self.forecast_container = tk.Frame(
            self.main_container,
            bg=self.themes[self.current_theme]['bg']
        )
        self.forecast_container.pack(pady=(0, 20), padx=40, fill=tk.BOTH, expand=True)
        
        # Forecast title
        forecast_title = tk.Label(
            self.forecast_container,
            text="5-Day Forecast",
            font=('Segoe UI', 18, 'bold'),
            bg=self.themes[self.current_theme]['bg'],
            fg=self.themes[self.current_theme]['text']
        )
        forecast_title.pack(anchor='w', pady=(0, 10))
        
        # Forecast cards
        self.forecast_cards_frame = tk.Frame(
            self.forecast_container,
            bg=self.themes[self.current_theme]['bg']
        )
        self.forecast_cards_frame.pack(fill=tk.BOTH, expand=True)
        
        self.forecast_cards = []
        for i in range(5):
            card = tk.Frame(
                self.forecast_cards_frame,
                bg=self.themes[self.current_theme]['card'],
                padx=15,
                pady=15,
                relief=tk.FLAT,
                bd=0
            )
            card.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10) if i < 4 else (0, 0))
            
            day_label = tk.Label(
                card,
                font=('Segoe UI', 12, 'bold'),
                bg=self.themes[self.current_theme]['card'],
                fg=self.themes[self.current_theme]['text']
            )
            day_label.pack()
            
            icon_label = tk.Label(
                card,
                font=('Segoe UI', 24),
                bg=self.themes[self.current_theme]['card'],
                fg=self.themes[self.current_theme]['text']
            )
            icon_label.pack(pady=5)
            
            temp_label = tk.Label(
                card,
                font=('Segoe UI', 14),
                bg=self.themes[self.current_theme]['card'],
                fg=self.themes[self.current_theme]['text']
            )
            temp_label.pack()
            
            self.forecast_cards.append({
                'frame': card,
                'day': day_label,
                'icon': icon_label,
                'temp': temp_label
            })
    
    def create_info_label(self, title, value):
        frame = tk.Frame(
            self.info_grid,
            bg=self.themes[self.current_theme]['card']
        )
        frame.grid(row=len(self.info_grid.winfo_children()) // 2, 
                  column=len(self.info_grid.winfo_children()) % 2,
                  sticky='e',
                  padx=(10, 0),
                  pady=5)
        
        title_label = tk.Label(
            frame,
            text=title + ":",
            font=('Segoe UI', 10),
            bg=self.themes[self.current_theme]['card'],
            fg=self.themes[self.current_theme]['text'],
            anchor='e'
        )
        title_label.pack(side=tk.LEFT)
        
        value_label = tk.Label(
            frame,
            text=value,
            font=('Segoe UI', 10, 'bold'),
            bg=self.themes[self.current_theme]['card'],
            fg=self.themes[self.current_theme]['accent'],
            anchor='w'
        )
        value_label.pack(side=tk.LEFT)
        
        return value_label
    
    def create_navigation(self):
        # Bottom navigation
        self.nav_frame = tk.Frame(
            self.main_container,
            bg=self.themes[self.current_theme]['secondary'],
            height=50
        )
        self.nav_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=40, pady=(0, 20))
        
        # Nav buttons
        nav_buttons = [
            ("Current", lambda: self.show_tab('current')),
            ("Hourly", lambda: self.show_tab('hourly')),
            ("Weekly", lambda: self.show_tab('weekly')),
            ("Maps", lambda: self.show_tab('maps')),
            ("Settings", lambda: self.show_tab('settings'))
        ]
        
        for i, (text, command) in enumerate(nav_buttons):
            btn = tk.Button(
                self.nav_frame,
                text=text,
                command=command,
                bg=self.themes[self.current_theme]['secondary'],
                fg=self.themes[self.current_theme]['text'],
                relief=tk.FLAT,
                font=('Segoe UI', 10),
                padx=15
            )
            btn.pack(side=tk.LEFT, padx=(10 if i > 0 else 20))
    
    def toggle_theme(self):
        self.current_theme = 'light' if self.current_theme == 'dark' else 'dark'
        self.theme_btn.config(
            text="☀️" if self.current_theme == 'dark' else "🌙",
            bg=self.themes[self.current_theme]['secondary'],
            fg=self.themes[self.current_theme]['text']
        )
        self.update_theme_colors()
    
    def update_theme_colors(self):
        theme = self.themes[self.current_theme]
        
        # Update main container
        self.main_container.config(bg=theme['bg'])
        
        # Update header
        self.header_frame.config(bg=theme['bg'])
        self.search_entry.config(
            bg=theme['secondary'],
            fg=theme['text'],
            insertbackground=theme['text']
        )
        
        # Update current weather frame
        self.current_weather_frame.config(bg=theme['card'])
        self.weather_left.config(bg=theme['card'])
        self.weather_right.config(bg=theme['card'])
        self.info_grid.config(bg=theme['card'])
        
        # Update labels
        self.location_label.config(bg=theme['card'], fg=theme['text'])
        self.date_label.config(bg=theme['card'], fg=theme['text'])
        self.temp_label.config(bg=theme['card'], fg=theme['text'])
        self.weather_desc_label.config(bg=theme['card'], fg=theme['text'])
        self.weather_icon_label.config(bg=theme['card'], fg=theme['text'])
        
        # Update forecast container
        self.forecast_container.config(bg=theme['bg'])
        for widget in self.forecast_container.winfo_children():
            if isinstance(widget, tk.Label):
                widget.config(bg=theme['bg'], fg=theme['text'])
        
        # Update forecast cards
        for card in self.forecast_cards:
            card['frame'].config(bg=theme['card'])
            card['day'].config(bg=theme['card'], fg=theme['text'])
            card['icon'].config(bg=theme['card'], fg=theme['text'])
            card['temp'].config(bg=theme['card'], fg=theme['text'])
        
        # Update info labels
        for child in self.info_grid.winfo_children():
            if isinstance(child, tk.Frame):
                for label in child.winfo_children():
                    if isinstance(label, tk.Label):
                        if ":" in label.cget("text"):
                            label.config(bg=theme['card'], fg=theme['text'])
                        else:
                            label.config(bg=theme['card'], fg=theme['accent'])
        
        # Update navigation
        self.nav_frame.config(bg=theme['secondary'])
        for btn in self.nav_frame.winfo_children():
            if isinstance(btn, tk.Button):
                btn.config(
                    bg=theme['secondary'],
                    fg=theme['text']
                )
    
    def update_weather(self, location):
        try:
            # Current weather
            current_url = f"{self.base_url}q={location}&appid={self.api_key}&units=metric"
            response = requests.get(current_url)
            data = json.loads(response.text)
            
            if data['cod'] != 200:
                raise Exception(data['message'])
            
            # Update current weather UI
            self.location_label.config(text=f"{data['name']}, {data['sys']['country']}")
            
            current_date = datetime.fromtimestamp(data['dt']).strftime('%A, %B %d, %Y')
            self.date_label.config(text=current_date)
            
            temp = data['main']['temp']
            self.temp_label.config(text=f"{temp:.1f}°C")
            
            weather_desc = data['weather'][0]['description'].title()
            self.weather_desc_label.config(text=weather_desc)
            
            # Weather icon
            icon_code = data['weather'][0]['icon']
            if self.custom_icons and icon_code in self.custom_icons:
                self.weather_icon_label.config(image=self.custom_icons[icon_code])
            else:
                self.weather_icon_label.config(text=self.weather_icons.get(icon_code, '☀️'))
            
            # Additional info
            feels_like = data['main']['feels_like']
            self.feels_like_label.config(text=f"{feels_like:.1f}°C")
            
            humidity = data['main']['humidity']
            self.humidity_label.config(text=f"{humidity}%")
            
            wind_speed = data['wind']['speed']
            self.wind_label.config(text=f"{wind_speed} m/s")
            
            pressure = data['main']['pressure']
            self.pressure_label.config(text=f"{pressure} hPa")
            
            visibility = data.get('visibility', 'N/A')
            if visibility != 'N/A':
                visibility = f"{visibility/1000:.1f} km" if visibility >= 1000 else f"{visibility} m"
            self.visibility_label.config(text=visibility)
            
            sunrise = datetime.fromtimestamp(data['sys']['sunrise']).strftime('%H:%M')
            self.sunrise_label.config(text=sunrise)
            
            sunset = datetime.fromtimestamp(data['sys']['sunset']).strftime('%H:%M')
            self.sunset_label.config(text=sunset)
            
            # Forecast
            forecast_url = f"{self.forecast_url}q={location}&appid={self.api_key}&units=metric"
            forecast_response = requests.get(forecast_url)
            forecast_data = json.loads(forecast_response.text)
            
            # Group by day
            daily_data = {}
            for item in forecast_data['list']:
                date = datetime.fromtimestamp(item['dt']).strftime('%Y-%m-%d')
                if date not in daily_data:
                    daily_data[date] = []
                daily_data[date].append(item)
            
            # Get next 5 days
            sorted_dates = sorted(daily_data.keys())
            for i, card in enumerate(self.forecast_cards):
                if i >= len(sorted_dates):
                    break
                
                date = sorted_dates[i]
                day_name = datetime.strptime(date, '%Y-%m-%d').strftime('%a')
                card['day'].config(text=day_name)
                
                # Get midday forecast for icon
                midday_forecast = None
                for forecast in daily_data[date]:
                    forecast_time = datetime.fromtimestamp(forecast['dt']).hour
                    if 11 <= forecast_time <= 14:
                        midday_forecast = forecast
                        break
                
                if not midday_forecast:
                    midday_forecast = daily_data[date][len(daily_data[date])//2]
                
                icon_code = midday_forecast['weather'][0]['icon']
                if self.custom_icons and icon_code in self.custom_icons:
                    card['icon'].config(image=self.custom_icons[icon_code])
                else:
                    card['icon'].config(text=self.weather_icons.get(icon_code, '☀️'))
                
                # Calculate min/max temp
                temps = [f['main']['temp'] for f in daily_data[date]]
                max_temp = max(temps)
                min_temp = min(temps)
                card['temp'].config(text=f"{max_temp:.0f}° / {min_temp:.0f}°")
            
        except Exception as e:
            print(f"Error fetching weather data: {e}")
    
    def show_tab(self, tab_name):
        print(f"Showing {tab_name} tab")
        # Implement tab switching logic here

if __name__ == "__main__":
    root = tk.Tk()
    app = HyperionWeatherApp(root)
    root.mainloop()