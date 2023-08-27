import cv2, time, base64, os
from datetime import datetime

# Initialize variables
capturing = False
frames_counter = 0
minimum_area = 10000
frames_counter_limit = 30
initial_background = None
folder_path_name = "images"
alert_frames = 25
alert_frames_counter = 0

# Open the camera
camera = cv2.VideoCapture(0)

# Create the image folder if it doesn't exist
if not os.path.exists(folder_path_name):
    os.makedirs(folder_path_name)

# Main loop
while True:
    # Read a frame from the camera
    _, neutral_frame = camera.read()

    # Apply Gaussian blur to the frame
    gaussian_frame = cv2.GaussianBlur(cv2.cvtColor(neutral_frame, cv2.COLOR_BGR2GRAY), (21, 21), 0)

    # If initial background is not set, set it and continue
    if initial_background is None:
        initial_background = gaussian_frame
        continue

    # Calculate the difference between the initial background and the current frame
    difference_frame = cv2.absdiff(initial_background, gaussian_frame)

    # Apply thresholding and dilation to the difference frame
    threshold_frame = cv2.threshold(difference_frame, 50, 255, cv2.THRESH_BINARY)[1]
    threshold_frame = cv2.dilate(threshold_frame, None, iterations=2)

    # Find contours in the threshold frame
    contours, _ = cv2.findContours(threshold_frame.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Process detected contours
    for contour in contours:
        if cv2.contourArea(contour) > minimum_area:
            capturing = True
            (coordinate_x, coordinate_y, width, height) = cv2.boundingRect(contour)
            cv2.rectangle(neutral_frame, (coordinate_x, coordinate_y), (coordinate_x + width, coordinate_y + height), (0, 255, 0), 3)

    # If capturing is enabled
    if capturing:
        if frames_counter == 0 or frames_counter % frames_counter_limit == 0:
            print('Saving image...')
            frames_counter = 0
            alert_frames_counter += 1

            # Encode and save the image
            _, buffer = cv2.imencode('.jpg', neutral_frame)
            with open(os.path.join(folder_path_name, datetime.now().strftime('%H:%M:%S') + ".jpg"), "wb") as file:
                file.write(buffer)

        capturing = False
        frames_counter += 1

    # Check for alerts
    if alert_frames_counter == alert_frames:
        print('Hey, we have a problem here!')

    # Display frames
    cv2.imshow("Threshold Frame", threshold_frame)
    cv2.imshow("Neutral Frame", neutral_frame)

    # Exit loop if 'q' key is pressed
    if cv2.waitKey(1) == ord('q'):
        break

# Release camera and close windows
camera.release()
cv2.destroyAllWindows()
