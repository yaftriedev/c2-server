# Counting IP occurrences in a file
def count_ip(ip, file):
    counter = 0
    with open(file, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if "," in line:
                if line.split(",")[0] == ip:
                    counter += 1
    return counter

# Upload text to a file with optional IP limit
def upload_text(text, ip, time, file="uploaded_text.txt", limit_ip=None):
    if not text or text.strip() == "":
        print(text)
        return

    if limit_ip is not None:
        if count_ip(ip, file) >= limit_ip:
            return
    
    with open(file, "a") as f:
        f.write(f"{ip}, {time}: {text}\n")

# Download file content
def download(file):
    try:
        with open(file, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return "Error 404: File not found."