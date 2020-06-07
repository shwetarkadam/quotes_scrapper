import os

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS, cross_origin
import requests
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen as uReq
import  re
app = Flask(__name__)


@app.route('/', methods=['GET'])  # route to display the home page
@cross_origin()
def homePage():
    return render_template("index.html")


@app.route('/review', methods=['POST', 'GET'])  # route to show the review comments in a web UI
@cross_origin()
def index():
    if request.method == 'POST':
        try:
            searchString = request.form['content'].replace(" ", "")
            goodreads_url = "https://www.goodreads.com/quotes/search?utf8=%E2%9C%93&q="+searchString+"&commit=Search"
            uClient = uReq(goodreads_url)
            goodreadsPage = uClient.read()
            uClient.close()
            goodreads_html = bs(goodreadsPage, "html.parser")
            bigboxes = goodreads_html.findAll("div", {"class": "quote mediumText"})
            #del bigboxes[0:3]
            box = bigboxes[0]
            #productLink = "https://www.flipkart.com" + box.div.div.div.a['href']
            #prodRes = requests.get(productLink)
            #prodRes.encoding = 'utf-8'
            #prod_html = bs(prodRes.text, "html.parser")
            #print(prod_html)
            #commentboxes = prod_html.find_all('div', {'class': "_3nrCtb"})

            filename = searchString + ".csv"
            fw = open(filename, "w")
            headers = "Tags, Quote By, Quote \n"
            fw.write(headers)

            reviews = []
            for commentbox in bigboxes:
                try:
                    # name.encode(encoding='utf-8')
                    name = commentbox.div.div.find_all('span', {'class': 'authorOrTitle'})[0].text

                except:
                    name = 'No Name'

                try:
                    # rating.encode(encoding='utf-8')
                    quotes =  commentbox.div.text
                    final_quotes = re.findall(r'“(.*?)(?<!\\)”', quotes)
                    final_quotes = ' '.join([str(elem) for elem in final_quotes])


                except:
                    final_quotes = 'No quotes'

                try:
                    # commentHead.encode(encoding='utf-8')
                    tags = commentbox.find_all('div', {'class': 'greyText smallText left'})[0].text
                    tags = tags.strip()
                    res = tags.split("tags:")
                    del res[0]
                    res1 = [x.replace(' ', '') for x in res]
                    final_tags = [x.replace('\n', '') for x in res1]
                    final_tags=' ,'.join([str(elem) for elem in final_tags])

                except:
                    final_tags = 'No Tags'


                mydict = {"yoursearch": searchString, "Name": name, "quotes": final_quotes, "Tags": final_tags}
                reviews.append(mydict)
                content = final_tags + "," + name + "," + final_quotes
                fw.write(content)
            return render_template('results.html', reviews=reviews[0:(len(reviews) - 1)])
        except Exception as e:
            print('The Exception message is: ', e)
            return 'something is wrong'
    # return render_template('results.html')

    else:
        return render_template('index.html')

port = int(os.getenv("PORT"))
if __name__ == "__main__":
    #app.run(host='0.0.0.0', port=5000)
    app.run(host='0.0.0.0', port=port)
    # app.run(host='127.0.0.1', port=8001, debug=True)
