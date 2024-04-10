import cv2

# Open the video file
cap = cv2.VideoCapture(r'C:\Users\Admin\climb_6.mp4')

# Get the frames per second (fps) of the video
fps = cap.get(cv2.CAP_PROP_FPS)

# Get the total number of frames in the video
total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

# Loop through each frame in the video
for i in range(total_frames):

    # Read the frame
    ret, frame = cap.read()

    # Save the frame as an image file
    cv2.imwrite(f'climb\climb_frame_{i+400+1600+400+300+260+550}.jpg', frame)

    # Print the progress
    print(f'Processed frame {i}/{total_frames}')

    # Wait for the next frame
    cv2.waitKey(int(1000 / fps))

# Release the video file
cap.release()

