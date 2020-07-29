# Actor Scrapper

Scrapping profile photo from FilmMakers, Megaphone korea.  
Scrapping keyword image from naver.

## Profile scrapper

run main.py

if error occur after creating csv file, run save_by_csv.py

## Keyword scrapper

run keyword_scrapper/naver.py

    python naver.py -name [keyword]

### Technology

keyword scrapper will scrapping keyword pictures from naver.  
Download original, Face cropped and Face cropped(gray) in separated directory.  
![image](https://user-images.githubusercontent.com/47638660/88817131-1b663880-d1f8-11ea-9566-30b20e94fb09.png)

### Data cleaning strategy

![image](https://user-images.githubusercontent.com/47638660/88817611-b101c800-d1f8-11ea-8c07-cb66c94694aa.png)
Other criterions like **brightness**, **color**, image **size** are under consideration
