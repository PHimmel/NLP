"""

This applications(more specifically, this tool-kit) purpose is:

    1. consolidation of certain natural language analytics libraries

    2. provide a uniformed interface to access the operations available from said libraries
       as well to access their resultant values

    3. aside from the high level text manipulation offered by those modules - there is also
       the basic, fundamental functionality present that pre-processes the text before it
       can be utilized by those high-level tools. This being:

            a. conversion of string input into lists of both its sentences and its words
            b. todo --> offer the removal of punctuation and stopwords to filter its contents
            c. convert the input to TextBlob(text analysis module build off of NLTK library) object
            d. provide the interface to operate on the new object types received from the start
               input, as well as the ability to return it as is, or in any of its other forms
I/O:

    Input:

        required: a raw, unadulterated string of text (can be text in other type but will be converted to str first)

        optional arguments:
            1. to lower the case of the input in the pre-processing stage add - lower=True - as a parameter
                when instantiating via either of the abstract interfaces

    Output:

        (variable depending on selected functions)
        1. specific information about the input text derived from the programs operations

        2. the input converted into other object-types as well as their corresponding
           differing representations of said input

Program structure:

    Two main interface classes are used as primary access points:

        1. TextInterface
        2. PrintTextInterface

    TextInterface - the primary abstract class for utilizing the program. It has no base class and
        delegates its requests to its instance attributes that are objects of classes within the
        implementation layer

    PrintTextInterface - inherits from TextInterface and it only extends functionality by possessing
        methods to console-print the return values from its parent(TextInterface) class.

    There are four classes that comprise the implementation layer:

        1. Text - base class of:

            2. WordAnalysis

            3. SentenceAnalysis

        4. TextProcessing

    1. Text - verifies that the input is str-type, if it is not - Text() converts it to str-type in its init stage
        - maintains the str-type input in its unmodified form - provides basic, general functionality for text
        processing:
            if the 'lower' parameter is entered as True, it will change the total input case to case-fold (i.e. lower)
            before any further processing is done
        todo expand on this - has attributes that are the results of those broad text modifications
        todo add the ability to initiate its subclasses depending on presence of Text manipulated variables
        its subclasses extents those basic abilities and add:

        2. WordAnalysis - a word tokenized attribute
        3. SentenceAnalysis - a sentence tokenized attribute

    4. TextProcessing - this class receives requests from clients that have already been preprocessed
        (Text and its subclass objects) and are in a format that can be utilized by this class for analysis

        offers additional parameterized methods that take another TextProcessing object as its argument - this
        is used for insight into the comparison of properties of 2 differing text items

todo - see prior todo that will alter the flow to create Text object !first! then subclass objects
Program flow:

    The respective interface takes the input arguments, and then:

        (flow to access implementation layer and produce the desired result)

        1. creates objects of both WordAnalysis and SentenceAnalysis (which generates 2 base Text objects
            through their initialization, the Text class shields its subclasses from receiving non str-type input)

        2. after the pre-processing completed in WordAnalysis and SentenceAnalysis, respective objects
            are generated of the TextProcessing class - depending on if an operation request was
            made on the interface layer to said class (TextProcessing is where most of the logic is)

        (return flow carrying manipulated data)

        1. the value is not copied nor passed directly out of the TextProcessing class - rather it is accessed
            through the class that made the request(WordAnalysis/SentenceAnalysis - they each hold an object
            reference to the TextProcessing class)

        2. the value is only accessed indirectly within the interface layer by referring through those attribute
            references, as it is invoking the actual request - whilst being 2 objects removed from the direct request

How to use this module:

    refer to the two interfaces of the 'Program Structure' section for most use-cases

    only access the implementation layer if altered functionality is required
        - if working within this layer and get lost, each class contains a descriptive __repr__ to help guide you

"""
from textblob import TextBlob
import nltk
import re

"""
TODO make sure that various input types are compatible 
"""


class TextProcessing(object):

    def __init__(self, text):
        self.text = text

    def __repr__(self):
        return 'TextProcessing(input type = {})'.format(type(self.text))

    def __str__(self):
        return 'An object for manipulating text.'

    def __sub__(self):
        pass

    def freq_dist(self):
        return nltk.FreqDist(self.text)

    def count(self):
        return len(self.text)

    def length(self):
        total_character_length = 0

        for item in self.text:
            length = len(item)
            total_character_length += length

        return total_character_length

    def rounded_average(self):
        return round(self.length() / self.count(), 2)

    @staticmethod
    def first_comparison_return(difference):
        return 'The first input parameter attribute is %.2f greater than the seconds.' % difference

    @staticmethod
    def second_comparison_return(difference):
        return 'The second input parameter attribute is %.2f greater than the firsts.' % difference

    def comparison_output_logic(self, difference):

        if difference < 0:
            difference = abs(difference)
            return self.second_comparison_return(difference)

        else:
            return self.first_comparison_return(difference)

    def compare_counts(self, other):

        difference = self.count() - other.count()
        return self.comparison_output_logic(difference)

    def compare_lengths(self, other):

        difference = self.length() - other.length()
        return self.comparison_output_logic(difference)

    def compare_averages(self, other):

        difference = self.rounded_average() - other.rounded_average()
        return self.comparison_output_logic(difference)


