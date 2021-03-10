import pandas as pd
import re
#import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer

dataset = pd.read_csv('bbc-text.csv')

#nltk.download('stopwords')
stop_words = set(stopwords.words("english"))
new_stopwords = [',','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
new_stopwords_list = stop_words.union(new_stopwords);  

words = []

for i in range(0, 2225):
    text = re.sub('[^a-zA-Z]',' ', dataset['text'][i])
    text = text.lower()
    text = text.split()
    ps = PorterStemmer()
    text = [ps.stem(word) for word in text if not word in set(new_stopwords_list)]
    text = ' '.join(text)
    words.append(text)

from sklearn.feature_extraction.text import TfidfVectorizer
tfidfvect = TfidfVectorizer(stop_words = new_stopwords_list);
x = tfidfvect.fit_transform(words).toarray()

tfidf_tokens = tfidfvect.get_feature_names()

df_tfidfvect = pd.DataFrame(data = x,columns = tfidf_tokens)

print("\nTF-IDF Vectorizer\n")
print(df_tfidfvect)


y = dataset['category']

from sklearn.model_selection import train_test_split
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.3, random_state = 0)

from sklearn.naive_bayes import MultinomialNB
classifier = MultinomialNB()
classifier.fit(x_train, y_train)

y_pred = classifier.predict(x_test);

politicsample =['When he spoke to the Democratic National Convention in support of Senator John Kerry, the party’s presidential nominee against George W. Bush, Barack Obama was an obscure state senator running for the US Senate. His soaring speech made the case for putting aside partisan differences and bringing Americans together; it also introduced him to the country and meant that he was instantly tipped to become a future president.We worship an awesome God in the blue states and we don’t like federal agents poking around in our libraries in the Red States.'] 
y_pred_perticular = classifier.predict(tfidfvect.transform(politicsample).toarray())

sportsample = ['To the fans and everybody in Gator Nation, I\'m sorry. I\'m extremely sorry. We were hoping for an undefeated season. That was my goal, something Florida has never done here. I promise you one thing, a lot of good will come out of this. You will never see any player in the entire country play as hard as I will play the rest of the season. You will never see someone push the rest of the team as hard as I will push everybody the rest of the season. You will never see a team play harder than we will the rest of the season. God Bless.'] 
y_pred_perticular = classifier.predict(tfidfvect.transform(sportsample).toarray())


from sklearn.metrics import confusion_matrix
cm = confusion_matrix(y_test, y_pred)
print(cm)

from sklearn.metrics import accuracy_score
a = accuracy_score(y_test,y_pred)
print("The accuracy of this model is: ", a*100)


from sklearn.metrics import precision_score,recall_score,f1_score

print('precision:',precision_score(y_test,y_pred,average="macro"))
print('recall:',recall_score(y_test,y_pred,average="macro"))
print('fscore:',f1_score(y_test,y_pred,average="macro"))
