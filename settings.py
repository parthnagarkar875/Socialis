TRACK_WORDS = ['Facebook']
TABLE_NAME = "Facebook"
TABLE_ATTRIBUTES = "id_str VARCHAR(255), created_at DATETIME, text VARCHAR(255), \
            polarity INT, subjectivity INT, named_ent VARCHAR (255), users_list VARCHAR(255), user_created_at VARCHAR(255), user_location VARCHAR(255), \
            user_description VARCHAR(255), user_followers_count INT, longitude DOUBLE, latitude DOUBLE, \
            retweet_count INT, favorite_count INT"
java_path = "C:/Program Files/Java/jdk1.8.0_131/bin/java.exe"
model_path="D:/Parth/Downloads/Stanford NER files/stanford-ner-2020-11-17/classifiers/english.all.3class.distsim.crf.ser.gz"
ner_java_path="D:/Parth/Downloads/Stanford NER files/stanford-ner-2020-11-17/stanford-ner.jar"