import video
import defines
from multiprocessing import Process, Queue, Lock
import time
import pyautogui
import pyudev
import cv2
import numpy as np
import os

def find_all_usb_webcam_paths():
    context = pyudev.Context()
    webcam_paths = []

    for device in context.list_devices(subsystem='video4linux'):
        # USB 웹캠 장치를 찾음
        if device.sys_name.startswith("video"):
            webcam_paths.append(device.device_node)

    return webcam_paths

def CheckCamPort():
    camnum = 0
    cap = []
    for i in range(3):
        cap.append(cv2.VideoCapture(i))
        if cap[i].isOpened():
            print("Opened Cam Port is : " + f"{i}")
            camnum = camnum + 1
            cap[i].release()
    return camnum

def recorder1(q,ctl,l):
    status = 0
    WIDTH = 1280
    HEIGHT = 720

    while ctl.empty():
        l.acquire()
        if status == 0:
            try:
                webcam_paths = find_all_usb_webcam_paths()
                print(webcam_paths)
                cap = cv2.VideoCapture(webcam_paths[0])
                # cap = cv2.VideoCapture(0)
                if cap.isOpened() is not True:
                    print("init camera fail 11")
                    q.put(np.zeros((HEIGHT,WIDTH,3), dtype=np.uint8))
                    continue

            except:
                print("init camera fail 12")
                q.put(np.zeros((HEIGHT,WIDTH,3), dtype=np.uint8))
            else:
                cap.set(cv2.CAP_PROP_FPS, 30)
                FPS = cap.get(cv2.CAP_PROP_FPS)
                print(FPS)
                if FPS != 0:
                    cap.set(3, WIDTH)
                    cap.set(4, HEIGHT)
                    cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M','J','P','G'))
                    status = 1

        elif status == 1:
            try:
                ret, f = cap.read()
            except:
                q.put(np.zeros((HEIGHT,WIDTH,3), dtype=np.uint8))
            else:
                if ret:
                    q.put(f)
                else:
                    q.put(np.zeros((HEIGHT,WIDTH,3), dtype=np.uint8))
                    print("cap read fail 1")
                    status = 0
                    cap.release()

    print("stop recording")
    cap.release()

def recorder2(q,ctl,l):
    status = 0
    WIDTH = 1280
    HEIGHT = 720

    while ctl.empty():
        l.acquire()
        if status == 0:
            try:
                webcam_paths = find_all_usb_webcam_paths()
                print(webcam_paths)
                cap = cv2.VideoCapture(webcam_paths[2])
                # cap = cv2.VideoCapture(1)
                if cap.isOpened() is not True:
                    print("init camera fail 21")
                    q.put(np.zeros((HEIGHT,WIDTH,3), dtype=np.uint8))
                    continue

            except:
                print("init camera fail 22")
                q.put(np.zeros((HEIGHT,WIDTH,3), dtype=np.uint8))
            else:
                cap.set(cv2.CAP_PROP_FPS, 30)
                FPS = cap.get(cv2.CAP_PROP_FPS)
                print(FPS)
                if FPS != 0:
                    cap.set(3, WIDTH)
                    cap.set(4, HEIGHT)
                    cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M','J','P','G'))
                    status = 1

        elif status == 1:
            try:
                ret, f = cap.read()
            except:
                q.put(np.zeros((HEIGHT,WIDTH,3), dtype=np.uint8))
            else:
                if ret:
                    q.put(f)
                else:
                    q.put(np.zeros((HEIGHT,WIDTH,3), dtype=np.uint8))
                    print("cap read fail 2")
                    status = 0
                    cap.release()

    print("stop recording")
    cap.release()
    
