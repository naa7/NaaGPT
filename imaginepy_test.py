from imaginepy import Imagine, Style, Ratio
from PIL import Image

def main():
    imagine = Imagine()
    description = input("Enter image description: ")
    print ('\033[1A\033[K', end='\r')
    print("Generating image...", end='\r')
    img_data = imagine.sdprem(
        prompt=description,
        style=Style.ANIME_V2,
        ratio=Ratio.RATIO_16X9
    )

    if img_data is None:
        print("An error occurred while generating the image.")
        return

    try:
        with open("example.png", mode="wb") as img_file:
            img_file.write(img_data)
        img = Image.open("example.png")
        img.show()
    except Exception as e:
        print(f"An error occurred while writing the image to file: {e}")

if __name__ == "__main__":
    main()
