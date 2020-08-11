import os
import telegram
import requests
from io import BytesIO
from newspaper import Article
from PIL import Image,ImageDraw,ImageFont
from pytrends.request import TrendReq
from GoogleNews import GoogleNews

for k in list(os.environ.keys()): # remove this for loop block if u are behind any proxy
    if k.lower().endswith('_proxy'):
        del os.environ[k]

def make_square(im, min_size=1080, fill_color=(0, 0, 0, 0)):
    x, y = im.size
    size = max(min_size, x, y)
    new_im = Image.new('RGBA', (size, size), fill_color)
    new_im.paste(im, (int((size - x) / 2), int((size - y) / 2)))
    return new_im

# function to send message to telegram
def send_to_telegram(image,caption) :
    token = 'enter your bot token @botfather on telegram  just google this process'#enter your bot token from bot father
    chat_id = 'chat id to which you want to send ' # enter -your chat id of group or user to whom u want to send message
    bot = telegram.Bot(token=token)
    bot.send_photo(chat_id=chat_id, photo=open(image, 'rb'))
    bot.send_message(chat_id=chat_id, text= caption)
    return

#function to inset caption to image
def drawText(msg, pos): 
    fontSize = 102
    lines = []

    font = ImageFont.truetype("impact.ttf", fontSize)
    w, h = draw.textsize(msg, font)

    imgWidthWithPadding = img.width * 0.99

    # 1. how many lines for the msg to fit ?
    lineCount = 1
    if(w > imgWidthWithPadding):
        lineCount = int(round((w / imgWidthWithPadding) + 1))

    if lineCount > 2:
        while 1:
            fontSize -= 2
            font = ImageFont.truetype("impact.ttf", fontSize)
            w, h = draw.textsize(msg, font,stroke_width= 0)
            lineCount = int(round((w / imgWidthWithPadding) + 1))
            print("try again with fontSize={} => {}".format(fontSize, lineCount))
            if lineCount < 3 or fontSize < 10:
                break


    print("img.width: {}, text width: {}".format(img.width, w))
    print("Text length: {}".format(len(msg)))
    print("Lines: {}".format(lineCount))


    # 2. divide text in X lines
    lastCut = 0
    isLast = False
    for i in range(0,lineCount):
        if lastCut == 0:
            cut = (len(msg) // lineCount) * i
        else:
            cut = lastCut

        if i < lineCount-1:
            nextCut = (len(msg) // lineCount) * (i+1)
        else:
            nextCut = len(msg)
            isLast = True

        print("cut: {} -> {}".format(cut, nextCut))

        # make sure we don't cut words in half
        if nextCut == len(msg) or msg[nextCut] == " ":
            print("may cut")
        else:
            print("may not cut")
            while msg[nextCut] != " ":
                nextCut += 1
            print("new cut: {}".format(nextCut))

        line = msg[cut:nextCut].strip()

        # is line still fitting ?
        w, h = draw.textsize(line, font)
        if not isLast and w > imgWidthWithPadding:
            print("overshot")
            nextCut -= 1
            while msg[nextCut] != " ":
                nextCut -= 1
            print("new cut: {}".format(nextCut))

        lastCut = nextCut
        lines.append(msg[cut:nextCut].strip())

    print(lines)

    # 3. print each line centered
    lastY = -h
    if pos == "bottom":
        lastY = img.height - h * (lineCount+1) - 10

    for i in range(0,lineCount):
        w, h = draw.textsize(lines[i], font)
        textX = img.width/2 - w//2
        #if pos == "top":
        #    textY = h * i
        #else:
        #    textY = img.height - h * i
        textY = lastY + h
        draw.text((textX-2, textY-2),lines[i],(0,0,0),font=font,)
        draw.text((textX+2, textY-2),lines[i],(0,0,0),font=font)
        draw.text((textX+2, textY+2),lines[i],(0,0,0),font=font)
        draw.text((textX-2, textY+2),lines[i],(0,0,0),font=font)
        draw.text((textX, textY),lines[i],(255,255,255),font=font)
        lastY = textY


    return

print("select your source to genrate images and article")
print("I preffer  google news\n")
print("0 - google news top headlines")
print("1 - Google trends top 20")
inputval = int(input()) 

if inputval is 1 : #if input is 1 then import top20 trends from google trends

    pytrend = TrendReq(hl='en-US')
    trending_searches_df = pytrend.trending_searches(pn="india")

    k = ((trending_searches_df.head(20)))
    p = k.values.tolist()
    templink = []

    for i in p :
        query = ("".join(i))
        googlenews = GoogleNews(lang='en')
        googlenews.search(query)
        templink.extend (googlenews.get__links()[0:5]) # 0: 5 to take 5 url for each trend
    url_list = templink

if inputval is 0 : #if input is 0 then import top headines(url) from google news
        from pygooglenews import GoogleNews #saving lill time
        toplinks = []
        gn = GoogleNews(lang = 'en', country = 'IN')
        top = gn.top_news(proxies=None, scraping_bee = None)
        for i in (top['entries']) :
            toplinks.append(i.link) 
        url_list = toplinks 


for i in (url_list): #for each url we need to scrap it  using newspaper3k liabrary
    articalurl = i 
    try :
        toi_article = Article(articalurl, language="en") # en for English 
        toi_article.download() #download article for given url
        toi_article.parse() #parse unwannted text , html tags and css
        toi_article.nlp() # nlp to get keywords
        hashtags2= []
        hashtags = sorted(toi_article.meta_keywords + toi_article.keywords)
        for i in hashtags :
             hashtags2.append( ("".join(i.split())))
        hashtags2 = (" #".join(hashtags2)) # meta keywords and keyword of article converted into hashtags
        
        imagetitle = toi_article.title #article title as   text on image 
        caption = toi_article.text + hashtags2 # arcial text and hashtag to genrate caption
        imageurl = (toi_article.top_image) # url of image to use 
        
        response = requests.get(imageurl)
        img = Image.open(BytesIO(response.content))  #download image from url to img object

        #img = make_square(img, fill_color=(155, 215, 255,212)) # use this function make ur image square

        draw = ImageDraw.Draw(img) # draw image
        drawText(imagetitle, "bottom") # this function will place image title on image  at given postiton
        img.save("temp.png") #save genrated image to caption
        send_to_telegram("temp.png",caption) # send this image to ur telegram using ur bot

        
    except :
        print("skipping this url due to error ")



