import streamlit as st
import time
from deep_translator import GoogleTranslator
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
import readtime
import textstat
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.text_rank import TextRankSummarizer
from sumy.summarizers.lex_rank import LexRankSummarizer
from io import StringIO


nltk.download('punkt')
nltk.download('punkt_tab')
nltk.download('stopwords')

# Page layout
st.set_page_config(page_title="MultiNLP Suite", 
                   page_icon=":robot_face:",
                   layout="wide",
                   initial_sidebar_state="expanded"
                   )

def p_title(title):
    st.markdown(f'<h3 style="text-align: left; color:#F63366; font-size:28px;">{title}</h3>', unsafe_allow_html=True)

# Creating Sidebar
st.sidebar.header('I want to :crystal_ball:')
nav = st.sidebar.radio('',['Go to homepage', 'Summarize text', 'Translate text', 'Analyze text'])
st.sidebar.write('')
st.sidebar.write('')
st.sidebar.write('')
st.sidebar.write('')
st.sidebar.write('')

# Contact Info
expander = st.sidebar.expander('Contact')
expander.markdown(
    """
    I'd love your feedback :smiley: Want to collaborate? Develop a project? 
    Find me on [LinkedIn](https://www.linkedin.com/in/sumitsingh3072/)
    """
)
#HOMEPAGE
if nav == 'Go to homepage':

    st.markdown("<h1 style='text-align: center; color: white; font-size:28px;'>Welcome to Multi-NLP!</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; font-size:56px;'<p>&#129302;</p></h3>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; color: grey; font-size:20px;'>Summarize, paraphrase, analyze text & more. Try our models, browse their source code, and share with the world!</h3>", unsafe_allow_html=True)
    """
    [![Buy me a coffee](https://img.shields.io/badge/Buy%20me%20a%20coffee--yellow.svg?logo=buy-me-a-coffee&logoColor=orange&style=social)](https://buymeacoffee.com/sumitsingh3072)
    """
    st.markdown('___')
    st.write(':point_left: Use the menu at left to select a task (click on > if closed).')
    st.markdown('___')

    st.markdown("<h3 style='text-align: left; color:#F63366; font-size:18px;'><b>Who is this App for?<b></h3>", unsafe_allow_html=True)
    st.write("Anyone can use this App completely for free! If you like it :heart:, show your support by sharing :+1: ")
    st.write("Are you into NLP? Our code is 100% open source and written for easy understanding. Fork it from [GitHub] (https://github.com/sumitsingh3072/MultiNLP-Suite), and pull any suggestions you may have. Become part of the community! Help yourself and help others :smiley:")

