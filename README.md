![Alt text](photos/banner.jpg?raw=true "Title")

***Cyber Transcriber*** is a Reddit bot that does its best to transcribe online images such as memes. ***Cyber Transcriber*** also has an optional functionality of working as an image scraper for any subreddit.

# Setup
- Create a Reddit account!
- got to https://ssl.reddit.com/prefs/apps/ and click create app.
- Save your
> client_id

> client_secret

> user_agent
- Input your keys when you create the reddit instance.

# Installation
- Run the following to install all of the dependencies needed.
> $ pip install -r requirements.txt

# Usage
- If the image scraping functionality is not needed, the following code can be commented out:
> create_folder(image_path)

> dl_image(image_path, submission, image)

> dl_preprocced(image_path, submission, image)
- This can be seen below:

![Alt text](photos/code1.jpg?raw=true "Title")

- Change the desired subreddit and amount of posts in the config file.
- The following filters can be applied:
> controversial, gilded, hot, new, rising, top
- This must be changed by replace "hot" in the following line of code:

![Alt text](photos/code2.jpg?raw=true "Title")

# How It Works
- If the image scraping functionality is desired a folder called images will be created and filled with all photos that are found.
- Each photo is preproccessed utilizing the OpenCV library functions. 

## Before
![Alt text](photos/before.jpg?raw=true "Title")

## After
![Alt text](photos/after.jpg?raw=true "Title")

- By using pytesseract a wrapper for Google's Tesseract-Opical Character Recognition(OCR) tool we can attempt to read the text within the images.

## Output
![Alt text](photos/output.jpg?raw=true "Title")

# Notes
- Images that have been removed or deleted from Reddit will be blank and will output "Image was not found".
- ***Cyber Transcriber*** is trying its best, but is not 100% correct. It is a work in progress and image preproccessing techniques will be researched until accuracy is improved. 
- Once ***Cyber Transcriber*** is more accurate, ***Cyber Transcriber*** will be able to be called on Reddit, and will comment the image text. 








