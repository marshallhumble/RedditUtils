import newspaper

cnn_paper = newspaper.build('http://rfa.org')

for article in cnn_paper.articles:
    print(article.url)
    article.download()
    article.parse()
    print(article.text)