#SUMMARIZE
if nav == 'Summarize text':    
    st.markdown("<h4 style='text-align: center; color:grey;'>Summariser &#129302;</h4>", unsafe_allow_html=True)
    st.text('')
    p_title('Summarize')
    st.text('')

    source = st.radio("How would you like to start? Choose an option below",
                          ("I want to input some text", "I want to upload a file"))
    st.text('')
    
    s_example = "Artificial Intelligence (AI) refers to the creation of machines that can perform tasks requiring human-like intelligence, including reasoning, learning, problem-solving, perception, and language understanding. AI spans various fields, the most prominent being machine learning, where systems use algorithms to analyze data, recognize patterns, and improve their performance over time without human intervention. Another key area is natural language processing (NLP), which allows machines to understand, interpret, and generate human language, enabling applications like chatbots, language translators, and virtual assistants. Computer vision is another significant AI component, giving machines the ability to interpret and understand visual information from the world, such as recognizing faces or detecting objects in images and videos. AI’s impact is vast, transforming industries from healthcare, where AI is aiding in disease diagnosis and personalized treatment plans, to transportation with autonomous vehicles, and finance through automated trading systems and fraud detection. As AI evolves, it brings significant advancements but also challenges, such as ethical concerns around data privacy, potential bias in algorithms, and the future of employment in an increasingly automated world. Nonetheless, AI holds the promise of revolutionizing countless sectors and improving efficiency, productivity, and innovation on a global scale."
    if source == 'I want to input some text':
        input_su = st.text_area("Use the example below or input your own text in English (between 1,000 and 10,000 characters)", value=s_example, max_chars=10000, height=330)
        
        if st.button('Summarize'):
            if len(input_su) < 1000:
                st.error('Please enter a text in English of minimum 1,000 characters')
            else:
                with st.spinner('Processing...'):
                    time.sleep(2)

                    # TextRank Summarization
                    my_parser = PlaintextParser.from_string(input_su, Tokenizer('english'))
                    text_rank_summarizer = TextRankSummarizer()
                    text_rank_summary = text_rank_summarizer(my_parser.document, sentences_count=3)
                    tr_result = " ".join(str(sentence) for sentence in text_rank_summary)
                    tr_result_len = str(len(tr_result)) + ' characters (' + "{:.0%}".format(len(tr_result) / len(input_su)) + ' of original content)'
                    
                    st.markdown('___')
                    st.write('TextRank Model')
                    st.caption(tr_result_len)
                    st.success(tr_result)

                    # LexRank Summarization
                    lex_rank_summarizer = LexRankSummarizer()
                    lexrank_summary = lex_rank_summarizer(my_parser.document, sentences_count=3)
                    lr_result = " ".join(str(sentence) for sentence in lexrank_summary)
                    lr_result_len = str(len(lr_result)) + ' characters (' + "{:.0%}".format(len(lr_result) / len(input_su)) + ' of original content)'

                    st.markdown('___')
                    st.write('LexRank Model')
                    st.caption(lr_result_len)
                    st.success(lr_result)
                    st.balloons()


    if source == 'I want to upload a file':
        file = st.file_uploader('Upload your file here', type=['txt'])
        if file is not None:
            with st.spinner('Processing...'):
                time.sleep(2)
                stringio = StringIO(file.getvalue().decode("utf-8"))
                string_data = stringio.read()
                if len(string_data) < 1000 or len(string_data) > 10000:
                    st.error('Please upload a file between 1,000 and 10,000 characters')
                else:
                    # TextRank Summarization
                    my_parser = PlaintextParser.from_string(string_data, Tokenizer('english'))
                    text_rank_summarizer = TextRankSummarizer()
                    text_rank_summary = text_rank_summarizer(my_parser.document, sentences_count=3)
                    t_r = " ".join(str(sentence) for sentence in text_rank_summary)
                    result_t_r = (str(len(t_r)) + ' characters (' + "{:.0%}".format(len(t_r)/len(string_data)) + ' of original content)')
                    
                    st.markdown('___')
                    st.write('TextRank Model')
                    st.caption(result_t_r)
                    st.success(t_r) 

                    # Scoring Model
                    text = string_data
                    stopWords = set(stopwords.words("english"))
                    words = word_tokenize(text)
                    freqTable = dict()

                    for word in words:
                        word = word.lower()
                        if word in stopWords:
                            continue
                        freqTable[word] = freqTable.get(word, 0) + 1

                    sentences = sent_tokenize(text)
                    sentenceValue = dict()

                    for sentence in sentences:
                        for word, freq in freqTable.items():
                            if word in sentence.lower():
                                sentenceValue[sentence] = sentenceValue.get(sentence, 0) + freq

                    sumValues = sum(sentenceValue.values())
                    average = int(sumValues / len(sentenceValue)) if sentenceValue else 0
                    summary = ' '.join(sentence for sentence in sentences if sentence in sentenceValue and sentenceValue[sentence] > (1.3 * average))
                    s_m = summary
                    result_s_m = (str(len(s_m)) + ' characters (' + "{:.0%}".format(len(s_m)/len(string_data)) + ' of original content)')

                    st.markdown('___')
                    st.write('Scoring Model')
                    st.caption(result_s_m)
                    st.success(s_m)

                    # LexRank Summarization
                    lex_rank_summarizer = LexRankSummarizer()
                    lexrank_summary = lex_rank_summarizer(my_parser.document, sentences_count=3)
                    l_r = " ".join(str(sentence) for sentence in lexrank_summary)
                    result_l_r = (str(len(l_r)) + ' characters (' + "{:.0%}".format(len(l_r)/len(string_data)) + ' of original content)')

                    st.markdown('___')
                    st.write('LexRank Model')
                    st.caption(result_l_r)
                    st.success(l_r)
                    st.balloons()

