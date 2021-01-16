from flask import Flask
from app.models import Users, Products, User_Reviews
from rake_nltk import Rake
import nltk 
from nltk.corpus import stopwords
import psycopg2

def getText(product_name):
  # texts = User_Reviews.query.filter_by(product_name=product_name).all()
  # test using: 
  texts = User_Reviews.query.filter_by(product_name=product_name).all()
  if len(texts) >= 100:
    texts = User_Reviews.query.filter_by(product_name=product_name).limit(100).all()

  if len(texts) == 0:
    print("No reviews found")
    return
  else:
    textList = []
    for t in texts:
      # remove non english words
      words = set(nltk.corpus.words.words())
      text = t.text
      text = " ".join(w for w in nltk.wordpunct_tokenize(text)if w.lower() in words or not w.isalpha())
      # remove punctuation
      punc = '''!()-[]{};:'"\, <>/?@#$%^&*_~'''
      for char in text:  
          if char in punc:  
              text = text.replace(char, " ")  

      textList.append(text)
    text = ' .'.join(textList)
    return text

def saveKeywords(product_name):
  r = Rake(stopwords=stopwords.words('english'))
  if getText(product_name) is not None:
    r.extract_keywords_from_text(getText(product_name))
    keywords = list(r.get_ranked_phrases()[:5])
    updateTable(product_name,keywords)
  else:
    print(product_name, "has no reviews to extract")

def updateTable (product_name, keywords):
    try:
        connection = psycopg2.connect(user = "my_user",
                                  password = "admin",
                                  host = "127.0.0.1",
                                  port = "5432",
                                  database = "my_database")

        cursor = connection.cursor()
        print("connected and began updating ")
        sql_update_query = """Update products set keywords = %s where product_name = %s"""
        cursor.execute(sql_update_query, (keywords, product_name))
        connection.commit()
        count = cursor.rowcount
        print(count, "Record Updated successfully ")

        # # show table after update
        # print("Table After updating record ")
        # sql_select_query = """select * from products where product_name = %s"""
        # cursor.execute(sql_select_query, (product_name,))
        # record = cursor.fetchone()
        # print(record)

    except (Exception, psycopg2.Error) as error:
        print("Error in update operation", error)

    finally:
        # closing database connection.
        if (connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")

def updateAllKeywords():
  products = Products.query.all()
  for p in products:
    product_name = p.product_name
    print("Updating product: ",product_name)
    saveKeywords(product_name)

# updateAllKeywords()

def calTotalSentimentScore():
  product = Products.query.all()
  for p in product:
    product_name = p.product_name
    num_reviews = p.no_of_review
    print("Updating score for: ",product_name)
    if num_reviews != None:
      all_reviews = User_Reviews.query.filter_by(product_name=product_name).all()
      all_scores = 0
      for a in all_reviews:
        all_scores += int(a.sentiment_score)
      result = round((all_scores / (len(all_reviews)*5))* 5)
    else:
      result = None
    updateScoreinProduct(product_name,result)
    # updateScoreinProduct(product_name,round(result))
  # # to filter reviews for each sentiment score
  # for review in range(5):
  #   reviews_sentiment.append(User_Reviews.query.filter_by(product_name=product_name, sentiment_score=str(review+1)).all())
  # print(reviews_sentiment[0])

def updateScoreinProduct (product_name, score):
    try:
        connection = psycopg2.connect(user = "my_user",
                                  password = "admin",
                                  host = "127.0.0.1",
                                  port = "5432",
                                  database = "my_database")

        cursor = connection.cursor()
        print("connected and began updating ")
        sql_update_query = """Update products set overall_sentiment= %s where product_name = %s"""
        cursor.execute(sql_update_query, (score, product_name))
        connection.commit()
        count = cursor.rowcount
        print(count, "Record Updated successfully ")

        # # show table after update
        # print("Table After updating record ")
        # sql_select_query = """select * from products where product_name = %s"""
        # cursor.execute(sql_select_query, (product_name,))
        # record = cursor.fetchone()
        # print(record)

    except (Exception, psycopg2.Error) as error:
        print("Error in update operation", error)

    finally:
        # closing database connection.
        if (connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")

calTotalSentimentScore()