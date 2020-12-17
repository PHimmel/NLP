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