#Translator
if nav == 'Translate text':
    st.markdown("<h4 style='text-align: center; color:grey;'>Translator&#129302;</h4>", unsafe_allow_html=True)
    st.text('')    
    p_example = 'In the heart of a bustling city, a small coffee shop stood, often overlooked. Its walls were adorned with local art, and the aroma of freshly brewed coffee wafted through the air. Inside, regulars gathered, sharing stories and laughter. One rainy afternoon, a newcomer entered, seeking refuge from the storm. The barista, with a warm smile, recommended a house special. As the stranger took a sip, they realized that sometimes the best moments come from unexpected places.'
    input_pa = st.text_area("Use the example below or input your own text in English (maximum 500 characters)", max_chars=500, value=p_example, height=160)

    if st.button('Translate'):
            if input_pa == '':
                st.error('Please enter some text')
            else:
                with st.spinner('Wait for it...'):
                    time.sleep(2)
                    translator = GoogleTranslator()
                    mid = translator.translate(input_pa, dest="fr")
                    mid2 = translator.translate(mid, dest="de")
                    back = translator.translate(mid2, dest="en")
                    
                    if back:  # Check if back translation is not empty
                        st.markdown('___')
                        st.write('Back Translation Model')
                        st.success(back)
                        st.balloons()
                    else:
                        st.error('Translation failed, please try again.')

#ANALYZE
      
if nav == 'Analyze text':
    st.markdown("<h4 style='text-align: center; color:grey;'>Accelerate knowledge with SYNTHIA &#129302;</h4>", unsafe_allow_html=True)
    st.text('')
    p_title('Analyze text')
    st.text('')
    
    a_example = "Artificial intelligence (AI) is intelligence demonstrated by machines, as opposed to the natural intelligence displayed by humans or animals. Leading AI textbooks define the field as the study of 'intelligent agents': any system that perceives its environment and takes actions that maximize its chance of achieving its goals. Some popular accounts use the term 'artificial intelligence' to describe machines that mimic cognitive functions that humans associate with the human mind, such as learning and problem solving, however this definition is rejected by major AI researchers. AI applications include advanced web search engines, recommendation systems (used by YouTube, Amazon and Netflix), understanding human speech (such as Siri or Alexa), self-driving cars (such as Tesla), and competing at the highest level in strategic game systems (such as chess and Go). As machines become increasingly capable, tasks considered to require intelligence are often removed from the definition of AI, a phenomenon known as the AI effect. For instance, optical character recognition is frequently excluded from things considered to be AI, having become a routine technology."

    source = st.radio("How would you like to start? Choose an option below",
                          ("I want to input some text", "I want to upload a file"))
    st.text('')

    if source == 'I want to input some text':
        input_me = st.text_area("Use the example below or input your own text in English (maximum of 10,000 characters)", max_chars=10000, value=a_example, height=330)
        if st.button('Analyze'):
            if len(input_me) > 10000:
                st.error('Please enter a text in English of maximum 1,000 characters')
            else:
                with st.spinner('Processing...'):
                    time.sleep(2)
                    nltk.download('punkt')
                    rt = readtime.of_text(input_me)
                    tc = textstat.flesch_reading_ease(input_me)
                    tokenized_words = word_tokenize(input_me)
                    lr = len(set(tokenized_words)) / len(tokenized_words)
                    lr = round(lr,2)
                    n_s = textstat.sentence_count(input_me)
                    st.markdown('___')
                    st.text('Reading Time')
                    st.write(rt)
                    st.markdown('___')
                    st.text('Text Complexity: from 0 or negative (hard to read), to 100 or more (easy to read)')
                    st.write(tc)
                    st.markdown('___')
                    st.text('Lexical Richness (distinct words over total number of words)')
                    st.write(lr)
                    st.markdown('___')
                    st.text('Number of sentences')
                    st.write(n_s)
                    st.balloons()

    if source == 'I want to upload a file':
        file = st.file_uploader('Upload your file here',type=['txt'])
        if file is not None:
            with st.spinner('Processing...'):
                    time.sleep(2)
                    stringio = StringIO(file.getvalue().decode("utf-8"))
                    string_data = stringio.read()
                    if len(string_data) > 10000:
                        st.error('Please upload a file of maximum 10,000 characters')
                    else:
                        nltk.download('punkt')
                        rt = readtime.of_text(string_data)
                        tc = textstat.flesch_reading_ease(string_data)
                        tokenized_words = word_tokenize(string_data)
                        lr = len(set(tokenized_words)) / len(tokenized_words)
                        lr = round(lr,2)
                        n_s = textstat.sentence_count(string_data)
                        st.markdown('___')
                        st.text('Reading Time')
                        st.write(rt)
                        st.markdown('___')
                        st.text('Text Complexity: from 0 or negative (hard to read), to 100 or more (easy to read)')
                        st.write(tc)
                        st.markdown('___')
                        st.text('Lexical Richness (distinct words over total number of words)')
                        st.write(lr)
                        st.markdown('___')
                        st.text('Number of sentences')
                        st.write(n_s)
                        st.balloons()