"""
CONVERTS INPUT TEXT TYPE TO *STR*

AFFECTS ALL SUBCLASSES, ALL SELF.TEXT IS A *STR*

instigates basic text manipulation that cascades to its subclasses and ultimately to its final processed form
"""


class Text(object):

    def __init__(self, text, lower=False):
        self.text = text
        self.type_check()
        if lower is True:
            self.lower()
        self.blob = TextBlob(self.text)

    """
    TODO PROBABLY DELETE THESE TWO CLASS METHODS
    
    Additional Text constructor method:
    
    initializes a Text object with the primary attribute of 'text' is in lower case format
    """

    @classmethod
    def lowercase(cls, text):
        str_text = cls.class_type_check(text)
        return Text(cls(str_text).lower())

    @classmethod
    def class_type_check(cls, text):
        if type(text) is not str:
            text = ' '.join(text)
            return text

    def __repr__(self):
        return 'Text(input-type = {}, \nsubclasses = {})'.format(type(self.text), Text.__subclasses__())

    def __str__(self):
        return 'A base-class object for basic text processing operations.'

    def type_check(self):
        if type(self.text) is not str:
            print('not a str', type(self.text))
            if type(self.text) is list:
                print('list')
                self.text = ' '.join(self.text)
            if type(self.text) is None:
                print('NoneType received at', self)
                self.text = ''
                return

    def lower(self):
        self.text = self.text.casefold()

    """
    Should these go into TP class?
    """

    def remove_punctuation(self):
        pass

    def remove_stopwords(self):
        pass

    def get_sentiment(self):
        return self.blob.sentiment


"""
class for producing sentences from text received from the Text class
"""


class SentenceAnalysis(Text):

    def __init__(self, text, lower):
        super().__init__(text, lower)

        self.sentences = self.make_sentences()
        self.text_processing = TextProcessing(self.sentences)

    def __repr__(self):
        return 'SentenceAnalysis({}, {}, \nSentenceAnalysis parent info = {})'.format(type(self.sentences),
                                                                                      repr(self.text_processing),
                                                                                      super().__repr__())

    def __str__(self):
        return 'An object for sentence analysis.'

    def make_sentences(self):
        sentences_split = self.text.split('.')
        return sentences_split


"""
class for producing words from text received from the Text class
"""


class WordAnalysis(Text):

    def __init__(self, text, lower):
        super().__init__(text, lower)

        self.words = self.make_words()
        self.text_processing = TextProcessing(self.words)

    def __repr__(self):
        return 'WordAnalysis({}, {}, \nWordAnalysis parent info = {})'.format(type(self.words),
                                                                              repr(self.text_processing),
                                                                              super().__repr__())

    def make_words(self):
        text_in_word_tokens = self.text.split()
        return text_in_word_tokens


"""
for both TextInterface and PrintInterface:

    if lower parameter is True, use lowercase text for analysis - default is False
"""


class TextInterface(object):
    def __init__(self, text, lower=False):
        self.text = text
        self.lower = lower
        self.sentence_analysis = SentenceAnalysis(self.text, self.lower)
        self.word_analysis = WordAnalysis(self.text, self.lower)

    def __repr__(self):
        return 'TextInterface(attributes = {}, {}, {})'.format(type(self.text), repr(self.word_analysis),
                                                               repr(self.sentence_analysis))

    def get_text(self):
        return self.sentence_analysis.text

    def get_sentences(self):
        return self.sentence_analysis.sentences

    def get_words(self):
        return self.word_analysis.words

    def average_word_length(self):
        average_length = self.sentence_analysis.text_processing.rounded_average() / \
                         self.word_analysis.text_processing.rounded_average()
        return average_length

    def average_sentence_length(self):
        return self.sentence_analysis.text_processing.rounded_average()

    def number_of_words(self):
        return self.word_analysis.text_processing.count()

    def number_of_sentences(self):
        return self.sentence_analysis.text_processing.count()

    def sentence_freq_dist(self):
        return self.sentence_analysis.text_processing.freq_dist()

    def word_freq_dist(self):
        return self.word_analysis.text_processing.freq_dist()


"""
PrintInterface - a subclass of TextInterface

simply adds the console-print function directly to the return value of its parent class
"""


