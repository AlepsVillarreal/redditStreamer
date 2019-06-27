# Start with loading all necessary libraries
import numpy as np
import pandas as pd
from os import path
from PIL import Image
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator

import matplotlib.pyplot as plt

#Read the sample.data
df = pd.read_csv('example.csv', encoding='ISO-8859-1')
print(df)



#text = data.Tweet.values
#wordcloud = WordCloud(
#    width = 3000,
#    height = 2000,
#    background_color = 'black',
#    stopwords = STOPWORDS).generate(str(text))
#fig = plt.figure(
#    figsize = (40, 30),
#    facecolor = 'k',
#    edgecolor = 'k')
#plt.imshow(wordcloud, interpolation = 'bilinear')
#plt.axis('off')
#plt.tight_layout(pad=0)
#plt.show()