import tkinter as tk
import json
import os


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
        self.background_colour = "grey55"
        self.window = tk.Tk()
        self.window.config(bg=self.background_colour)
        self.window.title("Colour Picker")
        self.window.geometry("600x600")
        self.window.minsize(400, 300)

        # Top Section
        self.top_section = tk.Frame(self.window, bg=self.background_colour)
        self.top_section.pack(side=tk.TOP)

        # Colour Display
        self.colour_display = tk.Canvas(self.top_section, width=300, height=100, bg='#666', bd=1,
                                        highlightbackground="black")
        self.colour_display.pack(pady=20, side=tk.TOP)

        # Hex Value
        self.hex_value_section = tk.Frame(self.top_section, bg=self.background_colour)
        self.hex_value_section.pack(padx=10, pady=10, side=tk.TOP)

        # Entry
        self.hex_input = tk.Entry(self.hex_value_section, textvariable=tk.StringVar(self.window, value='#000'))
        self.hex_input.pack(side=tk.LEFT)

        # Button
        self.preview_hex = tk.Button(self.hex_value_section, text="Preview",
                                     command=lambda: self.preview_hex_colour(self.hex_input.get()))
        self.preview_hex.pack(side=tk.LEFT, padx=10)

        # Change Colour values
        self.colour_inputs = tk.Frame(self.top_section, bg=self.background_colour)
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
        self.middle_section = tk.Frame(self.window, bg=self.background_colour)
        self.middle_section.pack(side=tk.TOP)

        # Change Colour Sliders
        self.sliders = tk.Frame(self.middle_section, bg=self.background_colour)
        self.sliders.pack(side=tk.TOP)
        # Red Slider
        self.red_slider = tk.Scale(self.sliders, from_=255, to=0, bg="#f99", highlightthickness=0)
        self.red_slider.bind("<ButtonRelease-1>",
                             lambda event: self.preview_colour(self.red_slider.get(), self.green_slider.get(),
                                                               self.blue_slider.get()))
        self.red_slider.bind("<B1-Motion>",
                             lambda event: self.preview_colour(self.red_slider.get(), self.green_slider.get(),
                                                               self.blue_slider.get()))
        self.red_slider.pack(side=tk.LEFT, padx=20, pady=10)
        # Green Slider
        self.green_slider = tk.Scale(self.sliders, from_=255, to=0, bg="#9f9", highlightthickness=0)
        self.green_slider.bind("<ButtonRelease-1>",
                               lambda event: self.preview_colour(self.red_slider.get(), self.green_slider.get(),
                                                                 self.blue_slider.get()))
        self.green_slider.bind("<B1-Motion>",
                               lambda event: self.preview_colour(self.red_slider.get(), self.green_slider.get(),
                                                                 self.blue_slider.get()))
        self.green_slider.pack(side=tk.LEFT, padx=20, pady=10)

        # Blue Slider
        self.blue_slider = tk.Scale(self.sliders, from_=255, to=0, bg="#99f", highlightthickness=0)
        self.blue_slider.bind("<ButtonRelease-1>",
                              lambda event: self.preview_colour(self.red_slider.get(), self.green_slider.get(),
                                                                self.blue_slider.get()))
        self.blue_slider.bind("<B1-Motion>",
                              lambda event: self.preview_colour(self.red_slider.get(), self.green_slider.get(),
                                                                self.blue_slider.get()))
        self.blue_slider.pack(side=tk.LEFT, padx=20, pady=10)

        # Bottom Section
        self.bottom_section = tk.Frame(self.window, bg=self.background_colour)
        self.bottom_section.pack(side=tk.TOP)

        self.store_colour = tk.Button(self.bottom_section, text="Store Colour",
                                      command=lambda: self.add_to_file(self.colour_display["background"]))
        self.store_colour.pack(pady=10)

        self.display_stored_colours = tk.Canvas(self.bottom_section, width=301, height=101, bg='#fff', bd=0,
                                                highlightthickness=0)
        self.display_stored_colours.pack(side=tk.TOP)

        self.display_colours()
        # Starts the window running
        self.window.mainloop()

    def add_to_file(self, hex_string):
        colours = None
        if not os.path.exists("colour_file.json"):
            file = open("colour_file.json", "w+")
        with open("colour_file.json") as file:
            try:
                data = json.load(file)
                try:
                    colours = data
                    colours["list"].append(hex_string)
                except ValueError:
                    print(f"Exception {ValueError}")
                    colours = {"list": [hex_string]}
            except:
                colours = {"list": [hex_string]}
        with open("colour_file.json", "w") as file:
            json.dump(colours, file)
        self.display_colours()

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
        self.preview_colour(colour[0], colour[1], colour[2])  #

    def remove_hex_colour(self, hex_string):
        with open("colour_file.json", 'r') as file:
            data = json.load(file)
            colours = data
            colours["list"].remove(hex_string)

        with open("colour_file.json", 'w') as file:
            file.write(json.dumps(colours))

        self.display_colours()

    def display_colours(self):
        self.display_stored_colours.delete("all")
        if os.path.exists("colour_file.json"):
            with open("colour_file.json") as file:
                try:
                    data = json.load(file)

                    index = 0
                    xpos = 0
                    ypos = 0
                    for row in range(4):
                        for col in range(12):
                            if index < len(data["list"]):
                                rect = self.display_stored_colours.create_rectangle(xpos, ypos, xpos + 25, ypos + 25,
                                                                                    fill=data["list"][index])
                                self.display_stored_colours.tag_bind(rect, "<Button-1>", lambda event,
                                                                                                hex=self.display_stored_colours.itemcget(
                                                                                                    rect,
                                                                                                    "fill"): self.preview_hex_colour(
                                    hex))
                                self.display_stored_colours.tag_bind(rect, "<Button-3>", lambda event,
                                                                                                hex=self.display_stored_colours.itemcget(
                                                                                                    rect,
                                                                                                    "fill"): self.remove_hex_colour(
                                    hex))
                                index += 1
                            xpos += 25
                        xpos = 0
                        ypos += 25
                except:
                    pass


print(int("f", 16))
value = ColourPickerWindow()