def recorder3(q,ctl,l):
    status = 0
    WIDTH = 1280
    HEIGHT = 720

    while ctl.empty():
        l.acquire()
        if status == 0:
            try:
                webcam_paths = find_all_usb_webcam_paths()
                print(webcam_paths)
                cap = cv2.VideoCapture(webcam_paths[4])
                # cap = cv2.VideoCapture(2)
                if cap.isOpened() is not True:
                    print("init camera fail 31")
                    q.put(np.zeros((HEIGHT,WIDTH,3), dtype=np.uint8))
                    continue

            except:
                print("init camera fail 32")
                q.put(np.zeros((HEIGHT,WIDTH,3), dtype=np.uint8))
            else:
                cap.set(cv2.CAP_PROP_FPS, 30)
                FPS = cap.get(cv2.CAP_PROP_FPS)
                print(FPS)
                if FPS != 0:
                    cap.set(3, WIDTH)
                    cap.set(4, HEIGHT)
                    cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M','J','P','G'))
                    status = 1

        elif status == 1:
            try:
                ret, f = cap.read()
            except:
                q.put(np.zeros((HEIGHT,WIDTH,3), dtype=np.uint8))
            else:
                if ret:
                    q.put(f)
                else:
                    q.put(np.zeros((HEIGHT,WIDTH,3), dtype=np.uint8))
                    print("cap read fail 3")
                    status = 0
                    cap.release()

    print("stop recording")
    cap.release()

