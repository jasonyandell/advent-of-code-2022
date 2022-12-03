def read_data(file):
    txt_file = open(f"{file}", "r")
    file_content = txt_file.read()
    txt_file.close()
    return file_content
