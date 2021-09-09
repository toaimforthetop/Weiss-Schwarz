from threading import Thread

def threading(cmd):
	thread = Thread(target=cmd)
	thread.daemon = True
	thread.start()