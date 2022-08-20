import praw
import os
import requests
import numpy
import cv2
import pytesseract
import keys
import config


def resize(image):
    # Resizes the image up by a scale of 6
    return cv2.resize(image, None, fx=10, fy=10, interpolation=cv2.INTER_CUBIC)


def gray(image):
    # Converts RGB colors to gray.
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


def med_blur(image):
    # Blurs the image by taking the median of all pixels within the kernel,
    # and replacing central element with the median. Removes noise.
    return cv2.medianBlur(image, 3)


def threshold(image):
    # If pixel is less than 240 set to 0, if greater than 240 set to 255.
    return cv2.threshold(image, 240, 255, cv2.THRESH_BINARY)[1]


def opening(image):
    # More image blur and noise removal. Image erosion/dilation, increase kernel
    # size to increase blur.
    kernel = numpy.ones((10, 10), numpy.uint8)
    return cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)


def black_to_white(image, opening):
    image = 255 - opening
    return image


def preprocess(image):
    image = med_blur(image)
    image = resize(image)
    image = gray(image)
    image = threshold(image)
    open = opening(image)
    image = black_to_white(image, open)
    return image


def create_folder(image_path):
    # Creates the images folder to store untouched and preprocessed images.
    CHECK_FOLDER = os.path.isdir(image_path)
    if not CHECK_FOLDER:
        os.makedirs(image_path)


def dl_image(image_path, submission, image):
    # Downloads the scraped image.
    cv2.imwrite(f"{image_path}{subreddit}---{submission.id}.png", image)


def dl_preproccesed(image_path, submission, image):
    # Downloads the scraped image after preproccesing.
    cv2.imwrite(
        f"{image_path}pp---{subreddit}---{submission.id}.png", image)


def scrape_image(submission):
    # get url in lowercase, copy to .raw #
    response = requests.get(submission.url.lower(), stream=True).raw
    # convert to array of bytes, with uint8 encoding #
    image = numpy.asarray(bytearray(response.read()), dtype="uint8")
    # read image data from memory, convert to image format #
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)
    return image


def find_text(image):
    # Call pytesseract to find text within preprocessed image. If image
    # removed, prints "Image was not found".
    txt = pytesseract.image_to_string(image, config=config.config)
    if txt.isspace():
        print("Image was not found")
    else:
        print(txt.replace('\n', ' '))

    print("*******************************\n")


reddit = praw.Reddit(
    # Create a read only Reddit instance.
    client_id=keys.client_id,
    client_secret=keys.client_secret,
    user_agent=keys.user_agent,
)

# Create variable for the path of the images folder.
directory_path = os.path.abspath(os.path.curdir)
image_path = os.path.join(directory_path, "images/")
create_folder(image_path)

subreddit = reddit.subreddit(config.subreddits)
count = 0

for submission in subreddit.hot(limit=config.post_count):
    if "jpg" in submission.url.lower() or "png" in submission.url.lower():
        image = scrape_image(submission)
        dl_image(image_path, submission, image)
        image = preprocess(image)
        dl_preproccesed(image_path, submission, image)
        find_text(image)
