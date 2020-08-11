# socail_content_collector
creates a list of url from  google news of google trends . Then scraps  artical title ,text, keywords. genrates hashtags from this keywors and meta discription.  places article title  on artical image and  creates a message  from hashtags  and artical text . now sends  this processed image  and msg to urs telegram . now u ca share this image to socail media and also  now you have caption with hashtags . 

code is pretty much basic.

process :

 1)  choose from two options - google news or google trends
 2)  if - google news :
            script will scrap top headlines froms google news and  store this urls in a list
     if - google trends : 
           script will scrap top 20 current trends and store this urls in a list
 3) for each url in list  :
        scrap  artical  title, image , text ,meta keyword and keywords
        create new image from artical image and place artical title over it
        create a caption  from  artical text + (artical meta keywords and keywords  converted into hashtags)
        send this image and caption to telegram using bot token and chat id 
        
### you can make changes as you want is prettyeasy ,add new sources to genrate url , use any other socail platform discord etc , telegram is good thowgh


