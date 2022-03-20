import cv2
import time

from src import MainProcess
from src.utils.camera import Camera
# from src.utils import Adam6050Input

from src.utils import logging


class RunApplication:
	def __init__(self):		
		self.camera      	= Camera(camera_id='18.avi', camera_pipeline=False)
		self.camera_run  	= self.camera.run()
		self.app         	= MainProcess()
		self.skip_frame  	= True
		#self.out		= self.__write_video('demo_video_4')

	
	def __write_video(self, filename):
		size = (int(self.camera_run.get(3)), int(self.camera_run.get(4)))
		return cv2.VideoWriter(f'{filename}.avi',cv2.VideoWriter_fourcc(*'XVID'), 10, size)

	def run(self):
		start_time 	= time.time()
		timestamp	= int(start_time)
  
		logging.info(f'======== Damage Detection Started ========')
		logging.info(f'Id : {timestamp}')

		# frame = cv2.imread('files/test_image.jpg')

		# # Process detection seal
		out = self.__write_video('3')

		while True:
			ret, frame = self.camera_run.read()
			if not ret:
				logging.error(f'Message : Error reading frame')
				self.camera.release(ret=False)
				self.capture = self.camera.run()
				time.sleep(1)
			else:
				if not self.skip_frame:
					drawed = self.app.main(image=frame, id=timestamp)
					out.write(drawed)
					self.skip_frame = True
				else: self.skip_frame = False; continue
			
				key_window = self.camera.show(drawed)
				if key_window == 27: break

		out.release()
		self.camera.release()

if __name__ == '__main__':
	aplication  = RunApplication()
	aplication.run()
