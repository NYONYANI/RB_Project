import pyrealsense2 as rs
import numpy as np
import cv2

class RealSenseCamera:
    def __init__(self):
        # Create a pipeline
        self.pipeline = rs.pipeline()

        # Configure the pipeline
        self.config = rs.config()
        self.config.enable_stream(rs.stream.color, 640, 480, rs.format.rgb8, 30)
        self.config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
        cv2.namedWindow('Depth Image')
        cv2.setMouseCallback('Depth Image', self.mouse_event)

        # Start the pipeline
        self.pipeline.start(self.config)
    def mouse_event(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            depth = self.depth_frame.get_distance(x, y)
            print(f"Depth at ({x}, {y}): {depth} meters")

    def run(self):
        try:
            while True:
                # Wait for the next frame
                frames = self.pipeline.wait_for_frames()

                # Get the color and depth frames
                color_frame = frames.get_color_frame()
                depth_frame = frames.get_depth_frame()

                if not color_frame or not depth_frame:
                    continue

                # Convert frames to numpy arrays
                color_image = np.asanyarray(color_frame.get_data())
                depth_image = np.asanyarray(depth_frame.get_data())

                # Get the depth frame
                self.depth_frame = frames.get_depth_frame()

                # Convert RGB to BGR
                color_image = cv2.cvtColor(color_image, cv2.COLOR_RGB2BGR)

                # Apply colormap on depth image (image must be converted to 8-bit per pixel first)
                depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.03), cv2.COLORMAP_JET)

                # Display the images
                cv2.imshow('Color Image', color_image)
                cv2.imshow('Depth Image', depth_colormap)

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

        finally:
            self.stop()

    def stop(self):
        # Stop the pipeline
        self.pipeline.stop()

        # Close all windows
        cv2.destroyAllWindows()
if __name__ == "__main__":
    camera = RealSenseCamera()
    camera.run()
