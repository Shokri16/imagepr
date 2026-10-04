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

CALIBRATION_IMAGE = os.path.join(
    OUTPUT_DIR,
    "road_calibration.jpg"
)

BIRD_EYE_IMAGE = os.path.join(
    OUTPUT_DIR,
    "bird_eye_view.jpg"
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
        "Could not read the first frame."
    )


height, width = frame.shape[:2]


# ============================================================
# INFORMATION
# ============================================================

print()
print("========================================")
print("4-CORNER ROAD CALIBRATION")
print("========================================")
print(f"Frame size: {width} x {height}")
print()
print("CLICK THE ROAD CORNERS IN THIS ORDER:")
print()
print("1. TOP-LEFT")
print("2. TOP-RIGHT")
print("3. BOTTOM-RIGHT")
print("4. BOTTOM-LEFT")
print()
print("Keyboard:")
print("U = undo last point")
print("C = clear all points")
print("S = save calibration")
print("ESC = cancel")
print("========================================")
print()


# ============================================================
# POINTS
# ============================================================

points = []

point_names = [
    "TOP-LEFT",
    "TOP-RIGHT",
    "BOTTOM-RIGHT",
    "BOTTOM-LEFT"
]


# ============================================================
# TKINTER
# ============================================================

root = tk.Tk()

root.title(
    "4-Corner Road Calibration"
)


canvas = tk.Canvas(
    root,
    width=width,
    height=height
)

canvas.pack()


# ============================================================
# IMAGE
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
    # DRAW POINTS
    # --------------------------------------------------------

    for i, (x, y) in enumerate(points):

        canvas.create_oval(
            x - 7,
            y - 7,
            x + 7,
            y + 7,
            fill="red",
            outline="white",
            width=2,
            tags="calibration"
        )

        canvas.create_text(
            x + 15,
            y - 15,
            text=str(i + 1),
            fill="yellow",
            font=("Arial", 16, "bold"),
            tags="calibration"
        )

        canvas.create_text(
            x + 15,
            y + 8,
            text=point_names[i],
            fill="white",
            font=("Arial", 10, "bold"),
            tags="calibration"
        )


    # --------------------------------------------------------
    # DRAW LINES
    # --------------------------------------------------------

    if len(points) >= 2:

        for i in range(
            len(points) - 1
        ):

            x1, y1 = points[i]
            x2, y2 = points[i + 1]

            canvas.create_line(
                x1,
                y1,
                x2,
                y2,
                fill="yellow",
                width=3,
                tags="calibration"
            )


    # --------------------------------------------------------
    # CLOSE QUADRILATERAL
    # --------------------------------------------------------

    if len(points) == 4:

        x1, y1 = points[3]
        x2, y2 = points[0]

        canvas.create_line(
            x1,
            y1,
            x2,
            y2,
            fill="yellow",
            width=3,
            tags="calibration"
        )


    # --------------------------------------------------------
    # INFORMATION PANEL
    # --------------------------------------------------------

    canvas.create_rectangle(
        10,
        10,
        390,
        125,
        fill="black",
        outline="white",
        tags="calibration"
    )


    if len(points) < 4:

        next_point = point_names[
            len(points)
        ]

        status = (
            f"Next: {next_point}"
        )

    else:

        status = "4 CORNERS SELECTED"


    canvas.create_text(
        20,
        30,
        anchor=tk.W,
        text=status,
        fill="white",
        font=("Arial", 14, "bold"),
        tags="calibration"
    )


    canvas.create_text(
        20,
        57,
        anchor=tk.W,
        text="U = Undo    C = Clear",
        fill="white",
        font=("Arial", 11),
        tags="calibration"
    )


    canvas.create_text(
        20,
        82,
        anchor=tk.W,
        text="S = Save    ESC = Cancel",
        fill="white",
        font=("Arial", 11),
        tags="calibration"
    )


    canvas.create_text(
        20,
        107,
        anchor=tk.W,
        text=f"Points: {len(points)}/4",
        fill="yellow",
        font=("Arial", 11, "bold"),
        tags="calibration"
    )


# ============================================================
# MOUSE CLICK
# ============================================================

def mouse_click(event):

    if len(points) >= 4:

        print(
            "Already have 4 points. "
            "Press S to save or C to restart."
        )

        return


    x = float(event.x)
    y = float(event.y)


    points.append(
        [x, y]
    )


    number = len(points)

    name = point_names[
        number - 1
    ]


    print(
        f"{number}. {name}: "
        f"({x:.1f}, {y:.1f})"
    )


    redraw()


canvas.bind(
    "<Button-1>",
    mouse_click
)


# ============================================================
# CREATE BIRD'S-EYE VIEW
# ============================================================

