import qrcode


def generate(url, add="/start"):
    img = qrcode.make(url + add)
    print("Generating QR Code...")
    img.show()
