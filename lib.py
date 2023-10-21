

def read_file(file_path):
    file = open(file_path, "r")
    content = file.read()
    file.close()
    return content
