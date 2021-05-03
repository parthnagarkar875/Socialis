brand = 'facebook'
TRACK_WORDS = [f'{brand}']
TABLE_NAME = f"{brand}"
TABLE_ATTRIBUTES = "id_str VARCHAR(255), created_at TIMESTAMP, text TEXT, \
            polarity INT, named_ent TEXT, users_list TEXT, user_location TEXT"
java_path = "/usr/bin/java"
model_path = "/home/unmodern/Parth/Stanford NER files/stanford-ner-2020-11-17/classifiers/english.all.3class.distsim.crf.ser.gz"
ner_java_path = "/home/unmodern/Parth/Stanford NER files/stanford-ner-2020-11-17/stanford-ner.jar"

