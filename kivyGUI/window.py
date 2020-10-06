from kivy.uix.screenmanager import Screen
from kivy.uix.textinput import TextInput
from kivy.app import App
from kivy.core.window import Window
from kivy.properties import ObjectProperty

class User(Screen):

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        Window.bind(on_key_down=self._on_keyboard_down)

    def _on_keyboard_down(self, instance, keyboard, keycode, text, modifiers):
        if self.ids.test3.focus and keycode == 40:
            self.set_prompt()

    def refresh_textinput(self):
        if self.ids.test1.text[-1] == '\n':
            self.ids.test1.text = self.ids.test1.text[:-1]

    def set_prompt(self):
        self.ids.test1.text += '\n>>> '
        self.ids.test3.text = self.ids.test1.text.split('\n')[-2].replace('>>>', '')


class Consol_Window(App):

    def build(self):
        return self.root


if __name__ == '__main__':
    Consol_Window().run()
