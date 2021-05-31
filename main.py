import tkinter as tk


# saved for later hehe ^-^
# https://stackoverflow.com/questions/4969543/colour-chart-for-tkinter-and-tix

def hex_to_rgb(hex_string) -> (int, int, int):
    string = hex_string[1:]
    r = int(string[0] + string[1], 16)
    g = int(string[2] + string[3], 16)
    b = int(string[4] + string[5], 16)
    return r, g, b


class ColourPickerWindow:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Colour Picker")
        self.window.geometry("600x600")
        self.window.minsize(400, 300)

        # Top Section
        self.top_section = tk.Frame(self.window)
        self.top_section.pack(side=tk.TOP)

        # Colour Display
        self.colour_display = tk.Canvas(self.top_section, width=300, height=100, bg='#666')
        self.colour_display.pack(pady=20, side=tk.TOP)

        # Hex Value
        self.hex_value_section = tk.Frame(self.top_section)
        self.hex_value_section.pack(padx=10, pady=10, side=tk.TOP)

        # Entry
        self.hex_input = tk.Entry(self.hex_value_section, textvariable=tk.StringVar(self.window, value='#000'))
        self.hex_input.pack(side=tk.LEFT)

        # Button
        self.preview_hex = tk.Button(self.hex_value_section, text="Preview", command=lambda: self.preview_hex_colour(self.hex_input.get()))
        self.preview_hex.pack(side=tk.LEFT, padx=10)

        # Change Colour values
        self.colour_inputs = tk.Frame(self.top_section)
        self.colour_inputs.pack(side=tk.TOP)

        # Red input
        self.red_input = tk.Entry(self.colour_inputs, textvariable=tk.StringVar(self.window, value='0'))
        self.red_input.pack(side=tk.LEFT, padx=10)

        # Green input
        self.green_input = tk.Entry(self.colour_inputs, textvariable=tk.StringVar(self.window, value='0'))
        self.green_input.pack(side=tk.LEFT, padx=10)

        # Blue input
        self.blue_input = tk.Entry(self.colour_inputs, textvariable=tk.StringVar(self.window, value='0'))
        self.blue_input.pack(side=tk.LEFT, padx=10)

        # Preview button
        # TODO: Error checking on the preview button
        self.preview = tk.Button(self.colour_inputs, text="Preview",
                                 command=lambda: self.preview_colour(self.red_input.get(), self.green_input.get(),
                                                                     self.blue_input.get()))
        self.preview.pack(padx=10, pady=10, side=tk.RIGHT)

        # Middle Section
        self.middle_section = tk.Frame(self.window)
        self.middle_section.pack(side=tk.TOP)

        # Change Colour Sliders
        self.sliders = tk.Frame(self.middle_section)
        self.sliders.pack(side=tk.TOP)
        # Red Slider
        self.red_slider = tk.Scale(self.sliders, from_=255, to=0, bg="#f99")
        self.red_slider.bind("<ButtonRelease-1>",
                             lambda event: self.preview_colour(self.red_slider.get(), self.green_slider.get(),
                                                               self.blue_slider.get()))
        self.red_slider.pack(side=tk.LEFT, padx=20, pady=10)

        # Green Slider
        self.green_slider = tk.Scale(self.sliders, from_=255, to=0, bg="#9f9")
        self.green_slider.bind("<ButtonRelease-1>",
                               lambda event: self.preview_colour(self.red_slider.get(), self.green_slider.get(),
                                                                 self.blue_slider.get()))
        self.green_slider.pack(side=tk.LEFT, padx=20, pady=10)

        # Blue Slider
        self.blue_slider = tk.Scale(self.sliders, from_=255, to=0, bg="#99f")
        self.blue_slider.bind("<ButtonRelease-1>",
                              lambda event: self.preview_colour(self.red_slider.get(), self.green_slider.get(),
                                                                self.blue_slider.get()))
        self.blue_slider.pack(side=tk.LEFT, padx=20, pady=10)

        # Starts the window running
        self.window.mainloop()

    def preview_colour(self, red: int = 0, green: int = 0, blue: int = 0):
        colour = f"#{int(red):02x}{int(green):02x}{int(blue):02x}"
        self.hex_input.delete(0, "end")
        self.hex_input.insert(0, colour)
        self.colour_display.config(bg=colour)
        self.red_input.delete(0, "end")
        self.red_input.insert(0, red)
        self.green_input.delete(0, "end")
        self.green_input.insert(0, green)
        self.blue_input.delete(0, "end")
        self.blue_input.insert(0, blue)
        self.red_slider.set(red)
        self.green_slider.set(green)
        self.blue_slider.set(blue)

    def preview_hex_colour(self, hex_string):
        colour = hex_to_rgb(hex_string)
        self.preview_colour(colour[0], colour[1], colour[2])


print(int("f", 16))
ColourPickerWindow()