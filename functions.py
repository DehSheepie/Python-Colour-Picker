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