class PrintInterface(TextInterface):

    def __init__(self, text, lower=False):
        super().__init__(text, lower)
        self.text = text
        self.lower = lower

    def __repr__(self):
        return 'PrintInterface(attributes : input-type = {}, lower = {}\nPrintInterface parent info = {})' \
            .format(type(self.text), self.lower, super().__repr__())

    def print_text(self):
        print(self.get_text())

    def print_words(self):
        print(self.get_words())

    def print_sentences(self):
        print(self.get_sentences())

    def print_average_word_length(self):
        print(self.average_sentence_length())

    def print_average_sentence_length(self):
        print(self.average_sentence_length())

    def print_sentence_freq_dist(self):
        print(self.sentence_freq_dist())

    def print_word_freq_dist(self):
        print(self.word_freq_dist())

    def print_sentence_sentiment(self):
        print(self.sentence_analysis.blob.sentiment)

    def print_word_sentiment(self):
        print(self.word_analysis.blob.sentiment)

    def print_sentence_count(self):
        print(self.number_of_sentences())

    def print_word_count(self):
        print(self.number_of_words())


"""
----------------------------------------------------------------------------------------------------------------------
ADDITIONAL FUNCTIONALITY STAGING AREA

NOT YET INCORPORATED INTO PROGRAM
"""


"""
this class: 
1. opens txt files on are within its directory/on its path
2. reads the data 
3. returns the text, either in its unmodified form or filtered by employing the parameter 'to_remove'
"""


class EnterTextIntoFile(object):

    def __init__(self, file, text):
        self.file = file
        self.text = text

    def __repr__(self):
        return 'EnterTextIntoFile({})'.format(self.file)

    def enter_data(self):
        print(repr(self.text))
        print(self)

        if not self.type_check(self.text):
            print('NoneType at', self)
            return

        # use 'w' to write over current contents, 'a' to append new data onto the file
        with open(self.file, 'a') as doc:

            doc.write(self.text)
            doc.close()
            print('Data entered into', self)

    @staticmethod
    def type_check(data):
        if data is None:
            return False
        return True


class ExtractTextFromFile(object):

    # these two class attributes are simply placeholders for the location to store meaningful, static values
    newline_removal = r'\n'
    indeed_posts = 'indeed_posts.txt'

    def __init__(self, file, to_remove=''):
        self.file = file
        self.to_remove = to_remove
        self.text = None

    def open_file_read_data_remove_garbage(self):
        if self.to_remove == '':
            no_arg = input('There will be no filtering the output text.\nIs that okay? Enter yes or no.\n')
            if 'no' in no_arg:
                raise ValueError('Add the \'to_remove\' parameter for removal, '
                                 'the current return would have been unmodified text')

        with open(self.file, 'r') as doc:
            doc_text = doc.read().replace(self.to_remove, '')
            doc.close()
            self.text = doc_text
        return self.text

    def remove_trash_from_string(self):
        return self.text.replace(self.to_remove, '')


class StringManipulation(object):
    regex_control_char_pattern = r'[\t\n\r\f]+'

    def __init__(self, string, filters=None):
        self.string = string
        self.filters = filters

        self.type_check()

    def type_check(self):

        if type(self.string) is not str:
            self.string = ''.join(self.string)

    def regex_search(self):
        pass

    """
    if no filters are specified, the default argument is to use the regex pattern to select for control characters
    """

    def regex_removal(self):
        if self.filters is None:
            self.filters = StringManipulation.regex_control_char_pattern
        removed = re.sub(self.filters, '', self.string)
        return removed

    def string_translation_removal(self):
        pass


def main():

    indeed_file = ExtractTextFromFile(ExtractTextFromFile.indeed_posts)#, to_remove=ExtractTextFromFile.newline_removal)
    removed_control = indeed_file.open_file_read_data_remove_garbage()
    filtered_indeed = PrintInterface(removed_control)
    filtered_indeed.print_text()
    print(indeed_file.remove_trash_from_string())


def type_testing():
    test = ['sddsdsSDDEdds dsdDDsd dsdsWDSWd.', 'sdFDsdd']
    # test = 'ssdsd'
    test_obj = TextInterface(test, lower=True)
    print(test_obj.get_words())
    print(test_obj.get_sentences())
    print(test_obj.get_text())
    print('\n')
    test_obj = TextInterface(test, lower=False)
    print(test_obj.get_words())
    print(test_obj.get_sentences())
    print(test_obj.get_text())
    #  additional = Text.lowercase(test)
    # print(additional.text)
    print('\n')
    print_test = PrintInterface(test, lower=True)
    print_test.print_words()
    print_test.print_text()
    print_test.print_sentences()
    print_test.print_sentence_freq_dist()
    print_test.print_word_freq_dist()

    print(print_test)


if __name__ == '__main__':
    print('Main\n')
    # main()
    print('\nTermination')
else:
    print('Imported')
