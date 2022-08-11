import praw
import os
import requests
import numpy
import cv2
import pytesseract

reddit = praw.Reddit(
    client_id="",
    client_secret="",
    user_agent="",
)

def gray(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

def med_blur(image):
    return cv2.medianBlur(image, 3)

def threshold(image):
    return cv2.threshold(image, 240, 255, cv2.THRESH_BINARY)[1]

def resize(image):
    return cv2.resize(image, None, fx = 6, fy = 6, interpolation = cv2.INTER_CUBIC)

def black_to_white(image, opening):
    image = 255 - opening
    return image 

def preprocessing(image):
    image = resize(image)
    image = gray(image)
    image = med_blur(image)
    image = threshold(image)
    kernel = numpy.ones((5,5), numpy.uint8)
    opening = cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)
    image = black_to_white(image, opening)
    return image

def create_folder(image_path):
    CHECK_FOLDER = os.path.isdir(image_path)
    if not CHECK_FOLDER:
        os.makedirs(image_path)

def scrape_image(submission):
    response = requests.get(submission.url.lower(), stream = True).raw
    image = numpy.asarray(bytearray(response.read()), dtype = "uint8")
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)
    cv2.imwrite(f"{subreddit}-{submission.id}.png", image)
    return image

def scrape_preproccesed(submission, image):
    cv2.imwrite(f"{subreddit}xxx{submission.id}.png", image)
    return

def find_text(image):
    txt = pytesseract.image_to_string(image, 
    config='-c tessedit_char_whitelist="ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890 "')
    if txt.isspace():
        print("Image was not found")
    else:
        print(txt.replace('\n', ' '))

    print("*******************************")

directory_path = os.path.abspath(os.path.curdir)
image_path = os.path.join(directory_path, "images/")
create_folder(image_path)

subreddit = reddit.subreddit("AdviceAnimals")

for submission in subreddit.hot(limit = 5):
    if "jpg" in submission.url.lower() or "png" in submission.url.lower():
        image = scrape_image(submission)
        image = preprocessing(image)
        scrape_preproccesed(submission, image)
        find_text(image)
        
        
