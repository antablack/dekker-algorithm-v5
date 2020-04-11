
import _thread
import sys
import time

class Dekker:
    def __init__(self):
        self.favoured_thread = 1
        self.thread1_wants_to_enter = False
        self.thread2_wants_to_enter = False
        self.completed = False

def thread1(dekker):
    while True:
        dekker.thread1_wants_to_enter = True
        #its critical section
        time.sleep(0.5)
        while dekker.thread2_wants_to_enter:
            if dekker.favoured_thread == 2 :
                dekker.thread1_wants_to_enter = False
                # wait until this thread is favored
                while dekker.favoured_thread == 2:
                    pass
                dekker.thread1_wants_to_enter = True

        #its critical section
        print("Thread1")
        time.sleep(3)
        #favour the 1nd thread
        dekker.favoured_thread = 2
        dekker.thread1_wants_to_enter = False
        if dekker.completed:
            print("thread 1 killed")
            break

def thread2(dekker):
    while True:
        dekker.thread2_wants_to_enter = True
        #its critical section
        time.sleep(0.5)
        while dekker.thread1_wants_to_enter:
            if dekker.favoured_thread == 1 :
                dekker.thread2_wants_to_enter = False
                while dekker.favoured_thread == 1:
                    pass
                dekker.thread2_wants_to_enter = True

        print("Thread2")
        #its critical section
        time.sleep(1)
        #favour the 1st thread
        dekker.favoured_thread = 1
        dekker.thread2_wants_to_enter = False
        if dekker.completed:
            print("thread 2 killed")
            break


def startThreads(dekker):
    try:
        _thread.start_new_thread( thread1, (dekker, ))
        _thread.start_new_thread( thread2, (dekker, ))
    except:
        print("Error: unable to start threads", sys.exc_info()[0])


if __name__ == "__main__" :
    dekker = Dekker()
    startThreads(dekker)
    print("killing threads")
    dekker.completed = True
    print(f'favoured_thread {dekker.favoured_thread}')
    print(f'thread1_wants_to_enter {dekker.thread1_wants_to_enter}')
    print(f'thread2_wants_to_enter {dekker.thread2_wants_to_enter}')
    while True:
        pass
    


#https://github.com/guicassolato/dekker
#https://www.geeksforgeeks.org/dekkers-algorithm-in-process-synchronization
#https://www.tutorialspoint.com/dekker-s-algorithm-in-operating-system