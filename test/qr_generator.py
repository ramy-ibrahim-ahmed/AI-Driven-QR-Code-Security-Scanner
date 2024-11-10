import qrcode


def generate_qr_codes(urls):
    for index, url in enumerate(urls):
        # Create a QR code object for each URL
        qr = qrcode.QRCode(
            version=1,  # Controls the size of the QR code (1 is the smallest).
            error_correction=qrcode.constants.ERROR_CORRECT_L,  # Error correction level.
            box_size=10,  # Size of each box in the QR code grid.
            border=4,  # Thickness of the border.
        )

        # Add the URL to the QR code
        qr.add_data(url)
        qr.make(fit=True)

        # Create an image of the QR code
        img = qr.make_image(fill="black", back_color="white")

        # Save the image to a file with a unique name
        img_filename = f"qrcode_{index + 1}.png"
        img.save(img_filename)

        print(f"QR code for {url} saved as '{img_filename}'.")


# List of URLs to generate QR codes for
urls_list = [
    "https://www.stubhub.com/jon-faddis-jazz-orchestra-tickets/", # benign
    "http://atel.se/wp-includes/SimplePie/Count/be7baa518d258efbb611498d0af83455/", # malware
]

# Call the function with the list of URLs
generate_qr_codes(urls_list)
