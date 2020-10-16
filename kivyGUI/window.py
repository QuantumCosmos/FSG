from kivy.uix.screenmanager import Screen
from kivy.app import App
from kivy.core.window import Window
from inspect import signature
from api_fourier import api
import threading

class User(Screen, api):
    stage_command = ''
    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        Window.bind(on_key_down=self._on_keyboard_down)
        # self.command_dict = {
        #     'one': self.one,
        #     'two': self.two,
        #     'three': self.three,
        #     'exit': self.exit,
        #     'fourier': fourier,
        #     'trace': trace,
        #     'circle': circle,
        #     'q': q
        # }

    def _on_keyboard_down(self, instance, keyboard, keycode, text, modifiers):
        if self.ids.test3.focus and keycode == 40:
            self.set_prompt()

    def refresh_textinput(self):
        if self.ids.test1.text[-1] == '\n':
            self.ids.test1.text = self.ids.test1.text[:-1]

    def set_prompt(self):
        self.ids.test3.text = self.ids.test1.text.split(
            '\n')[-1].replace('>', '').replace(User.stage_command, '')

        self.call_command()
        self.ids.test1.text += '\n>>{}>'.format(
            User.stage_command)

    def call_command(self):
        t = self.ids.test3.text

        if not User.stage_command == '':
            command = getattr(self, User.stage_command)
            threading.Thread(target=command, args=(
                User.stage_command, t, )).start()
            User.stage_command = ''

        elif t in dir(User):
            command = getattr(self, t)

            if len(signature(command).parameters)-1:
                User.stage_command = t
            else:
                threading.Thread(target=command, args=(t, )).start()

        else:
            print('Sorry, there is no command key: ' + t)

    def non(self, n):
        while n<10000:
            print(n)
            n += 1
    def one(self, t, n):
        print(n)
        self.non(int(n))
        print("Command one has Been Processed")


    def two(self, t):
        print("Command two has Been Processed")


    def three(self, t):
        print("Command three has Been Processed")

    def exit(self, t):
        App.get_running_app().stop()




class Consol_Window(App):

    def build(self):
        return self.root


if __name__ == '__main__':
    Consol_Window().run()
