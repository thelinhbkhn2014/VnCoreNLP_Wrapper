#### Table of contents
1. [Prerequisites](#prerequisites)
2. [Installation](#install)
3. [Usage for Python users](#python)

# py_vncorenlp: A Python Wrapper for [VnCoreNLP](https://github.com/vncorenlp/VnCoreNLP)

## Prerequisites <a name="prerequisites"></a>

- Java 1.8+ ([JRE](http://www.oracle.com/technetwork/java/javase/downloads/jre8-downloads-2133155.html) or [JDK](http://www.oracle.com/technetwork/java/javase/downloads/jdk8-downloads-2133151.html))
## Installation <a name="install"></a>

- To install this python wrapper for VnCoreNLP, users have to run the following command:

    `$ pip install py_vncorenlp` 

## Example usage <a name="example"></a>

```python
import py_vncorenlp

# Automatically download the VnCoreNLP model from the original resitory
py_vncorenlp.download_model()

# Load the pretrained VnCoreNLP model
model = py_vncorenlp.VnCoreNLP(annotators=["wseg", "pos", "ner", "parse"])

# Annotate a corpus where each line represents a raw sentence
model.annotate_file(input_file="input.txt", output_file="output.txt")

# Annotate a raw sentence
model.print_out(model.annotate_sentence("Ông Nguyễn Khắc Chúc  đang làm việc tại Đại học Quốc gia Hà Nội.")
```

By default, the output for each input sentence is formatted with 6 columns representing word index, word form, POS tag, NER label, head index of the current word and its dependency relation type:

```
1       Ông     Nc      O       4       sub
2       Nguyễn_Khắc_Chúc        Np      B-PER   1       nmod
3       đang    R       O       4       adv
4       làm_việc        V       O       0       root
5       tại     E       O       4       loc
6       Đại_học N       B-ORG   5       pob
7       Quốc_gia        N       I-ORG   6       nmod
8       Hà_Nội  Np      I-ORG   6       nmod
9       .       CH      O       4       punct
```

In addition, to be convenient for users who use only the VnCoreNLP for the word segmentation, we also provide a function only for this:

```python
sentence = "Ông Nguyễn Khắc Chúc  đang làm việc tại Đại học Quốc gia Hà Nội."
output = model.tokenize(sentence)
print(output)
# The result: "Ông Nguyễn_Khắc_Chúc đang làm_việc tại Đại_học Quốc_gia Hà_Nội ."
```
