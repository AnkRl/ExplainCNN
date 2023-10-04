from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout

class YourApp(App):    

    def build(self):
        root_widget = BoxLayout(orientation='vertical')

        # Title
        title = Label(
            font_size=50,
            markup=True)
        title.text = 'Welcome to [color=#ff00ff]Calculator[/color]!'

        # Num Pad
        button_symbols = ('1', '2', '3', '+',
                          '4', '5', '6', '-',
                          '7', '8', '9', '.',
                          '0', '*', '/', '=')

        button_grid = GridLayout(cols=4, size_hint_y=2)
        for symbol in button_symbols:
            button_grid.add_widget(Button(text=symbol))
        
        # Callback function
        def print_button_text(instance):
            output_label.text += instance.text        
        # Do the binding
        for button in button_grid.children[1:]:
            button.bind(on_press=print_button_text)    
        # Extra for child 0: "="
        def evaluate_result(instance):
            try:
                output_label.text = str(eval(output_label.text))
            except SyntaxError:
                output_label.text = 'No proper calculation!'
        button_grid.children[0].bind(on_press=evaluate_result)

        # CLear Function
        clear_button = Button(text='Clear',
                              size_hint_y=1,
                              size_hint_x = 0.5,
                              height=100)
        
        def clear_result(instance):
            output_label.text = ""
        clear_button.bind(on_press=clear_result)
        
        # Claculation Display
        output_label = Label(size_hint_y=1, size_hint_x= 1)

        def resize_label_text(label, new_height):
            label.font_size = 0.5*label.height

        output_label.bind(height=resize_label_text)

        root_widget.add_widget(title)        
        root_widget.add_widget(clear_button)
        root_widget.add_widget(button_grid)
        root_widget.add_widget(output_label)


        return root_widget


if __name__ == '__main__':
    YourApp().run()