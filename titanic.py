import streamlit as st
import pandas as pd
import pickle
rose = ('https://static.wikia.nocookie.net/heroes-of-the-characters/images/c/cc/Rose_DeWitt_Bukater.jpg')
jack = 'https://static.wikia.nocookie.net/jamescameronstitanic/images/c/c6/Untitledaksjk.png'



filename = 'final_model.sav'
model = pickle.load(open(filename, 'rb'))





def title_extractor(name):
    titles_range = ['Dr.', 'Mr.', 'Mrs.', 'Ms.', 'Rev.',
                    'Miss.', 'Master.', 'Don.', 'Mme.',
                    'Major.', 'Lady.', 'Sir.', 'Mlle.', 'Col.', 'Capt.', 'Countess.', 'Jonkheer.']
    test = name.split(' ')
    res = ''
    for x in test:
        if x in titles_range:
            res = x
            return res
            break
        else:
            res = ['none', name]


train = pd.read_csv('titanic.csv')

for idx, full_name in enumerate(train.Name):
    train.loc[idx, 'Name'] = title_extractor(full_name)
train.loc[:, 'family_size'] = train.loc[:, 'Parch'] + train.loc[:, 'SibSp']
train['single'] = (train.family_size == 0).astype('int')

titles = ('Dr.', 'Mr.', 'Mrs.', 'Ms.', 'Rev.',
          'Miss.', 'Master.', 'Don.', 'Mme.',
          'Major.', 'Lady.', 'Sir.', 'Mlle.', 'Col.', 'Capt.', 'Countess.', 'Jonkheer.')

ports_range = ('Queesntown, Ireland', 'Southampton, U.K.', ' Cherbourg, France')

classes = (1, 2, 3)

family_size_range = train.family_size.unique()

st.markdown("""
<style>
.big-font {

    font-size:60px !important;
   
     color :#C7BACC !important;
               font-family: 'Roboto', sans-serif;
}

.colored-font {
    font-size:50px !important;
    color: grey !important;
    font-weight: bold;

}
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="big-font">Will you make it if you were on the Titanic? Describe your self using left menu and find out. </p>', unsafe_allow_html=True)

st.sidebar.title('Describe yourself')

title = st.sidebar.selectbox('Your title', titles)

gender = st.sidebar.radio('Sex', ('Male', 'Female'))
gender_value = [1, 0] if gender == 'Female' else [0, 1]

status = st.sidebar.radio('Single?', ('Yes', 'No'))

status_value = 1 if status == "Yes" else 0

age = st.sidebar.slider('Age', 0, 90, 1)

family_size = st.sidebar.slider('How many family members with you?', int(family_size_range.min()),
                                int(family_size_range.max()), int(1))

pclass = st.sidebar.radio('Class', classes)

fare_range = train.loc[train['Pclass'] == pclass, 'Fare']

cabin = st.sidebar.radio('Cabin', (0, 1))

ports = st.sidebar.radio('Port of departure', ports_range)

fare = st.sidebar.slider('How much was your ticket (£)?', min(fare_range), max(fare_range))

# building input variable
titles_vector = [int(x == title) for x in titles]
embarked_vector = [int(x == ports) for x in ports_range]

prediction_inp = [pclass] + [age] + [fare] + [cabin] + \
                 [family_size] + [status_value] + titles_vector + gender_value + embarked_vector


prediction_inp = [pclass] + [age] + [fare] + [cabin] + \
                 [family_size] + [status_value] + titles_vector + gender_value + embarked_vector

survial = model.predict_proba([prediction_inp])[0,1]

if survial*100 > 50:


    fate = 'Rose'
else:


    fate = 'Jack'


md_results_green = f"<p class=\"colored-font\"> There is a <span style=\"color: green\"> {survial*100}% </span> you will end up like <span style=\"color: green\"> {fate} </span></p>"
md_results_red = f"<p class=\"colored-font\"> There is a <span style=\"color: red\"> {(survial)*100}% </span> you will end up like <span style=\"color: red\"> {fate} </span></p>"

if survial*100 > 50:
    md_results = md_results_green
    image = rose

else:
    md_results = md_results_red
    image = jack



st.markdown(md_results, unsafe_allow_html=True)
st.image(image, caption='You will likely end like '+fate)
