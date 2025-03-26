---
title: "Abstract class in C++"
categories:
  - Study
tags:
  - C++
  - WantedGameDeveloperCourseSeason2
---

# 1. 추상화 클래스
- 순수 가상함수(\+ 소멸자에 virtual 키워드)를 가지고 있는 클래스
- 껍데기만 있고 실제 구현은 없다
- 실제 구현은 해당 클래스를 상속받는 자식 클래스에서 이루어진다
	
### 1.1 순수가상함수
- 함수 뒤에 '\= 0' 을 붙여서 만든다

### 1.2 추상화 클래스의 생성자 & 소멸자
- virtual 소멸자 구현 있으면 이후 상속 받은 클래스의 소멸자를 구현하면 상속받은 클래스의 소멸자 호출 이후 상속 해준 클래스 소멸자 호출
- virtual이 없으면 delete 해주는 시점의 타입에 맞춘 소멸자만 호출된다