from kivy.uix.screenmanager import Screen
from kivy.app import App
from kivy.core.window import Window

class User(Screen):

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        Window.bind(on_key_down=self._on_keyboard_down)
        self.command_dict =  {
            'one': self.command_one,
            'two': self.command_two,
            'three': self.command_three,
            'exit': self.command_exit,
        }

    def _on_keyboard_down(self, instance, keyboard, keycode, text, modifiers):
        if self.ids.test3.focus and keycode == 40:
            self.set_prompt()

    def refresh_textinput(self):
        if self.ids.test1.text[-1] == '\n':
            self.ids.test1.text = self.ids.test1.text[:-1]

    def set_prompt(self):
        self.ids.test1.text += '\n>>> '
        self.ids.test3.text = self.ids.test1.text.split('\n')[-2].replace('>>>', '')
        self.call_command()

    
    def call_command(self):
        t = self.ids.test3.text.replace(' ', '')
        try:
            self.command_dict[t](t)
        except KeyError:
            print('Sorry, there is no command key: ' + t)

    
    def command_one(self, t):
        print("Command one has Been Processed")


    def command_two(self, t):
        print("Command two has Been Processed")


    def command_three(self, t):
        print("Command three has Been Processed")
    
    def command_exit(self, t):
        App.get_running_app().stop()




class Consol_Window(App):

    def build(self):
        return self.root


if __name__ == '__main__':
    Consol_Window().run()
