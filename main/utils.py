import cv2
import os

def convert_video_to_ar(video_path):
    # Define the output directory for AR content
    ar_content_dir = 'ar_content'
    os.makedirs(ar_content_dir, exist_ok=True)

    # Open the video file
    cap = cv2.VideoCapture(video_path)

    # Get video properties
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # Define AR effects (Example: adding a watermark)
    watermark = cv2.imread('watermark.png', cv2.IMREAD_UNCHANGED)

    # Define the codec and create VideoWriter object
    output_path = os.path.join(ar_content_dir, os.path.basename(video_path) + '_ar.mp4')
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    # Process each frame of the video
    while(cap.isOpened()):
        ret, frame = cap.read()
        if ret == True:
            # Apply AR effects (Example: adding a watermark)
            # Adjust the position and transparency of the watermark as needed
            overlay = cv2.resize(watermark, (width // 4, height // 4))
            x_offset = 20
            y_offset = height - overlay.shape[0] - 20
            alpha_s = overlay[:, :, 3] / 255.0
            alpha_l = 1.0 - alpha_s
            for c in range(0, 3):
                frame[y_offset:y_offset+overlay.shape[0], x_offset:x_offset+overlay.shape[1], c] = (
                    alpha_s * overlay[:, :, c] + alpha_l * frame[y_offset:y_offset+overlay.shape[0], x_offset:x_offset+overlay.shape[1], c])

            # Write the frame to the output video
            out.write(frame)
        else:
            break

    # Release everything when done
    cap.release()
    out.release()
    cv2.destroyAllWindows()

    return output_path
