import math

import cv2
import numpy as np


DEBUG = True

def get_rgb(event,x,y,flags,param):
    if event == cv2.EVENT_MOUSEMOVE:
        rgb = frame[y,x]
        print("RGB value at (",x,",",y,"): ", rgb)


red_lower = np.array([0, 0, 120])
red_upper = np.array([80, 60, 255])

green_lower = np.array([0, 110, 0])
green_upper = np.array([120, 255, 60])

blue_lower = np.array([115, 0, 0])
blue_upper = np.array([255, 90, 60])


#
# def update_green_lower_r(rval):
#     global green_lower
#     green_lower[2] = rval
#
# def update_green_lower_g(gval):
#     global green_lower
#     green_lower[1] = gval
#
# def update_green_lower_b(bval):
#     global green_lower
#     green_lower[0] = bval
#
# def update_green_upper_r(rval):
#     global green_upper
#     green_upper[2] = rval
#
# def update_green_upper_g(gval):
#     global green_upper
#     green_upper[1] = gval
#
# def update_green_upper_b(bval):
#     global green_upper
#     green_upper[0] = bval
#
#
#
# def update_blue_lower_r(rval):
#     global blue_lower
#     blue_lower[2] = rval
#
# def update_blue_lower_g(gval):
#     global blue_lower
#     blue_lower[1] = gval
#
# def update_blue_lower_b(bval):
#     global blue_lower
#     blue_lower[0] = bval
#
# def update_blue_upper_r(rval):
#     global blue_upper
#     blue_upper[2] = rval
#
# def update_blue_upper_g(gval):
#     global blue_upper
#     blue_upper[1] = gval
#
# def update_blue_upper_b(bval):
#     global blue_upper
#     blue_upper[0] = bval

# Define the initial RGB color ranges for red, green, and blue

# Open the default camera
cap = cv2.VideoCapture(0)

# Create a window to display the sliders
# cv2.namedWindow('sliders')
#
# # Create the sliders
# cv2.createTrackbar('Red Lower R', 'sliders', 0, 255, update_red_lower_r)
# cv2.createTrackbar('Red Lower G', 'sliders', 0, 255, update_red_lower_g)
# cv2.createTrackbar('Red Lower B', 'sliders', 0, 255, update_red_lower_b)
# cv2.createTrackbar('Red Upper R', 'sliders', 0, 255, update_red_upper_r)
# cv2.createTrackbar('Red Upper G', 'sliders', 0, 255, update_red_upper_g)
# cv2.createTrackbar('Red Upper B', 'sliders', 0, 255, update_red_upper_b)
#
#
#
# cv2.createTrackbar('Green Lower R', 'sliders', 0, 255, update_green_lower_r)
# cv2.createTrackbar('Green Lower G', 'sliders', 0, 255, update_green_lower_g)
# cv2.createTrackbar('Green Lower B', 'sliders', 0, 255, update_green_lower_b)
# cv2.createTrackbar('Green Upper R', 'sliders', 0, 255, update_green_upper_r)
# cv2.createTrackbar('Green Upper G', 'sliders', 0, 255, update_green_upper_g)
# cv2.createTrackbar('Green Upper B', 'sliders', 0, 255, update_green_upper_b)
#
#
#
# cv2.createTrackbar('Blue Lower R', 'sliders', 0, 255, update_blue_lower_r)
# cv2.createTrackbar('Blue Lower G', 'sliders', 0, 255, update_blue_lower_g)
# cv2.createTrackbar('Blue Lower B', 'sliders', 0, 255, update_blue_lower_b)
# cv2.createTrackbar('Blue Upper R', 'sliders', 0, 255, update_blue_upper_r)
# cv2.createTrackbar('Blue Upper G', 'sliders', 0, 255, update_blue_upper_g)
# cv2.createTrackbar('Blue Upper B', 'sliders', 0, 255, update_blue_upper_b)

