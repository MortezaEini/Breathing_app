import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.graphics import Color, Ellipse, RoundedRectangle, Rectangle, Line
from kivy.utils import get_color_from_hex
from kivy.properties import NumericProperty, StringProperty, BooleanProperty, ListProperty
from kivy.animation import Animation
from kivy.metrics import dp, sp
from kivy.lang import Builder
import math
import time

# تنظیم رنگ سفید برای پس‌زمینه اصلی
Window.clearcolor = (1, 1, 1, 1)

# کد KV با طراحی متعادل و مرتب
KV_STRING = '''
<WhiteCard@BoxLayout>:
    canvas.before:
        Color:
            rgba: 1, 1, 1, 1
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: [16]
        Color:
            rgba: 0.9, 0.94, 1, 1
        Line:
            rounded_rectangle: [self.x, self.y, self.width, self.height, 16]
            width: 1.5

<BreathingCircle>:
    canvas:
        Color:
            rgba: self.circle_color
        Ellipse:
            pos: self.pos
            size: self.size
        Color:
            rgba: 1, 1, 1, 0.8
        Line:
            width: 2
            circle: [self.center_x, self.center_y, min(self.width, self.height)/2]

<BreathingAppLayout>:
    orientation: 'vertical'
    padding: 20
    spacing: 16
    canvas:
        Color:
            rgba: 0.97, 0.98, 1, 1
        Rectangle:
            pos: self.pos
            size: self.size
    
    # هدر اصلی
    WhiteCard:
        orientation: 'vertical'
        padding: 16
        spacing: 8
        size_hint_y: 0.18
        
        Label:
            id: title_label
            text: '4-7-8 Breathing'
            font_size: 26
            bold: True
            color: 0.15, 0.35, 0.65, 1
            size_hint_y: 0.6
            halign: 'center'
            valign: 'middle'
            
        Label:
            id: subtitle_label
            text: 'Inhale 4s • Hold 7s • Exhale 8s'
            font_size: 18
            color: 0.3, 0.55, 0.85, 1
            size_hint_y: 0.4
            halign: 'center'
            valign: 'middle'
    
    # بخش بصری و تایمر
    WhiteCard:
        orientation: 'vertical'
        padding: 12
        size_hint_y: 0.4
        
        RelativeLayout:
            size_hint: 1, 0.65
            
            BreathingCircle:
                id: breathing_circle
                size_hint: None, None
                size: 180, 180
                pos_hint: {'center_x': 0.5, 'center_y': 0.5}
                circle_color: 0.35, 0.65, 1, 1
            
            Label:
                id: timer_label
                text: ''
                font_size: 52
                bold: True
                color: 0.15, 0.35, 0.65, 1
                pos_hint: {'center_x': 0.5, 'center_y': 0.5}
                halign: 'center'
                outline_width: 1
                outline_color: 1, 1, 1, 1
        
        BoxLayout:
            orientation: 'vertical'
            size_hint: 1, 0.35
            spacing: 4
            padding: [0, 8, 0, 0]
            
            Label:
                id: phase_label
                text: 'Ready'
                font_size: 22
                bold: True
                color: 0.15, 0.35, 0.65, 1
                size_hint_y: 0.6
                halign: 'center'
                valign: 'middle'
            
            Label:
                id: cycle_label
                text: 'Cycle: 0 / 5'
                font_size: 18
                color: 0.4, 0.6, 0.9, 1
                size_hint_y: 0.4
                halign: 'center'
                valign: 'middle'
    
    # دکمه‌های کنترل
    WhiteCard:
        orientation: 'vertical'
        padding: 12
        size_hint_y: 0.18
        
        GridLayout:
            cols: 3
            spacing: 12
            size_hint: 1, 1
            
            Button:
                id: start_button
                text: 'Start'
                background_color: 0.25, 0.6, 1, 1
                background_normal: ''
                color: 1, 1, 1, 1
                bold: True
                font_size: 20
                on_press: app.start_breathing()
                canvas.before:
                    Color:
                        rgba: 0.25, 0.6, 1, 1
                    RoundedRectangle:
                        pos: self.pos
                        size: self.size
                        radius: [12]
            
            Button:
                id: stop_button
                text: 'Stop'
                background_color: 0.95, 0.35, 0.35, 1
                background_normal: ''
                color: 1, 1, 1, 1
                bold: True
                font_size: 20
                disabled: True
                on_press: app.stop_breathing()
                canvas.before:
                    Color:
                        rgba: 0.95, 0.35, 0.35, 1
                    RoundedRectangle:
                        pos: self.pos
                        size: self.size
                        radius: [12]
            
            Button:
                id: reset_button
                text: 'Reset'
                background_color: 0.4, 0.7, 1, 1
                background_normal: ''
                color: 1, 1, 1, 1
                bold: True
                font_size: 20
                on_press: app.reset_breathing()
                canvas.before:
                    Color:
                        rgba: 0.4, 0.7, 1, 1
                    RoundedRectangle:
                        pos: self.pos
                        size: self.size
                        radius: [12]
    
    # تنظیمات سیکل
    WhiteCard:
        orientation: 'horizontal'
        padding: 16
        spacing: 12
        size_hint_y: 0.12
        
        Label:
            text: 'Cycles:'
            font_size: 18
            color: 0.15, 0.35, 0.65, 1
            size_hint_x: 0.4
            halign: 'right'
            valign: 'middle'
            bold: True
            
        Spinner:
            id: cycles_spinner
            text: '5'
            values: ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
            background_color: 1, 1, 1, 1
            color: 0.15, 0.35, 0.65, 1
            size_hint_x: 0.6
            font_size: 18
            option_cls: 'SpinnerOption'
            canvas.before:
                Color:
                    rgba: 0.85, 0.92, 1, 1
                RoundedRectangle:
                    pos: self.pos
                    size: self.size
                    radius: [8]
    
    # راهنما
    WhiteCard:
        orientation: 'vertical'
        padding: 16
        spacing: 8
        size_hint_y: 0.25
        
        Label:
            text: 'Instructions'
            font_size: 20
            bold: True
            color: 0.15, 0.35, 0.65, 1
            size_hint_y: 0.25
            halign: 'center'
            valign: 'middle'
            
        BoxLayout:
            orientation: 'vertical'
            spacing: 6
            size_hint_y: 0.75
            
            Label:
                text: '1. Inhale through nose for 4 seconds'
                font_size: 16
                color: 0.3, 0.5, 0.8, 1
                size_hint_y: 0.25
                halign: 'left'
                valign: 'middle'
            
            Label:
                text: '2. Hold your breath for 7 seconds'
                font_size: 16
                color: 0.3, 0.5, 0.8, 1
                size_hint_y: 0.25
                halign: 'left'
                valign: 'middle'
            
            Label:
                text: '3. Exhale through mouth for 8 seconds'
                font_size: 16
                color: 0.3, 0.5, 0.8, 1
                size_hint_y: 0.25
                halign: 'left'
                valign: 'middle'
            
            Label:
                text: '4. Repeat the cycle'
                font_size: 16
                color: 0.3, 0.5, 0.8, 1
                size_hint_y: 0.25
                halign: 'left'
                valign: 'middle'
'''

