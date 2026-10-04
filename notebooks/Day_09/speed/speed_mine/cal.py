import cv2
import json
import os
import tkinter as tk
from tkinter import simpledialog, messagebox
from PIL import Image, ImageTk


# ============================================================
# SETTINGS
# ============================================================

VIDEO_PATH = r"C:\Users\PC-LAB1\Desktop\server\uploads\shok_cam_test.mp4"

OUTPUT_DIR = r"C:\Users\PC-LAB1\Desktop\server\uploads\speed_calibration"

CALIBRATION_FILE = os.path.join(
    OUTPUT_DIR,
    "road_calibration.json"
)

IMAGE_FILE = os.path.join(
    OUTPUT_DIR,
    "road_calibration.jpg"
)


# ============================================================
# LOAD FIRST FRAME
# ============================================================

cap = cv2.VideoCapture(VIDEO_PATH)

if not cap.isOpened():
    raise RuntimeError(
        f"Could not open video:\n{VIDEO_PATH}"
    )

ret, frame = cap.read()
cap.release()

if not ret:
    raise RuntimeError(
        "Could not read first frame."
    )

height, width = frame.shape[:2]


print()
print("========================================")
print("ROAD CALIBRATION")
print("========================================")
print(f"Frame size: {width} x {height}")
print()
print("LEFT ROAD EDGE")
print("  Click points following the LEFT edge.")
print()
print("Press R")
print()
print("RIGHT ROAD EDGE")
print("  Click points following the RIGHT edge.")
print()
print("Press S to save.")
print()
print("U = undo")
print("C = clear current side")
print("L = left side")
print("R = right side")
print("ESC = cancel")
print("========================================")


# ============================================================
# POINT STORAGE
# ============================================================

left_points = []
right_points = []

current_side = "LEFT"


# ============================================================
# TKINTER
# ============================================================

root = tk.Tk()

root.title(
    "Road Calibration"
)

canvas = tk.Canvas(
    root,
    width=width,
    height=height
)

canvas.pack()


# ============================================================
# FRAME
# ============================================================

rgb = cv2.cvtColor(
    frame,
    cv2.COLOR_BGR2RGB
)

pil_image = Image.fromarray(
    rgb
)

photo = ImageTk.PhotoImage(
    pil_image
)

canvas.create_image(
    0,
    0,
    anchor=tk.NW,
    image=photo
)

canvas.photo = photo


# ============================================================
# DRAW
# ============================================================

def redraw():

    canvas.delete(
        "calibration"
    )

    # --------------------------------------------------------
    # LEFT LINE
    # --------------------------------------------------------

    if len(left_points) >= 2:

        for i in range(
            len(left_points) - 1
        ):

            x1, y1 = left_points[i]
            x2, y2 = left_points[i + 1]

            canvas.create_line(
                x1,
                y1,
                x2,
                y2,
                fill="red",
                width=3,
                tags="calibration"
            )


    # --------------------------------------------------------
    # RIGHT LINE
    # --------------------------------------------------------

    if len(right_points) >= 2:

        for i in range(
            len(right_points) - 1
        ):

            x1, y1 = right_points[i]
            x2, y2 = right_points[i + 1]

            canvas.create_line(
                x1,
                y1,
                x2,
                y2,
                fill="blue",
                width=3,
                tags="calibration"
            )


    # --------------------------------------------------------
    # LEFT POINTS
    # --------------------------------------------------------

    for i, (x, y) in enumerate(
        left_points
    ):

        canvas.create_oval(
            x - 5,
            y - 5,
            x + 5,
            y + 5,
            fill="red",
            outline="white",
            width=1,
            tags="calibration"
        )

        canvas.create_text(
            x + 10,
            y - 10,
            text=str(i + 1),
            fill="red",
            font=("Arial", 10, "bold"),
            tags="calibration"
        )


    # --------------------------------------------------------
    # RIGHT POINTS
    # --------------------------------------------------------

    for i, (x, y) in enumerate(
        right_points
    ):

        canvas.create_oval(
            x - 5,
            y - 5,
            x + 5,
            y + 5,
            fill="blue",
            outline="white",
            width=1,
            tags="calibration"
        )

        canvas.create_text(
            x + 10,
            y - 10,
            text=str(i + 1),
            fill="blue",
            font=("Arial", 10, "bold"),
            tags="calibration"
        )


    # --------------------------------------------------------
    # YELLOW ROAD CROSS-SECTIONS
    # --------------------------------------------------------

    count = min(
        len(left_points),
        len(right_points)
    )

    for i in range(count):

        lx, ly = left_points[i]
        rx, ry = right_points[i]

        canvas.create_line(
            lx,
            ly,
            rx,
            ry,
            fill="yellow",
            width=1,
            tags="calibration"
        )


    # --------------------------------------------------------
    # INFO
    # --------------------------------------------------------

    canvas.create_rectangle(
        10,
        10,
        390,
        115,
        fill="black",
        outline="white",
        tags="calibration"
    )

    canvas.create_text(
        20,
        28,
        anchor=tk.W,
        text=f"CURRENT: {current_side}",
        fill="white",
        font=("Arial", 14, "bold"),
        tags="calibration"
    )

    canvas.create_text(
        20,
        52,
        anchor=tk.W,
        text="L = Left    R = Right",
        fill="white",
        font=("Arial", 11),
        tags="calibration"
    )

    canvas.create_text(
        20,
        74,
        anchor=tk.W,
        text="U = Undo    C = Clear",
        fill="white",
        font=("Arial", 11),
        tags="calibration"
    )

    canvas.create_text(
        20,
        96,
        anchor=tk.W,
        text="S = Save    ESC = Cancel",
        fill="white",
        font=("Arial", 11),
        tags="calibration"
    )


