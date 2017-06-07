from flask import Flask
from flask import jsonify
import requests
from lxml import html
from flask import request

app = Flask(__name__)

@app.route('/')
def request_peli():
	
	title_id = request.args.get('i')
	if not title_id:
		return "usage: xxx/?i=id"

	response = requests.get('http://www.imdb.com/title/'+title_id)
	tree = html.fromstring(response.content)
	
	result={}
	result["id"]=title_id
	#Capturo generos
	aux=tree.xpath('//div[@class="title_wrapper"]//span[@itemprop="genre"]/text()')
	result["Genre"]=", ".join(aux).strip()

	aux=tree.xpath('//div[@class="titleBar"]/div[@class="title_wrapper"]/h1/text()')
	result["Title"]="".join(aux).strip()

	aux=tree.xpath('//div[@class="titleBar"]/div[@class="title_wrapper"]/h1/span/a/text()')
	result["Year"]="".join(aux).strip()



	aux=tree.xpath('//div[@class="titleBar"]/div[@class="title_wrapper"]//meta[@itemprop="contentRating"]/@content')
	result["Rated"]="".join(aux).strip()

	aux=tree.xpath('//div[@class="titleBar"]/div[@class="title_wrapper"]//meta[@itemprop="datePublished"]/@content')
	result["Released"]="".join(aux).strip()

	aux=tree.xpath('//div[@id="titleDetails"]//time[@itemprop="duration"]/text()')
	result["Runtime"]="".join(aux[0:1]).strip()

	aux=tree.xpath('//div[@class="credit_summary_item"]/span[@itemprop="director"]//span[@itemprop="name"]/text()')
	result["Director"]="".join(aux).strip()

	aux=tree.xpath('//div[@class="credit_summary_item"]/span[@itemprop="creator"]//span[@itemprop="name"]/text()')
	result["Writer"]=", ".join(aux).strip()

	aux=tree.xpath('//div[@class="credit_summary_item"]/span[@itemprop="actors"]//span[@itemprop="name"]/text()')
	result["Actors"]=", ".join(aux).strip()

	aux=tree.xpath('//div[@class="summary_text" and  @itemprop="description"]/text()')
	result["Plot"]="".join(aux).strip()

	aux=tree.xpath('//div[@id="titleDetails"]//h4[text() = "Country:"]/following-sibling::node()/text()')
	result["Country"]="".join(aux).strip()

	aux=tree.xpath('//div[@id="titleDetails"]//h4[text() = "Language:"]/following-sibling::node()/text()')
	result["Language"]="".join(aux).strip()


	aux=tree.xpath('//div[@class="imdbRating"]//span[@itemprop="ratingValue"]/text()')
	result["imdbRating"]="".join(aux).strip()

	aux=tree.xpath('//div[@class="imdbRating"]//span[@itemprop="ratingCount"]/text()')
	result["imdbVotes"]="".join(aux).strip()
	return jsonify(result)

