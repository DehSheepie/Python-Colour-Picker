import tkinter as tk
from tkinter import messagebox
import json
from os import path
from os import remove as rm
from random import randint


# saved for later hehe ^-^
# https://stackoverflow.com/questions/4969543/colour-chart-for-tkinter-and-tix

def hex_to_rgb(hex_string: str) -> tuple:
    string = hex_string[1:]
    r = f"{int(string[0] + string[1], 16)}"
    g = f"{int(string[2] + string[3], 16)}"
    b = f"{int(string[4] + string[5], 16)}"
    return r, g, b


def check_valid_colour_value(colour_value: str) -> int:
    try:
        colour = int(colour_value)
        if 0 <= colour < 256:
            return colour
        else:
            return -1
    except:
        return -1


class ColourPickerWindow:
    def __init__(self):
        # Attributes
        self.background_colour = "grey55"
        self.delete_popup = True

        self.window = tk.Tk()
        self.window.title("Colour Picker")
        self.window.geometry("600x600")
        self.window.minsize(400, 300)

        # Top Section
        self.top_section = tk.Frame(self.window, bg=self.background_colour)
        self.top_section.pack(side=tk.TOP, pady=10)

        # Colour Display
        self.colour_display = tk.Canvas(self.top_section, width=300, height=100, bg='#666', bd=1,
                                        highlightbackground="black")
        self.colour_display.pack(pady=10, side=tk.TOP)

        # Hex Value
        self.hex_value_section = tk.Frame(self.top_section, bg=self.background_colour)
        self.hex_value_section.pack(padx=10, pady=10, side=tk.TOP)

        # Random Colour Button
        self.random_colour = tk.Button(self.hex_value_section, text="Random Colour",
                                       command=self.generate_random_colour)
        self.random_colour.pack(side=tk.LEFT, padx=10)

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

        # Where randomise buttons will be added for each colour component
        self.colour_inputs_random_buttons = tk.Frame(self.top_section, bg=self.background_colour)
        self.colour_inputs_random_buttons.pack(side=tk.TOP, pady=10)

        # Red input
        self.red_input = tk.Entry(self.colour_inputs, textvariable=tk.StringVar(self.window, value='0'))
        self.red_input.pack(side=tk.LEFT, padx=10)
        self.red_input.bind("<KeyRelease>",
                            lambda event: self.preview_colour(self.red_input.get(), self.green_input.get(),
                                                              self.blue_input.get()))
        # Green input
        self.green_input = tk.Entry(self.colour_inputs, textvariable=tk.StringVar(self.window, value='0'))
        self.green_input.pack(side=tk.LEFT, padx=10)
        self.green_input.bind("<KeyRelease>",
                              lambda event: self.preview_colour(self.red_input.get(), self.green_input.get(),
                                                                self.blue_input.get()))

        # Blue input
        self.blue_input = tk.Entry(self.colour_inputs, textvariable=tk.StringVar(self.window, value='0'))
        self.blue_input.pack(side=tk.LEFT, padx=10)
        self.blue_input.bind("<KeyRelease>",
                             lambda event: self.preview_colour(self.red_input.get(), self.green_input.get(),
                                                               self.blue_input.get()))

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

        self.bottom_buttons = tk.Frame(self.bottom_section, bg=self.background_colour)
        self.bottom_buttons.pack(side=tk.TOP, pady=10)

        self.delete_all = tk.Button(self.bottom_buttons, text="Delete All", command=self.delete_all_colours)
        self.delete_all.pack(padx=10)

        # Red input randomizer
        self.red_input_random = tk.Button(self.colour_inputs_random_buttons, text="Randomise Red",
                                          command=lambda: self.preview_colour(str(randint(0, 255)),
                                                                              self.green_input.get(),
                                                                              self.blue_input.get()))
        self.red_input_random.pack(side=tk.LEFT, padx=10)

        # Green input randomizer
        self.green_input_random = tk.Button(self.colour_inputs_random_buttons, text="Randomise Green",
                                            command=lambda: self.preview_colour(self.red_input.get(),
                                                                                str(randint(0, 255)),
                                                                                self.blue_input.get()))
        self.green_input_random.pack(side=tk.LEFT, padx=10)

        # Blue input randomizer
        self.blue_input_random = tk.Button(self.colour_inputs_random_buttons, text="Randomise Blue",
                                           command=lambda: self.preview_colour(self.red_input.get(),
                                                                               self.green_input.get(),
                                                                               str(randint(0, 255))))
        self.blue_input_random.pack(side=tk.LEFT, padx=10)

        # Menu Bar
        self.main_menu = tk.Menu(self.window)

        # Options Menu
        self.options_menu = tk.Menu(self.main_menu, tearoff=False)

        # Theme Menu
        self.theme_menu = tk.Menu(self.options_menu, tearoff=False)
        self.theme_menu.add_command(label="Default", command=lambda: self.change_theme("gainsboro"))
        self.theme_menu.add_command(label="Dark", command=lambda: self.change_theme("grey55"))
        self.theme_menu.add_command(label="Darker", command=lambda: self.change_theme("grey24"))
        self.theme_menu.add_command(label="Super Dark", command=lambda: self.change_theme("grey6"))
        self.theme_menu.add_command(label="Velvet", command=lambda: self.change_theme("brown4"))
        self.theme_menu.add_command(label="Custom", command=lambda: self.change_theme(self.hex_input.get()))

        self.options_menu.add_command(label="Turn off Delete Popup", command=self.toggle_delete_popup)
        self.options_menu.add_cascade(label="Themes", menu=self.theme_menu)

        self.main_menu.add_cascade(label="Options", menu=self.options_menu)
        self.window.config(bg=self.background_colour, menu=self.main_menu)
        # Starts the window running
        self.window.mainloop()

    def change_theme(self, new_colour: str):
        try:
            self.background_colour = new_colour
            self.window.config(bg=self.background_colour)
            self.top_section.config(bg=self.background_colour)
            self.hex_value_section.config(bg=self.background_colour)
            self.colour_inputs.config(bg=self.background_colour)
            self.colour_inputs_random_buttons.config(bg=self.background_colour)
            self.middle_section.config(bg=self.background_colour)
            self.sliders.config(bg=self.background_colour)
            self.bottom_section.config(bg=self.background_colour)
            self.bottom_buttons.config(bg=self.background_colour)
        except:
            self.background_colour = new_colour
            self.window.config(bg="gainsboro")
            self.top_section.config(bg="gainsboro")
            self.hex_value_section.config(bg="gainsboro")
            self.colour_inputs.config(bg="gainsboro")
            self.colour_inputs_random_buttons.config(bg="gainsboro")
            self.middle_section.config(bg="gainsboro")
            self.sliders.config(bg="gainsboro")
            self.bottom_section.config(bg="gainsboro")
            self.bottom_buttons.config(bg="gainsboro")

    def toggle_delete_popup(self) -> None:
        self.delete_popup = not self.delete_popup
        if self.delete_popup:
            self.options_menu.entryconfigure(0, label="Turn off Delete Popup")
        else:
            self.options_menu.entryconfigure(0, label="Turn on Delete Popup")

    def delete_all_colours(self):
        response = tk.messagebox.askyesno(title="Remove Colour",
                                          message=f"Are you sure you want to remove all colours from the list?\nThis action cannot be undone.")
        if response:
            if path.exists("colour_file.json"):
                rm("colour_file.json")
            else:
                tk.messagebox.showinfo(title="No Colours", message="No colours could be found in storage.")
        self.display_colours()

    def generate_random_colour(self):
        self.preview_colour(f"{randint(0, 255)}", f"{randint(0, 255)}", f"{randint(0, 255)}")

    def add_to_file(self, hex_string):
        colours = None
        if not path.exists("colour_file.json"):
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

    def preview_colour(self, red: str, green: str, blue: str):

        validated_red = check_valid_colour_value(red)
        validated_green = check_valid_colour_value(green)
        validated_blue = check_valid_colour_value(blue)

        colour = f"#{validated_red if validated_red != -1 else 0:02x}{validated_green if validated_green != -1 else 0:02x}{validated_blue if validated_blue != -1 else 0:02x}"
        self.hex_input.delete(0, "end")
        self.hex_input.insert(0, colour)
        self.colour_display.config(bg=colour)
        if validated_red != -1:
            self.red_input.delete(0, "end")
            self.red_input.insert(0, red)
        if validated_green != -1:
            self.green_input.delete(0, "end")
            self.green_input.insert(0, green)
        if validated_blue != -1:
            self.blue_input.delete(0, "end")
            self.blue_input.insert(0, blue)
        self.red_slider.set(validated_red)
        self.green_slider.set(validated_green)
        self.blue_slider.set(validated_blue)

    def preview_hex_colour(self, hex_string: str):
        try:
            colour = hex_to_rgb(hex_string)
            self.preview_colour(colour[0], colour[1], colour[2])
        except:
            self.preview_colour("0", "0", "0")

    def remove_hex_colour(self, hex_string):
        if self.delete_popup:
            confirmation = tk.messagebox.askyesno(title="Remove Colour",
                                                  message=f"Are you sure you want to remove {hex_string} from the "
                                                          f"list?\n\nThis popup can be disabled in the options menu.")
        else:
            # If the delete popup has been disabled confirm the action automatically
            confirmation = True
        if confirmation:
            with open("colour_file.json", 'r') as file:
                data = json.load(file)
                colours = data
                colours["list"].remove(hex_string)

            with open("colour_file.json", 'w') as file:
                file.write(json.dumps(colours))

            self.display_colours()

    def display_colours(self):
        self.display_stored_colours.delete("all")
        if path.exists("colour_file.json"):
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


value = ColourPickerWindow()