def create_bird_eye():

    src = (
        points
    )


    # --------------------------------------------------------
    # Destination dimensions
    #
    # 100 pixels = 1 meter
    # --------------------------------------------------------

    output_width = int(
        road_width_m * 100
    )

    output_height = int(
        road_length_m * 100
    )


    if output_width < 100:
        output_width = 100

    if output_height < 100:
        output_height = 100


    destination = [
        [0, 0],
        [output_width - 1, 0],
        [output_width - 1, output_height - 1],
        [0, output_height - 1]
    ]


    src_array = (
        __import__("numpy")
        .array(
            src,
            dtype="float32"
        )
    )


    dst_array = (
        __import__("numpy")
        .array(
            destination,
            dtype="float32"
        )
    )


    H = cv2.getPerspectiveTransform(
        src_array,
        dst_array
    )


    bird_eye = cv2.warpPerspective(
        frame,
        H,
        (
            output_width,
            output_height
        )
    )


    cv2.imwrite(
        BIRD_EYE_IMAGE,
        bird_eye
    )


    return H


# ============================================================
# SAVE
# ============================================================

def save_calibration():

    if len(points) != 4:

        messagebox.showerror(
            "Not enough points",
            "You must select exactly 4 corners."
        )

        return


    # --------------------------------------------------------
    # ROAD WIDTH
    # --------------------------------------------------------

    global road_width_m
    global road_length_m


    road_width_m = simpledialog.askfloat(
        "Road Width",
        "Enter the REAL measured road width in meters:",
        parent=root,
        minvalue=0.1
    )


    if road_width_m is None:
        return


    # --------------------------------------------------------
    # ROAD LENGTH
    # --------------------------------------------------------

    road_length_m = simpledialog.askfloat(
        "Road Length",
        "Enter the REAL measured road length in meters:",
        parent=root,
        minvalue=0.1
    )


    if road_length_m is None:
        return


    # --------------------------------------------------------
    # CREATE OUTPUT DIRECTORY
    # --------------------------------------------------------

    os.makedirs(
        OUTPUT_DIR,
        exist_ok=True
    )


    # --------------------------------------------------------
    # HOMOGRAPHY
    # --------------------------------------------------------

    H = create_bird_eye()


    # --------------------------------------------------------
    # SAVE JSON
    # --------------------------------------------------------

    calibration = {

        "video": VIDEO_PATH,

        "frame_width": width,

        "frame_height": height,

        "road_width_m": road_width_m,

        "road_length_m": road_length_m,

        "corners": {

            "top_left": points[0],

            "top_right": points[1],

            "bottom_right": points[2],

            "bottom_left": points[3]
        }
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
    # SAVE CALIBRATION IMAGE
    # --------------------------------------------------------

    save_frame = frame.copy()


    pts = [
        (
            int(x),
            int(y)
        )
        for x, y in points
    ]


    # Quadrilateral

    cv2.polylines(
        save_frame,
        [
            __import__("numpy").array(
                pts,
                dtype="int32"
            )
        ],
        True,
        (0, 255, 255),
        3
    )


    # Points

    for i, (x, y) in enumerate(pts):

        cv2.circle(
            save_frame,
            (x, y),
            8,
            (0, 0, 255),
            -1
        )

        cv2.putText(
            save_frame,
            f"{i + 1} {point_names[i]}",
            (x + 10, y - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (255, 255, 255),
            2,
            cv2.LINE_AA
        )


    cv2.imwrite(
        CALIBRATION_IMAGE,
        save_frame
    )


    # --------------------------------------------------------
    # SAVE HOMOGRAPHY
    # --------------------------------------------------------

    homography_file = os.path.join(
        OUTPUT_DIR,
        "homography.npy"
    )


    __import__("numpy").save(
        homography_file,
        H
    )


    # --------------------------------------------------------
    # OUTPUT
    # --------------------------------------------------------

    print()
    print("========================================")
    print("CALIBRATION COMPLETE")
    print("========================================")

    print(
        f"Road width : "
        f"{road_width_m:.2f} m"
    )

    print(
        f"Road length: "
        f"{road_length_m:.2f} m"
    )

    print()
    print(
        f"Calibration:"
    )
    print(
        CALIBRATION_FILE
    )

    print()
    print(
        f"Calibration image:"
    )
    print(
        CALIBRATION_IMAGE
    )

    print()
    print(
        f"Bird's-eye view:"
    )
    print(
        BIRD_EYE_IMAGE
    )

    print()
    print(
        f"Homography:"
    )
    print(
        homography_file
    )


    messagebox.showinfo(
        "Calibration Complete",
        "Calibration saved successfully!\n\n"
        f"Width: {road_width_m:.2f} m\n"
        f"Length: {road_length_m:.2f} m\n\n"
        "Check bird_eye_view.jpg before "
        "running the speed tracker."
    )


    root.destroy()


# ============================================================
# KEYBOARD
# ============================================================

def key_pressed(event):

    key = event.keysym.lower()


    # --------------------------------------------------------
    # UNDO
    # --------------------------------------------------------

    if key == "u":

        if points:

            removed = points.pop()

            print(
                "Removed:",
                removed
            )

        redraw()


    # --------------------------------------------------------
    # CLEAR
    # --------------------------------------------------------

    elif key == "c":

        points.clear()

        print(
            "All points cleared."
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