# کلاس‌های سفارشی
class WhiteCard(BoxLayout):
    pass

class BreathingCircle(RelativeLayout):
    circle_color = ListProperty([0.35, 0.65, 1, 1])
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

class BreathingAppLayout(BoxLayout):
    pass

# اپلیکیشن اصلی
class Breathing478App(App):
    # Properties
    is_breathing_active = BooleanProperty(False)
    current_phase = StringProperty('Ready')
    time_left = NumericProperty(0)
    current_cycle = NumericProperty(0)
    total_cycles = NumericProperty(5)
    
    # Phase configurations - رنگ‌های واضح و متمایز
    PHASES = {
        'Inhale': {'duration': 4, 'color': [0.35, 0.65, 1, 1], 'timer_color': [0.35, 0.65, 1, 1]},
        'Hold': {'duration': 7, 'color': [0.5, 0.75, 1, 1], 'timer_color': [0.5, 0.75, 1, 1]},
        'Exhale': {'duration': 8, 'color': [0.7, 0.85, 1, 1], 'timer_color': [0.7, 0.85, 1, 1]}
    }
    
    # رنگ‌های ثابت برای ثانیه‌های پایانی هر فاز
    COUNTDOWN_COLORS = {
        3: [1, 0.8, 0.2, 1],    # زرد برای ثانیه ۳
        2: [1, 0.6, 0.1, 1],    # نارنجی برای ثانیه ۲
        1: [1, 0.3, 0.3, 1]     # قرمز برای ثانیه ۱
    }
    
    def build(self):
        Builder.load_string(KV_STRING)
        self.layout = BreathingAppLayout()
        self.phase_order = ['Inhale', 'Hold', 'Exhale']
        self.current_phase_index = 0
        self.animation_event = None
        self.timer_event = None
        self.circle_anim = None
        
        # تنظیم spinner
        Clock.schedule_once(self.setup_spinner, 0.1)
        
        return self.layout
    
    def setup_spinner(self, dt):
        spinner = self.layout.ids.cycles_spinner
        spinner.bind(text=self.on_cycles_changed)
    
    def on_start(self):
        self.update_display()
    
    def on_cycles_changed(self, spinner, text):
        try:
            self.total_cycles = int(text)
            self.update_cycle_display()
        except ValueError:
            pass
    
    def start_breathing(self, instance=None):
        if not self.is_breathing_active:
            self.is_breathing_active = True
            self.current_cycle = 0
            self.current_phase_index = 0
            
            self.layout.ids.start_button.disabled = True
            self.layout.ids.stop_button.disabled = False
            self.layout.ids.cycles_spinner.disabled = True
            self.layout.ids.phase_label.text = 'Starting...'
            self.layout.ids.timer_label.color = [0.15, 0.35, 0.65, 1]
            
            Clock.schedule_once(lambda dt: self.start_new_cycle(), 0.5)
    
    def stop_breathing(self, instance=None):
        self.is_breathing_active = False
        
        if self.animation_event:
            self.animation_event.cancel()
        if self.timer_event:
            self.timer_event.cancel()
        if self.circle_anim:
            self.circle_anim.stop(self.layout.ids.breathing_circle)
        
        self.layout.ids.start_button.disabled = False
        self.layout.ids.stop_button.disabled = True
        self.layout.ids.cycles_spinner.disabled = False
        self.current_phase = 'Stopped'
        self.layout.ids.phase_label.text = 'Stopped'
        self.layout.ids.timer_label.text = ''
        self.layout.ids.timer_label.color = [0.15, 0.35, 0.65, 1]
        
        Animation(size=(180, 180), duration=0.3).start(self.layout.ids.breathing_circle)
    
    def reset_breathing(self, instance=None):
        self.stop_breathing()
        
        self.current_phase = 'Ready'
        self.current_cycle = 0
        self.time_left = 0
        self.current_phase_index = 0
        
        self.layout.ids.phase_label.text = 'Ready'
        self.layout.ids.phase_label.color = [0.15, 0.35, 0.65, 1]
        self.layout.ids.timer_label.text = ''
        self.layout.ids.timer_label.color = [0.15, 0.35, 0.65, 1]
        self.layout.ids.breathing_circle.circle_color = [0.35, 0.65, 1, 1]
        self.layout.ids.breathing_circle.size = (180, 180)
        self.update_cycle_display()
    
    def start_new_cycle(self):
        if not self.is_breathing_active:
            return
        
        self.current_cycle += 1
        if self.current_cycle > self.total_cycles:
            self.complete_session()
            return
        
        self.current_phase_index = 0
        self.update_cycle_display()
        self.execute_current_phase()
    
    def execute_current_phase(self):
        if not self.is_breathing_active:
            return
        
        phase_name = self.phase_order[self.current_phase_index]
        phase_config = self.PHASES[phase_name]
        
        self.current_phase = phase_name
        self.layout.ids.phase_label.text = phase_name
        self.layout.ids.breathing_circle.circle_color = phase_config['color']
        self.layout.ids.timer_label.color = phase_config['timer_color']
        
        self.time_left = phase_config['duration']
        self.update_timer_display()
        
        self.animate_circle_for_phase(phase_name, phase_config['duration'])
        
        self.animation_event = Clock.schedule_once(
            lambda dt: self.next_step(),
            phase_config['duration']
        )
    
    def next_step(self):
        if not self.is_breathing_active:
            return
        
        self.current_phase_index += 1
        
        if self.current_phase_index >= len(self.phase_order):
            if self.current_cycle < self.total_cycles:
                self.layout.ids.phase_label.text = 'Rest'
                self.layout.ids.timer_label.text = '...'
                self.layout.ids.timer_label.color = [0.4, 0.6, 0.9, 1]
                Clock.schedule_once(lambda dt: self.start_new_cycle(), 1.5)
            else:
                self.complete_session()
        else:
            self.execute_current_phase()
    
    def animate_circle_for_phase(self, phase_name, duration):
        base_size = 180
        
        if phase_name == 'Inhale':
            target_size = 240
            anim_type = 'in_out_sine'
        elif phase_name == 'Exhale':
            target_size = 140
            anim_type = 'in_out_sine'
        else:
            target_size = 200
            anim_type = 'linear'
        
        if self.circle_anim:
            self.circle_anim.stop(self.layout.ids.breathing_circle)
        
        self.circle_anim = Animation(
            size=(target_size, target_size),
            duration=duration,
            t=anim_type
        )
        self.circle_anim.start(self.layout.ids.breathing_circle)
    
    def update_timer_display(self):
        if not self.is_breathing_active or self.time_left <= 0:
            return
        
        self.layout.ids.timer_label.text = str(int(self.time_left))
        
        if self.time_left in self.COUNTDOWN_COLORS:
            self.layout.ids.timer_label.color = self.COUNTDOWN_COLORS[self.time_left]
        else:
            phase_name = self.phase_order[self.current_phase_index]
            phase_config = self.PHASES[phase_name]
            self.layout.ids.timer_label.color = phase_config['timer_color']
        
        self.time_left -= 1
        self.timer_event = Clock.schedule_once(
            lambda dt: self.update_timer_display(),
            1
        )
    
    def update_cycle_display(self):
        self.layout.ids.cycle_label.text = f'Cycle: {self.current_cycle} / {self.total_cycles}'
    
    def update_display(self):
        self.update_cycle_display()
    
    def complete_session(self):
        self.is_breathing_active = False
        
        self.layout.ids.phase_label.text = 'Complete!'
        self.layout.ids.timer_label.text = '✓'
        self.layout.ids.timer_label.color = [0.25, 0.6, 1, 1]
        
        self.layout.ids.start_button.disabled = False
        self.layout.ids.stop_button.disabled = True
        self.layout.ids.cycles_spinner.disabled = False
        
        Animation(
            size=(180, 180),
            circle_color=[0.35, 0.65, 1, 1],
            duration=0.5
        ).start(self.layout.ids.breathing_circle)

# اجرای اپلیکیشن
if __name__ == '__main__':
    Breathing478App().run()