if __name__ == '__main__':
    width, height = pyautogui.size()
    pyautogui.FAILSAFE = False  
    pyautogui.moveTo(width, height)     
    pyautogui.FAILSAFE = True 
    print(f"Monitor pixel : ({width}x{height})")
    camnum = CheckCamPort()
    print(f"{camnum}-Camera System")

    v = video.opencv()
    mode = defines.MODE()

    frame_queue1 = Queue()
    control_queue1 = Queue()
    lock1 = Lock()
    record_process1 = Process(target=recorder1, args=(frame_queue1,control_queue1,lock1,)) 

    frame_queue2 = Queue()
    control_queue2 = Queue()
    lock2 = Lock()
    record_process2 = Process(target=recorder2, args=(frame_queue2,control_queue2,lock2,))

    frame_queue3 = Queue()
    control_queue3 = Queue()
    lock3 = Lock()
    record_process3 = Process(target=recorder3, args=(frame_queue3,control_queue3,lock3,))
    
    BUFFER = []
    FPS = 30
    end_point = FPS * 180
    play_point = 0
    delay_point = 0
    slow_level = 1
    slow_cnt = 0

    state = mode.IDLE

    w = int(width)
    h = int(height)

    record_process1.start()   
    record_process2.start()    
    record_process3.start()

    while True:
        frame1 = frame_queue1.get() 
        frame2 = frame_queue2.get()
        frame3 = frame_queue3.get()

        lock1.release()
        lock2.release()
        lock3.release()

        head_w = 1080
        head_h = 610
        f1 = cv2.resize(frame1, (head_w, head_h))
        f1 = cv2.transpose(f1)
        f1 = cv2.flip(f1, 0)
        
        body_w = 1080
        body_h = 610
        f2 = cv2.resize(frame2, (body_w, body_h))
        f2 = cv2.transpose(f2)
        f2 = cv2.flip(f2, 0)
        
        extra_w = 1080
        extra_h = 700
        f3 = cv2.resize(frame3, (extra_w, extra_h))
        f3 = f3[0:700, 135:945]
        frame_img = np.zeros((700, 270, 3), dtype=np.uint8)
        f3 = np.hstack((f3, frame_img))
        f3 = cv2.transpose(f3)
        f3 = cv2.flip(f3, 0)

        frame = np.hstack((f1, f2))
        frame = np.hstack((frame, f3))

        if state == mode.IDLE:
            msg = f'{play_point / FPS:3.1f}s'
            v.playFrame(frame, msg)
        elif state == mode.PLAY:
            length = len(BUFFER)
            if length >= (end_point + delay_point):
                del BUFFER[0]
            BUFFER.append(frame)

            if delay_point >= length:
                play_point = 0
                countdown = int((delay_point - length - 1) / FPS) + 1
            else:
                play_point = length - delay_point - 1
                countdown = 0
            
            msg = f'{(play_point / FPS):3.1f}s'
            if countdown != 0:
                msg2 = f'{countdown:5d}'
            else:
                msg2 = ""
            v.playFrame(BUFFER[play_point], msg, msg2, state, 1, 1)
        elif state == mode.REPLAY:
            if slow_cnt % slow_level == 0:
                if play_point < (len(BUFFER) - 1):
                    play_point = play_point + 1
                else:
                    state = mode.STOP
                
                msg = f'{play_point / FPS:3.1f}s'
                msg2 = ""
                v.playFrame(BUFFER[play_point], msg, msg2, state, slow_level, 2)
            slow_cnt = slow_cnt + 1
        elif state == mode.STOP:
            status = 3
            if key & 0xff == ord('d'):
                status = 4
            elif key & 0xff == ord('a'):
                status = 5
            msg = f'{play_point / FPS:3.1f}s'
            msg2 = ""
            v.playFrame(BUFFER[play_point], msg, msg2, state, slow_level, status)
            status = 3

        # cv2.namedWindow('frame1', cv2.WINDOW_FULLSCREEN)
        # cv2.setWindowProperty('frame1', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
        # cv2.imshow('frame1', f1)
        # cv2.imshow('frame2', f2)
        # cv2.imshow('frame3', f3)
        # cv2.imshow('frame', frame)

        key = cv2.waitKey(1)
        if key & 0xff == ord('s'):
            if state == mode.STOP or state == mode.REPLAY:
                slow_level = slow_level * 2
                if slow_level > 8:
                    slow_level = 1
        elif key & 0xff == ord('d'):
            if state != mode.IDLE:
                state = mode.STOP
                if play_point <= (len(BUFFER) - 15):
                    play_point = play_point + 15
        elif key & 0xff == ord('p'):
            if state == mode.PLAY:
                state = mode.STOP
            elif state == mode.REPLAY:
                state = mode.STOP
            elif state == mode.STOP:
                state = mode.REPLAY
        elif key & 0xff == ord('a'):
            if state != mode.IDLE:
                state = mode.STOP
                if play_point >= 15:
                    play_point = play_point - 15
        elif key & 0xff == ord('r'):
            if state == mode.IDLE:
                state = mode.PLAY
            else:
                state = mode.IDLE
            play_point = 0
            slow_level = 1
            BUFFER.clear()
        elif key & 0xff == ord('0'):
            state = mode.IDLE
            delay_point = FPS * 0
            play_point = 0
            slow_level = 1
            BUFFER.clear()
        elif key & 0xff == ord('1'):  
            state = mode.IDLE   
            delay_point = FPS * 1
            play_point = 0
            slow_level = 1
            BUFFER.clear()
        elif key & 0xff == ord('2'):
            state = mode.IDLE
            delay_point = FPS * 2
            play_point = 0
            slow_level = 1
            BUFFER.clear()
        elif key & 0xff == ord('3'):
            state = mode.IDLE
            delay_point = FPS * 3
            play_point = 0
            slow_level = 1
            BUFFER.clear()
        elif key & 0xff == ord('4'):
            state = mode.IDLE
            delay_point = FPS * 4
            play_point = 0
            slow_level = 1
            BUFFER.clear()
        elif key & 0xff == ord('5'):
            state = mode.IDLE
            delay_point = FPS * 5
            play_point = 0
            slow_level = 1
            BUFFER.clear()
        elif key & 0xff == ord('6'):
            state = mode.IDLE
            delay_point = FPS * 6
            play_point = 0
            slow_level = 1
            BUFFER.clear()
        elif key & 0xff == ord('7'):
            state = mode.IDLE
            delay_point = FPS * 7
            play_point = 0
            slow_level = 1
            BUFFER.clear()
        elif key & 0xff == ord('8'):
            state = mode.IDLE
            delay_point = FPS * 8
            play_point = 0
            slow_level = 1
            BUFFER.clear()
        elif key & 0xff == ord('9'):
            state = mode.IDLE
            delay_point = FPS * 9
            play_point = 0
            slow_level = 1
            BUFFER.clear()
        if key & 0xff == ord('q'):
            control_queue1.put(key)
            control_queue2.put(key)
            control_queue3.put(key)
            break
    
    time.sleep(1)
    record_process1.terminate()
    record_process1.join()
    record_process2.terminate()
    record_process2.join()
    record_process3.terminate()
    record_process3.join()

    cv2.destroyAllWindows()

    os.system("shutdown -h now")
