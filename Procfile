worker: python -m spacy download en_core_web_sm && python -m nltk.downloader punkt maxent_ne_chunker averaged_perceptron_tagger words && python scraper.py
web: sh setup.sh && python -m nltk.downloader stopwords && python -m spacy download en_core_web_sm && streamlit run app.py

