from email.mime import audio
from flask import Flask, render_template, request, url_for, redirect, send_file, session
from pytube import YouTube
from io import BytesIO
import PyPDF2
import speech_recognition as sr
import pyttsx3
import googletrans
import gtts
import playsound
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = "654c0fb3968af9d5e6a9b3edcbc7051b"

@app.route("/", methods = ["GET", "POST"])
def home():
    if request.method == "POST":
        session['link'] = request.form.get('url')
        session['file_type'] = request.form.get('file_type')

        try:
            url = YouTube(session['link'])
            url.check_availability()
        except:
            return render_template("error.html")
        if(session['file_type']=="audio"):
            return render_template("downloadd.html", url = url)
        elif(session['file_type']=="video"):
            return render_template("download.html", url = url)
    return render_template("home.html")

@app.route("/download", methods = ["GET", "POST"])
def download_video():
    if request.method == "POST":
        buffer = BytesIO()
        url = YouTube(session['link'])
        itag = request.form.get("itag")
        video = url.streams.get_by_itag(itag)
        video.stream_to_buffer(buffer)
        buffer.seek(0)
        return send_file(buffer, as_attachment=True, download_name=f"Anurag-{url.title}.mp4", mimetype="video/mp4")
    return redirect(url_for("home"))
@app.route("/downloadd", methods = ["GET", "POST"])
def downloadd_audio():
    if request.method == "POST":
        buffer = BytesIO()
        url = YouTube(session['link'])
        itag = request.form.get("itag")
        video = url.streams.get_by_itag(itag)
        video.stream_to_buffer(buffer)
        buffer.seek(0)
        return send_file(buffer, as_attachment=True, download_name=f"Anurag---{url.title}.mp3", mimetype="video/mp4")
    return redirect(url_for("home"))
@app.route("/filesave", methods = ["GET", "POST"])
def downloadd_file():
    # print("working fine", request.form)
    if request.method == 'POST':
        f = request.files['file_type']
        print(f)
        ff  = f.filename
        print(f'{f.filename} finweeeeeeeeeeeeeeeeeee')
        p = request.form.get("languages")
        # print(f"{p} okkkkkkkkkkkkkkkkkkkkkkkkkkkkk")
        f.save(f.filename)
        r = sr.Recognizer()
        translator = googletrans.Translator()
        # print(googletrans.LANGUAGES)
        input_lang = 'en'
        output_lang = p

        def SpeakText(command):
            engine = pyttsx3.init()
            engine.say(command)
            engine.runAndWait()
        while (1):
            try:
                print("Now say as your wish...")
                book = open(ff, 'rb')
                pdfReader = PyPDF2.PdfFileReader(book)
                pages = pdfReader.numPages
                print(pages)
                speaker = pyttsx3.init()
                # for num in range(1, pages):
                page = pdfReader.getPage(0)
                MyText = page.extractText()
                print(MyText)
                # speaker.say(text)
                # speaker.runAndWait()
                # print("Did you say:- " + MyText)
                translated = translator.translate(MyText, dest=output_lang)
                # print(translated.text)
                # SpeakText(MyText)
                if(translated.text!=""):
                    converted_audio = gtts.gTTS(translated.text, lang=output_lang)
                    converted_audio.save(f'{ff[:len(ff)-4]}.mp3')
                # playsound.playsound(f'{ff[:len(ff)-4]}.mp3')
                return f'<body style="background-color:rgb(230, 225, 225)"><div style="width: 900px;margin:0px auto;"><h1 style=" background-color: #b8afaf;text-align: center;padding: 10px 0px;">PDF Orignal Text and PDF Converted Text</h1> <h2 style="border: 2px solid #ccc;border-radius: 10px; border: 1px solid rgb(60, 59, 59);padding: 10px;background-color:rgb(205, 205, 206);  margin-bottom: 20px;">Number of pages in pdf {pages}</h2><section style="border: 1px solid #ccc;border-radius: 10px; border: 1px solid rgb(60, 59, 59);padding: 10px;background-color:rgb(205, 205, 206);  margin-bottom: 40px;"><h3 style="text-transform: uppercase;color: #444;font-size: 25px;">PDF Orignal Text -></h3><p>{MyText}</p></section>  <section style="background-color:rgb(243, 227, 206);border: 2px solid #ccc;border-radius: 10px; border: 1px solid rgb(60, 59, 59);padding: 10px;"> <h3 style="text-transform: uppercase;color: #444;font-size: 25px;">PDF Converted Text -></h3><p>{translated.text}</p></section></div></body>'

            # os.system('start aa.mp3')
            # with open(str(aa), 'wb') as f:
            # 	converted.save('aa.mp3')
            # 	playsound.playsound('aa.mp3')

            except sr.RequestError as e:
                print("Could not request results; {0}".format(e))

            except sr.UnknownValueError:
                print("unknown error occured")


    #   return render_template("converted_file.html")

# @app.route("/filesave", methods = ["GET", "POST"])
# def downloadd_file():
   



      
if __name__ == '__main__':
    app.run(debug=True)