def find_pens(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    _, s, _ = cv2.split(hsv)

    thresh_value = 185
    max_value = 255
    _, binary_img = cv2.threshold(s, thresh_value, max_value, cv2.THRESH_BINARY)

    contours, _ = cv2.findContours(binary_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)

    return contours


def extract_roi_from_contour(contour):
    x, y, w, h = cv2.boundingRect(contour)

    roi = frame[y:y + h, x:x + w]

    return roi, x, y


def get_colored_contours_based_on_roi(roi):
    red_mask = cv2.inRange(roi, red_lower, red_upper)
    green_mask = cv2.inRange(roi, green_lower, green_upper)
    blue_mask = cv2.inRange(roi, blue_lower, blue_upper)

    red_contours, _ = cv2.findContours(red_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    green_contours, _ = cv2.findContours(green_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    blue_contours, _ = cv2.findContours(blue_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    return red_contours, green_contours, blue_contours


def accumulate_contours(contours, dest, x, y):
    if contours:
        for i in range(len(contours)):
            for k in range(len(contours[i])):
                contours[i][k][0][0] += x
                contours[i][k][0][1] += y

        dest += contours

    return dest


def find_pen_tips(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    _, _, v = cv2.split(hsv)

    thresh_value = 215
    max_value = 255
    _, binary_img = cv2.threshold(v, thresh_value, max_value, cv2.THRESH_BINARY)

    white_contours, _ = cv2.findContours(binary_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    return white_contours


def combine_contours(contours):
    rcontours = []
    gcontours = []
    bcontours = []

    for i, c in enumerate(contours):
        roi, x, y = extract_roi_from_contour(c)
        red_contours, green_contours, blue_contours = get_colored_contours_based_on_roi(roi)

        rcontours = accumulate_contours(red_contours, rcontours, x, y)
        gcontours = accumulate_contours(green_contours, gcontours, x, y)
        bcontours = accumulate_contours(blue_contours, bcontours, x, y)

    combined_r_contour = None
    combined_g_contour = None
    combined_b_contour = None

    if rcontours:
        combined_r_contour = np.vstack(rcontours)

    if gcontours:
        combined_g_contour = np.vstack(gcontours)

    if bcontours:
        combined_b_contour = np.vstack(bcontours)

    return combined_r_contour, combined_g_contour, combined_b_contour


def draw(contour, color):
    rect = cv2.minAreaRect(contour)
    box = cv2.boxPoints(rect)
    box = np.int0(box)
    cv2.drawContours(frame, [box], -1, color, 2)


# def associate_pen_tip(tips, pen_contour, ignored):
#     distance = math.inf
#     idx = 9999
#     for i, wc in enumerate(tips):
#         if i in ignored:
#             continue
#
#         rect = cv2.minAreaRect(wc)
#         wbox = cv2.boxPoints(rect)
#         wbox = np.int0(wbox)
#
#         if pen_contour is not None and pen_contour.any():
#             rect = cv2.minAreaRect(pen_contour)
#             box = cv2.boxPoints(rect)
#             box = np.int0(box)
#
#             distances = []
#             for p1 in wbox:
#                 for p2 in box:
#                     dist = np.linalg.norm(p1 - p2)
#                     distances.append(dist)
#
#             if min(distances) < distance:
#                 distance = min(distances)
#                 idx = i
#     return idx


def associate_pens_tips(tips, r, g, b):
    pens = {0: 9999, 1: 9999, 2: 9999}

    for k, pen_contour in enumerate([r, g, b]):
        distance = math.inf
        idx = 9999
        cidx = 9999
        for i, wc in enumerate(tips):
            rect = cv2.minAreaRect(wc)
            wbox = cv2.boxPoints(rect)
            wbox = np.int0(wbox)

            if pen_contour is not None and pen_contour.any():
                rect = cv2.minAreaRect(pen_contour)
                box = cv2.boxPoints(rect)
                box = np.int0(box)

                distances = []
                for p1 in wbox:
                    for p2 in box:
                        dist = np.linalg.norm(p1 - p2)
                        distances.append(dist)

                if min(distances) < distance and min(distances) < 6:
                    distance = min(distances)
                    idx = i
                    cidx = k

        pens[cidx] = idx

    if 9999 in pens:
        del pens[9999]
    return pens[0], pens[1], pens[2]


def get_pen_tip_association_line(pen_contour, tip_contour):
    rect = cv2.minAreaRect(tip_contour)
    wbox = cv2.boxPoints(rect)
    wbox = np.int0(wbox)

    rect = cv2.minAreaRect(pen_contour)
    box = cv2.boxPoints(rect)
    box = np.int0(box)

    pen_box_center = tuple(np.mean(box, axis=0).astype(int))
    associated_white_box_center = tuple(np.mean(wbox, axis=0).astype(int))

    return pen_box_center, associated_white_box_center


def draw_pen_tip_association(pen_contour, tip_contour):
    pen_box_center, associated_white_box_center = get_pen_tip_association_line(pen_contour, tip_contour)
    cv2.line(frame, pen_box_center, associated_white_box_center, (0, 255, 255), 2)


def draw_pen_tip_associations(r, g, b, tips, wc_i_r, wc_i_g, wc_i_b):
    if r is not None and r.any() and tips_contours and len(tips) > wc_i_r and wc_i_r != 9999:
        draw_pen_tip_association(r, tips[wc_i_r])

    if g is not None and g.any() and tips_contours and len(tips) > wc_i_g and wc_i_g != 9999:
        draw_pen_tip_association(g, tips[wc_i_g])

    if b is not None and b.any() and tips_contours and len(tips) > wc_i_b and wc_i_b != 9999:
        draw_pen_tip_association(b, tips[wc_i_b])


def draw_combined(r, g, b):
    if r is not None and r.any():
        draw(r, (0, 0, 255))

    if g is not None and g.any():
        draw(g, (0, 255, 0))

    if b is not None and b.any():
        draw(b, (255, 0, 0))


def determine_approx_lines_of_pens(r, g, b, tips_contours, wc_i_r, wc_i_g, wc_i_b):
    pens = {}
    if r is not None and r.any() and tips_contours and len(tips_contours) > wc_i_r and wc_i_r != 9999:
        red_pen_box_center, red_pen_tip_center = get_pen_tip_association_line(r, tips_contours[wc_i_r])
        pens["r"] = {"pen": red_pen_box_center, "tip": red_pen_tip_center}

    if g is not None and g.any() and tips_contours and len(tips_contours) > wc_i_g and wc_i_g != 9999:
        green_pen_box_center, green_pen_tip_center = get_pen_tip_association_line(g, tips_contours[wc_i_g])
        pens["g"] = {"pen": green_pen_box_center, "tip": green_pen_tip_center}

    if b is not None and b.any() and tips_contours and len(tips_contours) > wc_i_b and wc_i_b != 9999:
        blue_pen_box_center, blue_pen_tip_center = get_pen_tip_association_line(b, tips_contours[wc_i_b])
        pens["b"] = {"pen": blue_pen_box_center, "tip": blue_pen_tip_center}

    return pens


while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    contours = find_pens(frame)
    tips_contours = find_pen_tips(frame)

    combined_r_contour, combined_g_contour, combined_b_contour = combine_contours(contours)

    if DEBUG:
        draw_combined(combined_r_contour, combined_g_contour, combined_b_contour)
        for wc in tips_contours:
            draw(wc, (255, 255, 255))

    wc_i_r, wc_i_g, wc_i_b = associate_pens_tips(tips_contours, combined_r_contour, combined_g_contour, combined_b_contour)

    if DEBUG:
        draw_pen_tip_associations(combined_r_contour, combined_g_contour, combined_b_contour, tips_contours, wc_i_r, wc_i_g, wc_i_b)

    pens = determine_approx_lines_of_pens(combined_r_contour, combined_g_contour, combined_b_contour, tips_contours, wc_i_r, wc_i_g, wc_i_b)

    print(pens)

    cv2.imshow('frame', frame)

    # Exit the loop when the 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the capture and close all windows
cap.release()
cv2.destroyAllWindows()