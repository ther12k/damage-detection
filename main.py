import cv2
import time

from src import MainProcess
from src.utils.camera import Camera
from src.utils import Adam6050Input

from src.utils import logging, datetime_format
from config import DEVICE_ID, GATE_ID, TIMEID_FORMAT,FTP_HOST, USER_NAME, USER_PASSWD
import ftplib
from datetime import datetime
import os

class RunApplication:
	def __init__(self):		
		self.camera      	= Camera(camera_id=0, flip_method=2, camera_pipeline=False)
		self.camera_run  	= self.camera.run()
		self.adam_input		= Adam6050Input()
		self.app         	= MainProcess()
		self.prev_input		= list()
		self.skip_frame  	= False
		self.count_frame 	= 0

	#prefer to move to another file	
	def chdir(self,ftp_path, ftp_conn):
		dirs = [d for d in ftp_path.split('/') if d != '']
		for p in dirs:
			self.check_dir(p, ftp_conn)

	#prefer to move to another file
	def check_dir(dir, ftp_conn):
		filelist = []
		ftp_conn.retrlines('LIST', filelist.append)
		found = False
		for f in filelist:
			if f.split()[-1] == dir and f.lower().startswith('d'):
				found = True

		if not found:
			ftp_conn.mkd(dir)
		ftp_conn.cwd(dir)

	def video_upload(self,file_name):
		try:
			year, month, day, hour, _, _,_ = datetime_format()
			dest_path = f'/{GATE_ID}/{year}/{month}/{day}/'
			"""Transfer file to FTP."""
			# Connect
			session = ftplib.FTP(FTP_HOST, USER_NAME, USER_PASSWD)

			# Change to target dir
			self.chdir(dest_path,session)

			# Transfer file
			logging.info("Transferring %s to %s..." % (file_name,dest_path))
			with open(file_name, "rb") as file:
				session.storbinary('STOR %s' % os.path.basename(dest_path+DEVICE_ID+file_name), file)
			
			# Close session
			session.quit()
			return dest_path+file_name
		except:
			logging.info('error: upload file error')
			return 'error: upload file error'

	def __write_video(self, filename):
		size = (int(self.camera_run.get(3)), int(self.camera_run.get(4)))
		return cv2.VideoWriter(f'{filename}.avi',cv2.VideoWriter_fourcc(*'XVID'), 10, size)

	def __trigger_camera(self):
		input_list = self.adam_input.di_inputs()
		if not self.prev_input == input_list:
			if not self.prev_input[4] and input_list:
				trigger = True
			self.prev_input = input_list
		else: trigger = True
		return trigger
		 
	def run(self):
		
		start_time 	= time.time()
		timestamp	= int(start_time)
  
		logging.info(f'======== Damage Detection Started ========')
		logging.info(f'Id : {timestamp}')

		# Define Write Video
		time_id = datetime.now()
		name = time_id.strftime(TIMEID_FORMAT)[:-4]
		out_video =  self.__write_video(name)
		
		while True:
			#if self.__trigger_camera():
			ret, frame = self.camera_run.read()
			if not ret:
				logging.error(f'Message : Error reading frame')
				self.camera.release(ret=False)
				self.capture = self.camera.run()
				time.sleep(1)
			else:
				if not self.skip_frame:
					if self.count_frame == 2:
						print(cv2.imwrite('test.jpg', frame));break
					else: self.count_frame+=1
					file_path = self.video_upload(name+'.avi')
					if 'error' in file_path :
						file_path=''
					drawed = self.app.main(frame,time_id,file_path)
						#out_video.write(drawed)
					self.skip_frame = True
				else: self.skip_frame = False; continue
			
				key_window = self.camera.show(drawed)
				if key_window == 27: break

		self.out.release()
		self.camera.release()

if __name__ == '__main__':
	aplication  = RunApplication()
	aplication.run()
