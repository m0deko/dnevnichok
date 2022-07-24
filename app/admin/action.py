def txt_check(filename):
    ext = filename.rsplit('.', 1)[1]
    if ext == "txt" or ext == "TXT":
        return True
    return False