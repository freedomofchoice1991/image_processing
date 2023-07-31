import time
import os
import logging
import multiprocessing
# OpenCV is a popular open-source computer vision and image
# processing library that provides various
# functions for working with images, videos, and computer vision tasks.
import cv2          # pip install opencv-python


def resize_process(input_image, resized_queue):
    time.sleep(1)
    resized_image = cv2.resize(input_image, (600, 600))  # Resize the image to 100x100
    resized_queue.put(resized_image)

def grayscale_process(resized_queue, grayscale_queue):
    time.sleep(1)
    resized_image = resized_queue.get()
    grayscale_image = cv2.cvtColor(resized_image, cv2.COLOR_BGR2GRAY)
    grayscale_queue.put(grayscale_image)

def edge_detection_process(grayscale_queue, number):
    time.sleep(1)
    grayscale_image = grayscale_queue.get()
    # Use Canny algorithm to detect edges
    edges = cv2.Canny(grayscale_image, 100, 200)
    if len(edges) > 600:  # Example condition to terminate early if too many edges detected
        print("----Terminating edge detection process due to excessive edges.")
        return
    # Further processing with the edges (not implemented in this example)
    print("Edge detection process completed.")
    print(f'Number of edges detected: {len(edges)}')

    # Save the grayscale image in the "result" folder
    result_folder = "result"
    os.makedirs(result_folder, exist_ok=True)
    cv2.imwrite(os.path.join(result_folder, f"grayscale_image_{number}.jpg"), grayscale_image)


if __name__ == "__main__":
    # Load the input images
    input_images = ["images/img1.jpg", "images/img2.jpg", "images/img3.jpg", "images/img4.jpg", "images/img5.jpg"]
    # --------logging section------------
    # log into terminal
    multiprocessing.log_to_stderr()
    # create a logger object
    logger = multiprocessing.get_logger()
    # set logging level
    logger.setLevel(logging.INFO)
    # --------multiprocessing section----------
    for image, number in zip(input_images, range(1, len(input_images) + 1)):
        # Load the input image
        input_image = cv2.imread(image)
        # Create multiprocessing queues for communication between processes
        resized_queue = multiprocessing.Queue()
        grayscale_queue = multiprocessing.Queue()

        # Create processes
        process1 = multiprocessing.Process(target=resize_process, name='resize_process', args=(input_image, resized_queue))
        process2 = multiprocessing.Process(target=grayscale_process, name='grayscale_process', args=(resized_queue, grayscale_queue))
        process3 = multiprocessing.Process(target=edge_detection_process, name='edge_detection_process', args=(grayscale_queue, number))

        # Start the processes
        process1.start()
        process2.start()
        process3.start()

        # Wait for all processes to finish
        process1.join()
        process2.join()
        process3.join()

        print("Image processing pipeline completed.")
