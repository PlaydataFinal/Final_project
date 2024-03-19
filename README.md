# 유사도 기반 추천시스템
서비스 운영 전이라 Cold start issue가 있는 상황. 유저 정보나 선택 정보가 없어서 Collaborative Filtering을 적용하기 힘들다. Content-Based Filtering을 채택.

Ai Hub에서 여행 방문지, 경로 데이터를 발견하여 Collaborative Filtering이나 Hybrid 기법 적용을 고려했다. 다만 후술할 데이터 출처인 제주관광공사 홈페이지인 visitjeju의 데이터와 idx가 달라서 테이블 join 전처리의 어려움이 있었음. 여러 데이터 출처를 선택하기보단 visitjeju 홈페이지에서 크롤링해올 수 있는 데이터를 최대한 활용하기로 했다.

![image](https://github.com/PlaydataFinal/Final_project/assets/145752714/69652d49-93d6-4bfe-9008-ca439633f218)



좋아요, 별점, 리뷰 데이터와 해당 유저의 메타 데이터가 없는 상황에서 관광지 간 유사도를 얻을 수 있는 방법을 고민했다.
-> Contents에 대한 특징을 담고 있는 데이터를 백터화하여 백터 간 코사인 값을 계산하면 우리 추천시스템의 궁극적인 타겟 피쳐인 관광지 간 유사성을 도출할 수 있다고 생각했다.

![image](https://github.com/PlaydataFinal/Final_project/assets/145752714/0a474f48-b14c-42e9-8289-e8c4247a826d)



이는 Content-Based Filtering 중 임베딩 방식을 의미한다. Content-Based Filtering에는 이와 달리 One Hot Encoding 을 활용하는 방식이 있다. 관광지에 대한 여러 정보를 수집하여 columns으로 만들어 관광지에 대한 메타 데이터 테이블을 형성하고 One Hot Encoding을 통해 유사도를 계산하는 방식을 고안했었다. 하지만 메타 데이터 테이블의 colunm 하나를 만들기 위해 fancy한 모델을 찾고 성능을 체크해야 하는 것은 비효율적이라 판단되어서 해당 모델링은 기각되었다.

![image](https://github.com/PlaydataFinal/Final_project/assets/145752714/0a1e040f-e411-4921-817f-8a998864e3aa)




# 태그 유사도
insight
동백과 수국, 동백과 온천 중 전자가 더 유사하다. 이것을 아는 방법은 동백과 수국 태그를 동시에 가지고 있는 관광지가 후자보다 많다는 점만으로 태그 간 유사성을 시사할 수 있다.. 태그들이 특정 관광지라는 하나의 오브젝트로 묶임으로서 라벨이 생기는 느낌.
-> 태그 클러스터링, 태그 유사도 기반 추천시스템
-> 제주관광공사 홈페이지 visitjeju에서 제공하는 관광지별 태그 데이터 크롤링

![image](https://github.com/PlaydataFinal/Final_project/assets/145752714/961dded5-5459-4b5d-a036-d200e0ad0afd)




태그들을 TF-IDF 백터화 시키기

![image](https://github.com/PlaydataFinal/Final_project/assets/145752714/8e817da0-0f9f-4440-b9f3-65bc1acf3e41)



코사인 유사도를 계산 및 데이터프레임 얻기

![image](https://github.com/PlaydataFinal/Final_project/assets/145752714/04beb7da-fef6-4608-85ed-fc70e5b120dc)

![image](https://github.com/PlaydataFinal/Final_project/assets/145752714/bfaf6b77-2589-4f5f-b165-2ac511b2dbe4)

![image](https://github.com/PlaydataFinal/Final_project/assets/145752714/93c8f042-4b67-49b9-a319-21ac42a60949)



유사도 행렬을 사용하면 유저가 한 관광지를 골랐을 때 그와 비슷한 관광지를 추천해줄 수 있다.

![image](https://github.com/PlaydataFinal/Final_project/assets/145752714/45686885-8356-4f17-9a61-bb5e425f1ee8)



최종적으로 태그 유사도 추천시스템은 챗봇에 사용한 상세설명을 임베딩한 값과 함께
웹페이지 중 관광지 상세정보 페이지에서 해당 관광지와 유사한 3곳을 추천해주는 서비스로서 적용되었다.

![image](https://github.com/PlaydataFinal/Final_project/assets/145752714/128f74a6-0daf-40ff-a9c1-fe6264b1a98a)


ID는 웹 url 관광지마다 구분자임.(mysite/6103 -> 1100고지 설명페이지) 임베딩은 챗봇에 사용한 상세설명에서 핵심키워드 20개를 추출해서 임베딩한 값들이다. 추가로 저 태그 유사도를 사용하기위해 임베딩을 해서 유사도 검사시 사용할 때 상세설명 키워드 추출한 임베딩값과 태그 임베딩을 동시 사용하였다.

![image](https://github.com/PlaydataFinal/Final_project/assets/145752714/c644d2b3-8433-430b-9c11-a6fbfa52cde8)



관광지 상세설명간에 서로 유사한 관광지를 상위 40개 구함 > 이 40개 중에서 태그 임베딩값을 이용해서 가장 유사한 3개를 선택 > 이 3개에 해당하는 ID를 rec칼럼에 저장 하는 프로세스로 로직을 구성했다.

![image](https://github.com/PlaydataFinal/Final_project/assets/145752714/ba04be0c-9b71-4321-946a-215aff36b22d)




+태그 클러스터링도 시도했었는데 클러스터는 잘 나눠지는 것을 확인했다. 하지만 적절한 활용 방법을 생각하지 못해 서비스화시키지는 못 했다.

![image](https://github.com/PlaydataFinal/Final_project/assets/145752714/5e848793-b443-4aef-bb03-9bdd9c9843ba)





# 텍스트 유사도
태그 유사도 모델링에서 사용한 데이터는 제주관광공사에서 도메인 지식에 따라 labeling한 정제된 태그 데이터이다. 관광지에 대한 정성적인 정보들을 더 잘 담고 있는 자유도 높은 low-level 데이터로부터 유사도를 도출하고 싶었다.
-> 네이버 리뷰, 블로그 리뷰로부터 명사를 추출하고 어휘집을 만들어서 유의어를 처리하는 모델링을 구상했다.

![image](https://github.com/PlaydataFinal/Final_project/assets/145752714/53c8fe35-65b2-42fc-8d52-8a5ce702e921)

![image](https://github.com/PlaydataFinal/Final_project/assets/145752714/411810bf-8751-40ac-9ad7-d9a0aa544d9f)



그러나 데이터 merge 시 난점때문에 활용하기 어려웠다. 그래서 텍스트 유사도 모델링의 데이터로  visitjeju에 관광지별 상세설명 글을 채택했다. 텍스트 유사도 모델링은 챗봇 서비스로 적용하였다.



# 이미지 유사도
