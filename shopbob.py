import csv
import bs4 as bs
from urllib.request import urlopen, Request 

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}

product_count = 0
brand_count = 0

reg_url = 'https://www.shopbop.com/actions/designerindex/viewAlphabeticalDesigners.action'
req = Request(url = reg_url,headers = headers)
source1 = urlopen(req).read()
soup = bs.BeautifulSoup(source1,'lxml')

csv_file = open('shopbob.csv','w',encoding="utf-8")
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['Product Name','Product Price','Product Color','Product Number','Image link','Product Size','Description'])

for an in soup.find_all('div',class_='group'): #link to designer(say brands)
    for link in an.find_all('a'):
        link = link.get('href')
        #print(link)

        des_url1 = 'https://www.shopbop.com'+link
        des_req1 = Request(url = des_url1,headers = headers)
        des_source = urlopen(des_req1).read()
        des_soup1 = bs.BeautifulSoup(des_source,'lxml')

        for everyitem in des_soup1.find_all('a',class_='url'):    #designer page items(say products)
            item = everyitem.get('href')
            item_url = 'https://www.shopbop.com'+item
            item_req = Request(url = item_url,headers = headers)
            itemsource = urlopen(item_req).read()
            itemsoup = bs.BeautifulSoup(itemsource,'lxml')
            #print(item_url)

            for product_name in itemsoup.find_all('div',id = 'product-title'):
                product_name = product_name.text
                print(product_name)

            for product_price in itemsoup.find_all('span',class_='pdp-price'):
                product_price = product_price.text
                print(product_price)

            for product_color in itemsoup.find_all('span',class_='selectedColorLabel'):
                color = []
                product_color = product_color.text
                color.append(product_color)
                print(color)

            for product_number in itemsoup.find_all('span',itemprop = 'sku'):
                product_number = product_number.text
                print(product_number)

            for product_image_link in itemsoup.find_all('img',class_ = 'display-image'):
                image = []
                product_image_link = product_image_link.get('src')
                image.append(product_image_link)
                print(product_image_link)

            for product_size in itemsoup.find_all('div',class_ = 'sizeBox'):
                size = []
                product_size = product_size.text
                size.append(product_size)
                print(size)

            for product_description in itemsoup.find_all('div',id='product-details'):
                des = []
                for description in product_description.find_all('li'):
                    description = description.text
                    des.append(description)
                print(des)

            csv_writer.writerow([product_name,product_price,color,product_number,image,size,des])
            product_count += 1
            if product_count == 60:
                break

        brand_count += 1
        if brand_count == 20:
            break

csv_file.close()
