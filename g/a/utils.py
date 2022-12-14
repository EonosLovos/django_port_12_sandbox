import base64
import io
import os
import urllib.parse
from typing import Any, List, Optional
from collections import Counter
import matplotlib.pyplot as plt
import pandas as pd
from django.core.files.uploadedfile import UploadedFile
from PIL import Image
from wordcloud import STOPWORDS, WordCloud

stopwords = set(STOPWORDS)

def show_wordcloud(data: Optional[Counter]) -> Optional[Image.Image]:
	"""Convert matplotlib data to image."""
	try:
		wordcloud = WordCloud(
			background_color="white",max_words=400,max_font_size=400,
			scale=3,width=1600, height=1200, random_state=0,stopwords=stopwords)
		wordcloud.generate(str(data))
		plt.imshow(wordcloud, interpolation="bilinear")
		plt.axis("off")
		image = io.BytesIO()
		plt.savefig(image, format="png")
		image.seek(0)
		string = base64.b64encode(image.read())
		image_64 = "data:image/png;base64," +   urllib.parse.quote_plus(string)
		return image_64
	except ValueError:
		return None