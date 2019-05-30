options(stringsAsFactors = FALSE)
library(hexSticker)
library(showtext)
font_add_google("Quicksand", "qs")  # google font name, name in R
font_add_google("Gloria Hallelujah", "gh")  # google font name, name in R
showtext_auto()

img = "https://cdn.pixabay.com/photo/2016/03/19/04/40/cap-1266204_960_720.png"

sticker(img,
        package="pypeds",
        p_size=8, p_y = 0.57,
        p_family = "gh",
        s_x=1, s_y=1.2,  # position
        s_width=.8, s_height=.8,
        h_fill = "grey", h_color="#36454f", p_color = "#536878",
        filename="pypeds_hexSticker.png")
