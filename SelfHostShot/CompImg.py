from PIL import Image, ImageChops

# 비교할 두 이미지 파일 경로
img1_path = "../Shots/temp/20230408_1723_9.png"
img2_path = "../Shots/temp/20230408_1723_1.png"

# 이미지 열기
img1 = Image.open(img1_path)
img2 = Image.open(img2_path)

# 이미지 비교
diff = ImageChops.difference(img1, img2)

# 두 이미지가 같은지 다른지 구분
if diff.getbbox():
    print("두 이미지는 다릅니다.")
else:
    print("두 이미지는 같습니다.")