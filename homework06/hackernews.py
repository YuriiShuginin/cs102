from bottle import (
    route, run, template, request, redirect
)

from scraputils import get_news
from db import News, session
from bayes import NaiveBayesClassifier


@route("/news")
def news_list():
    s = session()
    rows = s.query(News).filter(News.label == None).all()
    return template('news_template', rows=rows)


@route("/add_label/")
def add_label():
    label = request.query.label
    id_value = request.query.id
    s = session()
    news = s.query(News).filter(News.id == id_value).one()
    news.label = label
    s.commit()
    redirect("/news")


@route("/update")
def update_news():
    news_list = get_news("https://news.ycombinator.com/newest", n_pages=1)
    s = session()
    for news in news_list:
        if s.query(News).filter(News.title == news['title'], News.author == news['author']).first() == None:
            newest = News(title=news['title'], author=news['author'], url=news['url'], comments=news['comments'], points=news['points'])
            s.add(newest)
    s.commit()
    redirect("/news")


@route("/classify")
def classify_news():
    # PUT YOUR CODE HERE
    pass


if __name__ == "__main__":
    run(host="localhost", port=8080)