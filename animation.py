import tkinter as tk
import random
from PIL import Image, ImageTk, ImageDraw

root = tk.Tk()
root.title("Bouncing Burger")
canvas = tk.Canvas(root, width=600, height=400, bg="black")
canvas.pack()

# Load and crop burger image to a circle
size = (120, 120)
burger_img_raw = Image.open("burger.jpg").resize(size).convert("RGBA")

# Create a circular mask
mask = Image.new("L", size, 0)
draw = ImageDraw.Draw(mask)
draw.ellipse((0, 0) + size, fill=255)

# Apply mask to image
burger_img_circle = Image.new("RGBA", size)
burger_img_circle.paste(burger_img_raw, (0, 0), mask=mask)

burger_img = ImageTk.PhotoImage(burger_img_circle)
img_width, img_height = burger_img.width(), burger_img.height()

x, y = 300, 200  # gitna ng canvas
dx, dy = 2, 2    # mas mabagal na galaw

# Create burger image on canvas
ball = canvas.create_image(x, y, image=burger_img)

text = "JERICK P. ABELLAR"
initial_font_size = 18
font_family = "Arial"
font_style = "bold"

def random_color():
    # Generate a random color in hex format
    return "#%06x" % random.randint(0, 0xFFFFFF)

def create_text_with_bg_stuck_to_edge(x, y, text, font_size):
    font = (font_family, font_size, font_style)
    temp_text = canvas.create_text(x, y, text=text, font=font)
    bbox = canvas.bbox(temp_text)
    canvas.delete(temp_text)

    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    # Limit rectangle to 70% of burger width and 28% of burger height
    max_width = img_width * 0.70
    max_height = img_height * 0.28

    # Scale down font if needed
    scale_factor = min(1, max_width / text_width, max_height / text_height)
    adjusted_font_size = max(8, int(font_size * scale_factor))
    font = (font_family, adjusted_font_size, font_style)

    # Recompute text and bbox with new font size
    text_id = canvas.create_text(x, y, text=text, fill="black", font=font)
    bbox = canvas.bbox(text_id)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    pad_x = 6  # mas maliit na padding
    pad_y = 2
    rect_left = x - text_width / 2 - pad_x
    rect_right = x + text_width / 2 + pad_x
    rect_top = y - text_height / 2 - pad_y
    rect_bottom = y + text_height / 2 + pad_y

    rect_bg = canvas.create_rectangle(
        rect_left, rect_top,
        rect_right, rect_bottom,
        fill="white", outline="black", width=3
    )

    canvas.tag_raise(text_id, rect_bg)
    return text_id, rect_bg

ball_text, rect_bg = create_text_with_bg_stuck_to_edge(x, y, text, initial_font_size)

paused = False

def update():
    global x, y, dx, dy
    if not paused:
        x += dx
        y += dy

        bounced = False

        # Collision detection for image
        if x - img_width // 2 <= 0 or x + img_width // 2 >= 600:
            dx = -dx
            bounced = True
        if y - img_height // 2 <= 0 or y + img_height // 2 >= 400:
            dy = -dy
            bounced = True

        if bounced:
            # Randomize name color and rectangle outline
            new_color = random_color()
            canvas.itemconfig(ball_text, fill=new_color)
            canvas.itemconfig(rect_bg, outline=new_color)

        # Move burger image
        canvas.coords(ball, x, y)
        # Center text on burger
        canvas.coords(ball_text, x, y)
         # Rectangle background (auto-fit sa loob ng bilog)
        bbox = canvas.bbox(ball_text)
        pad_x = 6
        pad_y = 2
        rect_left = bbox[0] - pad_x
        rect_top = bbox[1] - pad_y
        rect_right = bbox[2] + pad_x
        rect_bottom = bbox[3] + pad_y
        canvas.coords(rect_bg, rect_left, rect_top, rect_right, rect_bottom)

    root.after(16, update)

def toggle_pause(event=None):
    global paused
    paused = not paused

root.bind("<space>", toggle_pause)
update()
root.mainloop()