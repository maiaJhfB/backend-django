import argparse
import cv2
import os
import numpy as np
from tattoo_augmenter import TattooAugmenter

def create_dummy_tattoo(path):
    """Creates a simple dummy tattoo image if it doesn't exist."""
    if not os.path.exists(path):
        try:
            dummy_tattoo = np.zeros((100, 150, 4), dtype=np.uint8) # Rectangular shape
            cv2.putText(dummy_tattoo, 'PYTHON', (5, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255, 255), 2, cv2.LINE_AA)
            cv2.line(dummy_tattoo, (0,0), (149,99), (255, 0, 0, 150), 3)
            cv2.line(dummy_tattoo, (0,99), (149,0), (0, 0, 255, 150), 3)
            cv2.imwrite(path, dummy_tattoo)
            print(f"Created dummy tattoo image: {path}")
            return True
        except Exception as e:
            print(f"Error creating dummy tattoo: {e}")
            return False
    return True

def main():
    parser = argparse.ArgumentParser(description='Apply virtual tattoos using MediaPipe Pose.')
    parser.add_argument('--mode', type=str, default='webcam', choices=['webcam', 'image'],
                        help='Execution mode: webcam or image.')
    parser.add_argument('--input', type=str, default=None,
                        help='Path to the input image file (required for image mode).')
    parser.add_argument('--output', type=str, default='/home/ubuntu/output_tattooed_image.jpg',
                        help='Path to save the output image (for image mode).')
    parser.add_argument('--tattoo', type=str, default='/home/ubuntu/dummy_tattoo.png',
                        help='Path to the tattoo image (PNG with alpha recommended). A dummy tattoo will be created if not found.')
    parser.add_argument('--part', type=str, default='forearm',
                        help='Target body part (currently only "forearm" is implemented).')
    parser.add_argument('--rotate', type=float, default=0.0,
                        help='Rotation angle for the tattoo image in degrees.')
    parser.add_argument('--smooth', type=int, default=3,
                        help='Smoothing window size (frames) for temporal stability.')
    parser.add_argument('--blur', type=int, default=7,
                        help='Kernel size for blurring tattoo edges (odd number).')
    parser.add_argument('--bg_thresh', type=int, default=10,
                        help='Threshold for removing white background (0-255).')

    args = parser.parse_args()

    # Ensure dummy tattoo exists if the specified one is not found
    if not os.path.exists(args.tattoo):
        print(f"Tattoo image not found at {args.tattoo}. Attempting to create a dummy tattoo.")
        if not create_dummy_tattoo('/home/ubuntu/dummy_tattoo.png'):
             print("Failed to create or find a tattoo image. Exiting.")
             return
        args.tattoo = '/home/ubuntu/dummy_tattoo.png'
    # No need for the second check if the first one already defaults to the dummy path
    # elif not create_dummy_tattoo('/home/ubuntu/dummy_tattoo.png'):
    #     print("Failed to create or find a tattoo image. Exiting.")
    #     return

    try:
        # Pass all relevant arguments to the augmenter
        augmenter = TattooAugmenter(
            tattoo_image_path=args.tattoo,
            target_body_part=args.part,
            bg_color_threshold=args.bg_thresh,
            smoothing_window=args.smooth,
            blur_kernel_size=args.blur,
            rotation_angle=args.rotate
            # use_gpu=args.use_gpu # If GPU flag is added later
        )

        if args.mode == 'webcam':
            print("Starting webcam mode...")
            augmenter.run_on_webcam()
        elif args.mode == 'image':
            if args.input is None:
                print("Error: Input image path (--input) is required for image mode.")
            else:
                print(f"Starting image mode for {args.input}...")
                augmenter.run_on_image(args.input, args.output)
        else:
            print(f"Error: Unknown mode '{args.mode}'")

        augmenter.close()

    except FileNotFoundError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        import traceback
        traceback.print_exc() # Print detailed traceback for debugging

if __name__ == '__main__':
    main()

