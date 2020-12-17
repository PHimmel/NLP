def main():

    indeed_file = ExtractTextFromFile(ExtractTextFromFile.indeed_posts)#, to_remove=ExtractTextFromFile.newline_removal)
    removed_control = indeed_file.open_file_read_data_remove_garbage()
    filtered_indeed = PrintInterface(removed_control)
    filtered_indeed.print_text()
    print(indeed_file.remove_trash_from_string())

if __name__ == '__main__':
	print('Main\n')
	# main()
	print('\nTermination')
else:
	print('Imported')