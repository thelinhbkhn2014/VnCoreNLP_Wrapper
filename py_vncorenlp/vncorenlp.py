import jnius_config
import os
import shutil


def download_model(save_dir='./'):
    # current_path = os.path.abspath(os.getcwd())
    if save_dir[-1] == '/':
        save_dir = save_dir[:-1]
    if os.path.isdir(save_dir + "/models") and os.path.exists(save_dir + '/VnCoreNLP-1.2.jar'):
        print("VnCoreNLP model folder " + save_dir + " already exists! Please load VnCoreNLP from this folder!")
    else:
        os.mkdir(save_dir + "/models")
        os.mkdir(save_dir + "/models/dep")
        os.mkdir(save_dir + "/models/ner")
        os.mkdir(save_dir + "/models/postagger")
        os.mkdir(save_dir + "/models/wordsegmenter")
        # jar
        os.system("wget https://raw.githubusercontent.com/vncorenlp/VnCoreNLP/master/VnCoreNLP-1.2.jar")
        shutil.move("VnCoreNLP-1.2.jar", save_dir + "/VnCoreNLP-1.2.jar")
        # wordsegmenter
        os.system("wget https://raw.githubusercontent.com/vncorenlp/VnCoreNLP/master/models/wordsegmenter/vi-vocab")
        os.system(
            "wget https://raw.githubusercontent.com/vncorenlp/VnCoreNLP/master/models/wordsegmenter/wordsegmenter.rdr")
        shutil.move("vi-vocab", save_dir + "/models/wordsegmenter/vi-vocab")
        shutil.move("wordsegmenter.rdr", save_dir + "/models/wordsegmenter/wordsegmenter.rdr")
        # postagger
        os.system("wget https://raw.githubusercontent.com/vncorenlp/VnCoreNLP/master/models/postagger/vi-tagger")
        shutil.move("vi-tagger", save_dir + "/models/postagger/vi-tagger")
        # ner
        os.system("wget https://raw.githubusercontent.com/vncorenlp/VnCoreNLP/master/models/ner/vi-500brownclusters.xz")
        os.system("wget https://raw.githubusercontent.com/vncorenlp/VnCoreNLP/master/models/ner/vi-ner.xz")
        os.system(
            "wget https://raw.githubusercontent.com/vncorenlp/VnCoreNLP/master/models/ner/vi-pretrainedembeddings.xz")
        shutil.move("vi-500brownclusters.xz", save_dir + "/models/ner/vi-500brownclusters.xz")
        shutil.move("vi-ner.xz", save_dir + "/models/ner/vi-ner.xz")
        shutil.move("vi-pretrainedembeddings.xz", save_dir + "/models/ner/vi-pretrainedembeddings.xz")
        # parse
        os.system("wget https://raw.githubusercontent.com/vncorenlp/VnCoreNLP/master/models/dep/vi-dep.xz")
        shutil.move("vi-dep.xz", save_dir + "/models/dep/vi-dep.xz")


class VnCoreNLP:
    def __init__(self, max_heap_size='-Xmx2g', annotators=["wseg", "pos", "ner", "parse"], save_dir = './'):
        if save_dir[-1] == '/':
            save_dir = save_dir[:-1]
        if os.path.isdir(save_dir + "/models") == False or os.path.exists(save_dir + '/VnCoreNLP-1.2.jar') == False:
            raise Exception("Please download the VnCoreNLP model!")
        jnius_config.add_options(max_heap_size)
        self.current_working_dir = os.getcwd()
        os.chdir(save_dir)
        jnius_config.set_classpath(save_dir + "/VnCoreNLP-1.2.jar")
        from jnius import autoclass
        javaclass_vncorenlp = autoclass('vn.pipeline.VnCoreNLP')
        self.javaclass_String = autoclass('java.lang.String')
        self.annotators = annotators
        if "wseg" not in annotators:
            self.annotators.append("wseg")

        self.model = javaclass_vncorenlp(annotators)

    def annotate_text(self, text):
        from jnius import autoclass
        javaclass_Annotation = autoclass('vn.pipeline.Annotation')
        str = self.javaclass_String(text)
        annotation = javaclass_Annotation(str)
        self.model.annotate(annotation)
        dict_sentences = {}
        list_sentences = annotation.toString().split("\n\n")[:-1]
        for i in range(len(list_sentences)):
            list_words = list_sentences[i].split("\n")
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
            dict_sentences[i] = list_dict_words
        return dict_sentences

    def word_segment(self, text):
        from jnius import autoclass
        javaclass_Annotation = autoclass('vn.pipeline.Annotation')
        str = self.javaclass_String(text)
        annotation = javaclass_Annotation(str)
        self.model.annotate(annotation)
        list_segmented_sentences = []
        list_sentences = annotation.toString().split("\n\n")[:-1]
        for sent in list_sentences:
            list_words = sent.split("\n")
            list_segmented_words = []
            for word in list_words:
                word = word.replace("\t\t", "\t")
                list_tags = word.split("\t")
                list_segmented_words.append(list_tags[1])
            list_segmented_sentences.append(" ".join(list_segmented_words))
        return list_segmented_sentences

    def print_out(self, dict_sentences):
        for sent in dict_sentences.keys():
            list_dict_words = dict_sentences[sent]
            for word in list_dict_words:
                print(str(word["index"]) + "\t" + word["wordForm"] + "\t" + word["posTag"] + "\t" + word["nerLabel"] + "\t" + str(word["head"]) + "\t" + word["depLabel"])
            print("")

    def annotate_file(self, input_file, output_file):
        os.chdir(self.current_working_dir)
        input_str = self.javaclass_String(input_file)
        output_str = self.javaclass_String(output_file)
        self.model.processPipeline(input_str, output_str, self.annotators)

if __name__ == '__main__':
    download_model(save_dir='/home/vinai/Desktop/testvncore')
    model = VnCoreNLP(annotators=["wseg"], save_dir='/home/vinai/Desktop/testvncore')
    output = model.annotate_text("Ông Nguyễn Khắc Chúc  đang làm việc tại Đại học Quốc gia Hà Nội. Bà Lan, vợ ông Chúc, cũng làm việc tại đây.")
    print(output)
    model.print_out(output)
    model.annotate_file(input_file="/home/vinai/Desktop/testvncore/t/input.txt", output_file="output.txt")
    print(model.word_segment("Ông Nguyễn Khắc Chúc  đang làm việc tại Đại học Quốc gia Hà Nội."))