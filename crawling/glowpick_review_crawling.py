def crawling():
    
    total  = []

#     웹페이지 안띄우기
#     chrome_options = webdriver.ChromeOptions()
#     chrome_options.add_argument("headless")
#     chrome_options.add_argument('--disable-gpu')
#     chrome_options.add_argument('lang=ko_KR')
    
#    driver = webdriver.Chrome(chrome_options=chrome_options)    

    driver = webdriver.Chrome()     
    
    driver.set_window_size(700, 1400)
    
    for i in range(1, 6):
        print(i)
        url = f'https://www.glowpick.com/product/{links[i]}'
        driver.get(url)
        
        try :
            driver.find_element_by_css_selector(".error-layout__subtitle") == '오류코드: 500'
            print('pass')
            pass
        
        except :

            p = 0

            if int(driver.find_element_by_css_selector('.section-list-score__rating-item.joiner')
                   .text.replace('총 ',"").replace('명',"").replace(',', "")) >= 5:

                while p < 5:

                    # 스크롤 제일 마지막 아래 대상 선택
                    ELEMENT = driver.find_elements_by_css_selector('.review-list-item')[-2]
                    time.sleep(1)

                    # ELEMENT 가 화면에 보이도록 스크롤 조정 --> 아래 부분 추가로 확장됨
                    driver.execute_script("arguments[0].scrollIntoView(true);", ELEMENT)        
                    p = p + 1
                    time.sleep(1)

                    # 스크롤 제일 마지막 아래 대상 선택
                    ELEMENT = driver.find_elements_by_css_selector('.review-list-item')[-5]
                    time.sleep(1)

                    # ELEMENT 가 화면에 보이도록 스크롤 조정 --> 아래 부분 추가로 확장됨
                    driver.execute_script("arguments[0].scrollIntoView(true);", ELEMENT)

            else:
                 while p < 2:

                    # 스크롤 제일 마지막 아래 대상 선택
                    ELEMENT = driver.find_elements_by_css_selector('.list-item')[-5]
                    time.sleep(0.5)

                    # ELEMENT 가 화면에 보이도록 스크롤 조정 --> 아래 부분 추가로 확장됨
                    driver.execute_script("arguments[0].scrollIntoView(true);", ELEMENT)        
                    p = p + 1
                    time.sleep(0.5)


            user, age, skin, gender, score, review = [], [], [], [], [], []
                    
            total_reviews = driver.find_elements_by_xpath('//li[@class="review-list-item"]')

            req = driver.page_source
            soup = BeautifulSoup(req, 'html.parser')
            user_gender = soup.select('.txt .icon-sprite')
            user_like = soup.select('.label .icon-sprite')

            #제품명
            item = driver.find_element_by_xpath('//*[@id="gp-default-main"]/section/div/ul[1]/li[2]/section[1]/h1/span').text

            #회사명
            company = driver.find_element_by_xpath('//*[@id="gp-default-main"]/section/div/ul[1]/li[2]/section[1]/p').text

            #용량
            size = driver.find_element_by_xpath('//*[@id="gp-default-main"]/section/div/ul[1]/li[2]/section[1]/div[2]/div[1]').text.split(' / ')[0]

            #가격
            price = driver.find_element_by_xpath('//*[@id="gp-default-main"]/section/div/ul[1]/li[2]/section[1]/div[2]/div[1]').text.split(' / ')[1]


            for i in range(len(total_reviews)):

                #사용자 id
                user_id = total_reviews[i].text.split('·')[0].split('\n')[1]
                user.append(user_id)

                #사용자 나이
                user_age = total_reviews[i].text.split('·')[0].split('\n')[2]
                age.append(user_age)

                #피부 타입
                user_skin = total_reviews[i].text.split('·')[1]
                skin.append(user_skin)

                #사용자 평점
                user_like1 = user_like[i]['class'][2].replace('gpa-', '').replace('-small', '')
                if user_like1 == 'best':
                    user_like1 = 5
                elif user_like1 == 'good':
                    user_like1 = 4
                elif user_like1 == 'soso':
                    user_like1 = 3
                elif user_like1 == 'bad':
                    user_like1 = 2
                else :
                    user_like1 = 1
                score.append(user_like1)

                #사용자 후기
                user_review = total_reviews[i].text.split('·')[2].replace('\n', '')
                review.append(user_review)

            #사용자 성별
            for i in range(0, len(user_gender),2):
                if user_gender[i]['class'][0] == 'evaluation' or user_gender[i]['class'][0] == 'ranked':
                    pass

                else:
                    user_gender1 = user_gender[i]['class'][1].replace('icon-gender-', '')
                    if user_gender1 == 'f':
                        user_gender1='여성'
                    else:
                        user_gender1='남성'
                    gender.append(user_gender1)

            data = pd.DataFrame({
                            'item' : item,
                            'company' : company,
                            'size' : size,
                            'price' : price,
                            'id' : user,
                            'gender': gender,
                            'age' : age,
                            'skin' : skin,
                            'score': score,
                            'review' : review
                        })

            total.append(data)
    result = pd.concat(total)
    
    driver.quit()
    
    return result
