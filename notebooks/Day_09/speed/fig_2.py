import cv2
import json
import os
import tkinter as tk
from PIL import Image, ImageTk


# ============================================================
# PATHS
# ============================================================

VIDEO_PATH = r"C:\Users\PC-LAB1\Desktop\New folder\Test Video.mp4"

OUTPUT_DIR = r"C:\Users\PC-LAB1\Desktop\New folder\calibration"

CALIBRATION_FILE = os.path.join(
    OUTPUT_DIR,
    "road_calibration.json"
)

IMAGE_FILE = os.path.join(
    OUTPUT_DIR,
    "road_calibration.jpg"
)


# ============================================================
# LOAD FIRST VIDEO FRAME
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
        "Could not read the first frame."
    )


height, width = frame.shape[:2]

print()
print("========================================")
print("ROAD CALIBRATION")
print("========================================")

print(
    f"Frame size: {width} x {height}"
)

print()
print("HOW TO USE")
print("----------------------------------------")
print("LEFT SIDE:")
print("  Click several points along the LEFT")
print("  edge of the road.")
print()
print("RIGHT SIDE:")
print("  Press R, then click several points")
print("  along the RIGHT edge of the road.")
print()
print("SAVE:")
print("  Press S")
print()
print("OTHER:")
print("  L = select LEFT")
print("  R = select RIGHT")
print("  U = undo last point")
print("  C = clear current side")
print("  ESC = cancel")
print()
print("IMPORTANT:")
print("Click the actual road edges.")
print("Do NOT click vehicles.")
print("Follow the curve of the road.")
print("========================================")


# ============================================================
# POINT STORAGE
# ============================================================

left_points = []
right_points = []

current_side = "LEFT"


# ============================================================
# CREATE WINDOW
# ============================================================

root = tk.Tk()

root.title(
    "Road Calibration - Click Road Boundaries"
)


# ============================================================
# CANVAS
# ============================================================

canvas = tk.Canvas(
    root,
    width=width,
    height=height
)

canvas.pack()


# ============================================================
# CONVERT OPENCV -> PIL
# ============================================================

frame_rgb = cv2.cvtColor(
    frame,
    cv2.COLOR_BGR2RGB
)

image = Image.fromarray(
    frame_rgb
)

photo = ImageTk.PhotoImage(
    image
)


canvas.create_image(
    0,
    0,
    anchor=tk.NW,
    image=photo
)


# Keep reference alive
canvas.photo = photo


# ============================================================
# DRAW EVERYTHING
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
            x - 4,
            y - 4,
            x + 4,
            y + 4,
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
            x - 4,
            y - 4,
            x + 4,
            y + 4,
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
    # CONNECT LEFT/RIGHT VISUALLY
    # --------------------------------------------------------

    if (
        len(left_points) >= 2
        and
        len(right_points) >= 2
    ):

        # Match points by index where possible

        count = min(
            len(left_points),
            len(right_points)
        )

        for i in range(
            count
        ):

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
    # INFO PANEL
    # --------------------------------------------------------

    canvas.create_rectangle(
        10,
        10,
        370,
        105,
        fill="black",
        outline="white",
        tags="calibration"
    )


    canvas.create_text(
        20,
        28,
        anchor=tk.W,
        text=f"CURRENT SIDE: {current_side}",
        fill="white",
        font=("Arial", 14, "bold"),
        tags="calibration"
    )


    canvas.create_text(
        20,
        50,
        anchor=tk.W,
        text="L = Left     R = Right",
        fill="white",
        font=("Arial", 11),
        tags="calibration"
    )


    canvas.create_text(
        20,
        70,
        anchor=tk.W,
        text="U = Undo     C = Clear",
        fill="white",
        font=("Arial", 11),
        tags="calibration"
    )


    canvas.create_text(
        20,
        90,
        anchor=tk.W,
        text="S = Save     ESC = Cancel",
        fill="white",
        font=("Arial", 11),
        tags="calibration"
    )


# ============================================================
# MOUSE CLICK
# ============================================================

