import speech_recognition as sr
import time
import json

class Speech_Sphinx(object):
    def recognize(self):
        r = sr.Recognizer()
        energy_threshold = -1
        # request spoken input
        with sr.Microphone(sample_rate=48000, chunk_size=1024) as source:
            # if this is the first time then we want to calibrate for ambient noise levels, but it takes 1s so don't do it every time - this will be less sensitive to changing conditions, though!
            '''
            if energy_threshold == -1:
                r.adjust_for_ambient_noise(source, duration=1)  # listen for 1 second to calibrate the energy threshold for ambient noise levels
                print("Chucking rate: ", source.CHUNK)
                print("format rate :", source.format)
                print(r.energy_threshold)
                r.energy_threshold += 2000
                energy_threshold = r.energy_threshold
                print(str(energy_threshold))
            else:
                r.energy_threshold = energy_threshold
            '''
            print("Say something!...")
            audio = r.listen(source)
            try:
                print("Trying sphinx")
                ts1 = time.time()
                request_text = r.recognize_sphinx(audio)
                ts2 = time.time()
                delta = ts2 - ts1
                print("Sphinx Speech recognizer thinks you said:\n" + request_text)
                print("request took " + str(delta) + "s.")
            except:
                print("Speech input cannot be understood.")
                request_text = input("\n\nYour text Input : ")
            return request_text

class Speech_Google(object):
    def __init__(self):
        with open('key.json') as key:
            self.GOOGLE_CLOUD_SPEECH_CREDENTIALS = json.dumps(json.load(key))

    def recognize(self):
        r = sr.Recognizer()
        # request spoken input
        with sr.Microphone(sample_rate=48000, chunk_size=1024) as source:
            r.adjust_for_ambient_noise(source, duration=1)
            # if this is the first time then we want to calibrate for ambient noise levels, but it takes 1s so don't do it every time - this will be less sensitive to changing conditions, though!
            '''
            if energy_threshold == -1:
                  # listen for 1 second to calibrate the energy threshold for ambient noise levels
                print("Chucking rate: ", source.CHUNK)
                print("format rate :", source.format)
                print(r.energy_threshold)
                r.energy_threshold += 2000
                energy_threshold = r.energy_threshold
                print(str(energy_threshold))
            else:
                r.energy_threshold = energy_threshold
            '''
            print("Say something!...")
            audio = r.listen(source)
            try:
                print("Trying google")
                ts1 = time.time()
                request_text = r.recognize_google_cloud(audio, credentials_json= self.GOOGLE_CLOUD_SPEECH_CREDENTIALS)
                ts2 = time.time()
                delta = ts2 - ts1
                print("google cloud speech recognizer thinks you said:\n" + request_text)
                print("request took " + str(delta) + "s.")
            except sr.UnknownValueError:
                print("Google Speech Recognition could not understand audio")
                request_text = input("\n\nYour text Input : ")
            except sr.RequestError as e:
                print("Could not request results from Google Speech Recognition service; {0}".format(e))
                request_text = input("\n\nYour text Input : ")
            except Exception as e:
                print("Speech input cannot be understood.")
                print(e)
                request_text = input("\n\nYour text Input : ")
            return request_text