
import speech_recognition as sr

def voice():
    r = sr.Recognizer()

    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)

        print("Please say something")

        audio = r.listen(source)

        print("Recognizing Now .... ")


        try:
            print("You have said \n" + r.recognize_google(audio, language="fr-FR"))



        except Exception as e:
            print("Error :  " + str(e))




if __name__ == "__main__":
    voice()