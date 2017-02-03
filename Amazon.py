'''
Created on 20 Jan 2017

@author: Yuezhou He (John)
'''
from __builtin__ import raw_input
def p2f(x):
    return float(x.strip('%'))/100

def ratings(Product_ID):
    import requests
    import re
    page_param=''.join(("contextId=dpx&asin=",Product_ID))
    page=requests.get("https://www.amazon.com/gp/customer-reviews/widgets/average-customer-review/popover/ref=dpx_acr_pop_",params=page_param)
    web_text=re.findall("<span class=\"a-size-small\">.*%</span>",page.content)
    distribution_of_ratings=re.findall("[0-9]*%",''.join(web_text))
    mean=0
    second_moment=0
    sum_prob=0
    text_file=open("Ratings.txt","w")
    for idx, element in enumerate(distribution_of_ratings):
        text_file.write("%d stars: %s\n" % (5-idx,p2f(element)))
        mean=mean+(5-idx)*p2f(element)
        second_moment=second_moment+(5-idx)**2*p2f(element)
        sum_prob=sum_prob+p2f(element)
        if sum_prob>=0.5:
            median=5-idx
            sum_prob=-10
    varience=second_moment-(mean)**2
    text_file.write("mean: %f\nvarience: %f\nmedian: %d\n"  % (mean,varience,median))
    text_file.close()
    return 'Ratings distribution obtained and summary printed out to Ratings.txt'

def reviews(Product_ID):
    from amazon_scraper import AmazonScraper
    f=open('password.txt')
    f.readline()
    Access_key=f.readline().strip('\n')
    f.readline()
    Secret_key=f.readline().strip('\n')
    f.readline()
    Asso_tag=f.readline().strip('\n')
    amzn = AmazonScraper(Access_key,Secret_key,Asso_tag,MaxQPS=0.9, Timeout=5.0)
    p = amzn.lookup(ItemId=Product_ID)
    rs = p.reviews()
    all_reviews_on_page = list(rs)
    review_texts=[]
    for r in all_reviews_on_page:
        review_texts.append(r.full_review().text)
    text_file = open("Output.txt", "w")
    for idx,each_review in enumerate(review_texts):
        text_file.write("%d %s\n" % (idx,each_review.encode("utf8")))
    text_file.close()
    import csv
    with open("output.csv",'wb') as resultFile:
        wr = csv.writer(resultFile, dialect='excel')
        wr.writerow(review_texts)
    return 'Reviews obtained and printed out to Output.txt'

def cloud():
    import os
    from os import path
    from wordcloud import WordCloud
    d = path.dirname(os.path.realpath(__file__))
    text = open(path.join(d, 'Output.txt')).read()
    wordcloud = WordCloud().generate(text)
    import matplotlib.pyplot as plt
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.savefig("output.jpeg")
    return 'word cloud gernerated as output.jpeg'

Product_ID=raw_input('What is the Product ID?\n')
ratings(Product_ID)
reviews(Product_ID)
cloud()

