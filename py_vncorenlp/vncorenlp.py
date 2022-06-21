import jnius_config
import os
import shutil


def download_model():
    if os.path.isdir("./models") == False:
        os.mkdir("./models")
        os.mkdir("./models/dep")
        os.mkdir("./models/ner")
        os.mkdir("./models/postagger")
        os.mkdir("./models/wordsegmenter")
        os.system("wget https://raw.githubusercontent.com/vncorenlp/VnCoreNLP/master/VnCoreNLP-1.1.1.jar")
        # wordsegmenter
        os.system("wget https://raw.githubusercontent.com/vncorenlp/VnCoreNLP/master/models/wordsegmenter/vi-vocab")
        os.system(
            "wget https://raw.githubusercontent.com/vncorenlp/VnCoreNLP/master/models/wordsegmenter/wordsegmenter.rdr")
        shutil.move("vi-vocab", "./models/wordsegmenter/vi-vocab")
        shutil.move("wordsegmenter.rdr", "./models/wordsegmenter/wordsegmenter.rdr")
        # postagger
        os.system("wget https://raw.githubusercontent.com/vncorenlp/VnCoreNLP/master/models/postagger/vi-tagger")
        shutil.move("vi-tagger", "./models/postagger/vi-tagger")
        # ner
        os.system("wget https://raw.githubusercontent.com/vncorenlp/VnCoreNLP/master/models/ner/vi-500brownclusters.xz")
        os.system("wget https://raw.githubusercontent.com/vncorenlp/VnCoreNLP/master/models/ner/vi-ner.xz")
        os.system(
            "wget https://raw.githubusercontent.com/vncorenlp/VnCoreNLP/master/models/ner/vi-pretrainedembeddings.xz")
        shutil.move("vi-500brownclusters.xz", "./models/ner/vi-500brownclusters.xz")
        shutil.move("vi-ner.xz", "./models/ner/vi-ner.xz")
        shutil.move("vi-pretrainedembeddings.xz", "./models/ner/vi-pretrainedembeddings.xz")
        # parse
        os.system("wget https://raw.githubusercontent.com/vncorenlp/VnCoreNLP/master/models/dep/vi-dep.xz")
        shutil.move("vi-dep.xz", "./models/dep/vi-dep.xz")
    else:
        print("The VnCoreNLP model is already!")


class VnCoreNLP:
    def __init__(self, max_heap_size='-Xmx2g', annotators=["wseg", "pos", "ner", "parse"]):
        if os.path.isdir("./models") == False:
            raise Exception("Please download the VnCoreNLP model before initialization!")
        jnius_config.add_options(max_heap_size)
        jnius_config.set_classpath("./VnCoreNLP-1.1.1.jar")
        from jnius import autoclass
        javaclass_vncorenlp = autoclass('vn.pipeline.VnCoreNLP')
        self.javaclass_String = autoclass('java.lang.String')
        self.annotators = annotators
        if "wseg" not in annotators:
            self.annotators.append("wseg")
        self.model = javaclass_vncorenlp(annotators)

    def annotate_sentence(self, sentence):
        from jnius import autoclass
        javaclass_Annotation = autoclass('vn.pipeline.Annotation')
        str = self.javaclass_String(sentence)
        annotation = javaclass_Annotation(str)
        self.model.annotate(annotation)
        output = annotation.toString().replace("\n\n", "")
        list_words = output.split("\n")
        list_dict_words = []
        for word in list_words:
            dict_word = {}
            word = word.replace("\t\t", "\t")
            list_tags = word.split("\t")
            dict_word["index"] = int(list_tags[0])
            dict_word["wordForm"] = list_tags[1]
            dict_word["posTag"] = list_tags[2]
            dict_word["nerLabel"] = list_tags[3]
            if "parse" in self.annotators:
                dict_word["head"] = int(list_tags[4])
            else:
                dict_word["head"] = list_tags[4]
            dict_word["depLabel"] = list_tags[5]
            list_dict_words.append(dict_word)
        return list_dict_words

    def tokenize(self, sentence):
        from jnius import autoclass
        javaclass_Annotation = autoclass('vn.pipeline.Annotation')
        str = self.javaclass_String(sentence)
        annotation = javaclass_Annotation(str)
        self.model.annotate(annotation)
        output = annotation.toString().replace("\n\n", "")
        list_words = output.split("\n")
        list_segmented_words = []
        for word in list_words:
            word = word.replace("\t\t", "\t")
            list_tags = word.split("\t")
            list_segmented_words.append(list_tags[1])
        return " ".join(list_segmented_words)

    def print_out(self, list_dict_words):
        for word in list_dict_words:
            print(str(word["index"]) + "\t" + word["wordForm"] + "\t" + word["posTag"] + "\t" + word["nerLabel"] + "\t" + str(word["head"]) + "\t" + word["depLabel"])

    def annotate_file(self, input_file, output_file):
        input_str = self.javaclass_String(input_file)
        output_str = self.javaclass_String(output_file)
        self.model.processPipeline(input_str, output_str, self.annotators)

if __name__ == '__main__':
    download_model()
    model = VnCoreNLP(annotators=["wseg"])
    output = model.tokenize("Ông Nguyễn Khắc Chúc  đang làm việc tại Đại học Quốc gia Hà Nội.")
    print(output)
    model.annotate_file(input_file="/home/vinai/Desktop/testvncore/input.txt", output_file="/home/vinai/Desktop/testvncore/output.txt")