def mouse_click(event):

    global left_points
    global right_points

    x = event.x
    y = event.y

    if current_side == "LEFT":

        left_points.append(
            [float(x), float(y)]
        )

        print(
            f"LEFT {len(left_points)}: "
            f"({x:.1f}, {y:.1f})"
        )

    else:

        right_points.append(
            [float(x), float(y)]
        )

        print(
            f"RIGHT {len(right_points)}: "
            f"({x:.1f}, {y:.1f})"
        )

    redraw()


canvas.bind(
    "<Button-1>",
    mouse_click
)


# ============================================================
# KEYBOARD
# ============================================================

def key_pressed(event):

    global current_side

    key = event.keysym.lower()


    # --------------------------------------------------------
    # LEFT
    # --------------------------------------------------------

    if key == "l":

        current_side = "LEFT"

        print()
        print("Current side: LEFT")

        redraw()


    # --------------------------------------------------------
    # RIGHT
    # --------------------------------------------------------

    elif key == "r":

        current_side = "RIGHT"

        print()
        print("Current side: RIGHT")

        redraw()


    # --------------------------------------------------------
    # UNDO
    # --------------------------------------------------------

    elif key == "u":

        if current_side == "LEFT":

            if len(left_points) > 0:

                removed = left_points.pop()

                print(
                    "Removed LEFT:",
                    removed
                )

        else:

            if len(right_points) > 0:

                removed = right_points.pop()

                print(
                    "Removed RIGHT:",
                    removed
                )

        redraw()


    # --------------------------------------------------------
    # CLEAR CURRENT SIDE
    # --------------------------------------------------------

    elif key == "c":

        if current_side == "LEFT":

            left_points.clear()

            print(
                "LEFT points cleared."
            )

        else:

            right_points.clear()

            print(
                "RIGHT points cleared."
            )

        redraw()


    # --------------------------------------------------------
    # SAVE
    # --------------------------------------------------------

    elif key == "s":

        save_calibration()


    # --------------------------------------------------------
    # ESC
    # --------------------------------------------------------

    elif key == "escape":

        print()
        print(
            "Calibration cancelled."
        )

        root.destroy()


root.bind(
    "<Key>",
    key_pressed
)


# ============================================================
# SAVE CALIBRATION
# ============================================================

def save_calibration():

    if len(left_points) < 2:

        print()
        print(
            "ERROR: Need at least 2 LEFT points."
        )

        return


    if len(right_points) < 2:

        print()
        print(
            "ERROR: Need at least 2 RIGHT points."
        )

        return


    os.makedirs(
        OUTPUT_DIR,
        exist_ok=True
    )


    # --------------------------------------------------------
    # JSON
    # --------------------------------------------------------

    calibration = {

        "video": VIDEO_PATH,

        "frame_width": width,

        "frame_height": height,

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
    # SAVE VISUALIZATION
    # --------------------------------------------------------

    save_image = frame.copy()


    # LEFT
    if len(left_points) >= 2:

        pts = np.array(
            left_points,
            dtype=np.int32
        )

        cv2.polylines(
            save_image,
            [pts],
            False,
            (0, 0, 255),
            3
        )


    # RIGHT
    if len(right_points) >= 2:

        pts = np.array(
            right_points,
            dtype=np.int32
        )

        cv2.polylines(
            save_image,
            [pts],
            False,
            (255, 0, 0),
            3
        )


    # POINTS
    for x, y in left_points:

        cv2.circle(
            save_image,
            (int(x), int(y)),
            5,
            (0, 0, 255),
            -1
        )


    for x, y in right_points:

        cv2.circle(
            save_image,
            (int(x), int(y)),
            5,
            (255, 0, 0),
            -1
        )


    cv2.imwrite(
        IMAGE_FILE,
        save_image
    )


    # --------------------------------------------------------
    # PRINT
    # --------------------------------------------------------

    print()
    print("========================================")
    print("CALIBRATION SAVED")
    print("========================================")

    print()
    print(
        f"LEFT points : {len(left_points)}"
    )

    print(
        f"RIGHT points: {len(right_points)}"
    )

    print()
    print(
        "JSON:"
    )

    print(
        CALIBRATION_FILE
    )

    print()
    print(
        "Visualization:"
    )

    print(
        IMAGE_FILE
    )

    print()
    print("You can now close the window.")

    root.destroy()


# ============================================================
# INITIAL DRAW
# ============================================================

redraw()


# ============================================================
# START
# ============================================================

root.mainloop()