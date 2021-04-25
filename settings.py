TRACK_WORDS = ['Facebook']
TABLE_NAME = "Facebook"
TABLE_ATTRIBUTES = "id_str VARCHAR(255), created_at TIMESTAMP, text TEXT, \
            polarity INT, named_ent VARCHAR (255), users_list VARCHAR(255),user_location VARCHAR(255)"
java_path = "/usr/bin/java"
model_path="/home/unmodern/Parth/Stanford NER files/stanford-ner-2020-11-17/classifiers/english.all.3class.distsim.crf.ser.gz"
ner_java_path="/home/unmodern/Parth/Stanford NER files/stanford-ner-2020-11-17/stanford-ner.jar"