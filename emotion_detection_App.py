import cv2
from deepface import DeepFace
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk


camera = None
frame = None


face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')


def start_webcam():
    global camera, frame
    camera = cv2.VideoCapture(0)  
    if not camera.isOpened():
        messagebox.showerror("Error", "Unable to access the webcam.")
        return

    
    camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    update_frame()


def update_frame():
    global camera, frame
    if camera and camera.isOpened():
        ret, frame = camera.read()
        if ret:
            
            frame = cv2.resize(frame, (640, 480), interpolation=cv2.INTER_LINEAR)

            
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(rgb_frame)
            imgtk = ImageTk.PhotoImage(image=img)
            webcam_label.imgtk = imgtk
            webcam_label.configure(image=imgtk)
        webcam_label.after(20, update_frame)  


def capture_image():
    global frame
    if frame is not None:
        
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray_frame, scaleFactor=1.1, minNeighbors=5, minSize=(100, 100))

        if len(faces) > 0:
           
            (x, y, w, h) = faces[0]
            face_frame = frame[y:y + h, x:x + w]

           
            image_path = "captured_image.jpg"
            face_frame_resized = cv2.resize(face_frame, (224, 224))  # Resize for DeepFace
            cv2.imwrite(image_path, face_frame_resized)
            messagebox.showinfo("Image Saved", f"Image saved as {image_path}")
            display_captured_image(image_path)
            detect_emotion(image_path)
        else:
            messagebox.showerror("Error", "No face detected. Please try again.")
    else:
        messagebox.showerror("Error", "No frame captured from the webcam.")


def display_captured_image(image_path):
    try:
        captured_image = Image.open(image_path)
       
        imgtk = ImageTk.PhotoImage(captured_image)
        captured_label.imgtk = imgtk
        captured_label.configure(image=imgtk)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to display captured image: {e}")

def detect_emotion(image_path):
    try:
    
        analysis = DeepFace.analyze(img_path=image_path, actions=['emotion'], enforce_detection=False)

        if isinstance(analysis, list):
            analysis = analysis[0]  

        dominant_emotion = analysis['dominant_emotion']

        result_text.config(text=f"Detected Emotion: {dominant_emotion}", fg="green")
    except Exception as e:
        result_text.config(text=f"Emotion detection failed: {str(e)}", fg="red")

def stop_webcam():
    global camera
    if camera and camera.isOpened():
        camera.release()
    webcam_label.configure(image="")
    messagebox.showinfo("Webcam Stopped", "Webcam feed stopped.")

root = Tk()
root.title("Emotion Detection")
root.geometry("1000x700")
root.configure(bg="#f0f0f0")


title_label = Label(root, text="Emotion Detection App", font=("Arial", 24, "bold"), bg="#f0f0f0", fg="#333")
title_label.pack(pady=10)


main_frame = Frame(root, bg="#f0f0f0")
main_frame.pack(pady=10)


webcam_frame = Frame(main_frame, bg="#f0f0f0")
webcam_frame.grid(row=0, column=0, padx=20)
webcam_label = Label(webcam_frame, text="Webcam Feed", bg="gray")
webcam_label.pack(fill=BOTH, expand=True)

captured_frame = Frame(main_frame, bg="#f0f0f0")
captured_frame.grid(row=0, column=1, padx=20)
captured_label = Label(captured_frame, text="Captured Image", bg="lightgray")
captured_label.pack(fill=BOTH, expand=True)


button_frame = Frame(root, bg="#f0f0f0")
button_frame.pack(pady=10)

start_button = Button(button_frame, text="Start Webcam", command=start_webcam, font=("Arial", 14), bg="green", fg="white")
start_button.grid(row=0, column=0, padx=10)

capture_button = Button(button_frame, text="Capture Image", command=capture_image, font=("Arial", 14), bg="blue", fg="white")
capture_button.grid(row=0, column=1, padx=10)

stop_button = Button(button_frame, text="Stop Webcam", command=stop_webcam, font=("Arial", 14), bg="red", fg="white")
stop_button.grid(row=0, column=2, padx=10)

result_text = Label(root, text="Detected Emotion: None", font=("Arial", 18), bg="#f0f0f0", fg="#333")
result_text.pack(pady=20)

root.mainloop()

if camera and camera.isOpened():
    camera.release()