# ============================================================
# MOUSE
# ============================================================

def mouse_click(event):

    if current_side == "LEFT":

        left_points.append(
            [float(event.x), float(event.y)]
        )

        print(
            f"LEFT {len(left_points)}: "
            f"({event.x:.1f}, {event.y:.1f})"
        )

    else:

        right_points.append(
            [float(event.x), float(event.y)]
        )

        print(
            f"RIGHT {len(right_points)}: "
            f"({event.x:.1f}, {event.y:.1f})"
        )

    redraw()


canvas.bind(
    "<Button-1>",
    mouse_click
)


# ============================================================
# SAVE
# ============================================================

def save_calibration():

    if len(left_points) < 2:

        messagebox.showerror(
            "Error",
            "Add at least 2 LEFT points."
        )

        return

    if len(right_points) < 2:

        messagebox.showerror(
            "Error",
            "Add at least 2 RIGHT points."
        )

        return


    # --------------------------------------------------------
    # ASK REAL WIDTH
    # --------------------------------------------------------

    road_width = simpledialog.askfloat(
        "Road Width",
        "Enter the measured road width in meters:",
        parent=root,
        minvalue=0.1
    )

    if road_width is None:
        return


    # --------------------------------------------------------
    # ASK REAL LENGTH
    # --------------------------------------------------------

    road_length = simpledialog.askfloat(
        "Road Length",
        "Enter the measured road length in meters:",
        parent=root,
        minvalue=0.1
    )

    if road_length is None:
        return


    # --------------------------------------------------------
    # CREATE DIRECTORY
    # --------------------------------------------------------

    os.makedirs(
        OUTPUT_DIR,
        exist_ok=True
    )


    # --------------------------------------------------------
    # SAVE JSON
    # --------------------------------------------------------

    calibration = {

        "video": VIDEO_PATH,

        "frame_width": width,

        "frame_height": height,

        "road_width_m": road_width,

        "road_length_m": road_length,

        "left_boundary": left_points,

        "right_boundary": right_points
    }


    with open(
        CALIBRATION_FILE,
        "w"
    ) as f:

        json.dump(
            calibration,
            f,
            indent=4
        )


    # --------------------------------------------------------
    # SAVE IMAGE
    # --------------------------------------------------------

    save_frame = frame.copy()


    if len(left_points) >= 2:

        pts = cv2.UMat(
            cv2.array(left_points)
        )


    # Draw left
    for i in range(
        len(left_points) - 1
    ):

        p1 = tuple(
            map(
                int,
                left_points[i]
            )
        )

        p2 = tuple(
            map(
                int,
                left_points[i + 1]
            )
        )

        cv2.line(
            save_frame,
            p1,
            p2,
            (0, 0, 255),
            3
        )


    # Draw right
    for i in range(
        len(right_points) - 1
    ):

        p1 = tuple(
            map(
                int,
                right_points[i]
            )
        )

        p2 = tuple(
            map(
                int,
                right_points[i + 1]
            )
        )

        cv2.line(
            save_frame,
            p1,
            p2,
            (255, 0, 0),
            3
        )


    # Draw points
    for x, y in left_points:

        cv2.circle(
            save_frame,
            (int(x), int(y)),
            5,
            (0, 0, 255),
            -1
        )


    for x, y in right_points:

        cv2.circle(
            save_frame,
            (int(x), int(y)),
            5,
            (255, 0, 0),
            -1
        )


    cv2.imwrite(
        IMAGE_FILE,
        save_frame
    )


    print()
    print("========================================")
    print("CALIBRATION SAVED")
    print("========================================")
    print(
        f"Road width : {road_width} m"
    )
    print(
        f"Road length: {road_length} m"
    )
    print()
    print(CALIBRATION_FILE)
    print()
    print(IMAGE_FILE)


    messagebox.showinfo(
        "Saved",
        "Calibration saved successfully."
    )

    root.destroy()


# ============================================================
# KEYBOARD
# ============================================================

def key_pressed(event):

    global current_side

    key = event.keysym.lower()


    if key == "l":

        current_side = "LEFT"

        print(
            "\nCurrent side: LEFT"
        )

        redraw()


    elif key == "r":

        current_side = "RIGHT"

        print(
            "\nCurrent side: RIGHT"
        )

        redraw()


    elif key == "u":

        if current_side == "LEFT":

            if left_points:

                removed = left_points.pop()

                print(
                    "Removed LEFT:",
                    removed
                )

        else:

            if right_points:

                removed = right_points.pop()

                print(
                    "Removed RIGHT:",
                    removed
                )

        redraw()


    elif key == "c":

        if current_side == "LEFT":

            left_points.clear()

            print(
                "LEFT cleared."
            )

        else:

            right_points.clear()

            print(
                "RIGHT cleared."
            )

        redraw()


    elif key == "s":

        save_calibration()


    elif key == "escape":

        print(
            "Calibration cancelled."
        )

        root.destroy()


root.bind(
    "<Key>",
    key_pressed
)


# ============================================================
# START
# ============================================================

redraw()

root.mainloop()