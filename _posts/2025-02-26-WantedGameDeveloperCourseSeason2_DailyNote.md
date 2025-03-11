---
title: "2025-02-26_CppDailyNote"
categories:
  - Blog
tags:
  - C++
  - WantedGameDeveloperCourse
---

# 오전
### 열거형(Enumeration, Enum)
- 관련된 상수들의 집합을 의미있는 이름으로 묶어서 표현할 수 있는 데이터타입
```cpp
enum TileType {
    EARTH,      // 자동으로 0부터 시작이 기본
    FOREST = 5, // 이런식으로 숫자 지정 가능
    SWAMP       // 기본적으로는 다음 숫자, 이 경우에는 6
};
struct Tile {
	...
    TileType type;
};
int main()
{
    Tile tile;
    tile.type = TileType::EARTH;        // 이런식으로 사용 가능하다.
    tile.type = (TileType)(rand() % 3); // 정수를 캐스팅해서 이런식으로도 가능
}
```
- 데이터의 처리보다 코드상의 의미전달에 의미가 있다.
- 요즘은 이렇게도 쓴다
```cpp
enum class TileType // 기본은 각 4바이트
: uint8_t // 이런식으로 메모리를 줄일수도 있다. 이경우엔 각 1바이트, 표현범위는 감소
{
    Earth,
    Forest,
    Swamp
};
struct Tile {
    TileType type;
};
int main()
{
    Tile tile;
    tile.type = TileType::Earth;
    tile.type = (TileType)(rand() % 3);  // 이경우엔 형변환이 강제된다.
}
```
### 클래스 개요
- OOP
- 객체 - (메시지) - 객체
- 절차지향 - 과도한 전역변수 - ...
- 캡슐화
- ...
---
### 이어서
- (객체) 상태 - (프로그램) 멤버변수/필드 - 속성, 데이터...
- (객체) 동작 - (프로그램) 멤버함수/메소드 - 기능, 동작...
- 클래스와 객체(인스턴스) 사이의 관계
- ...
- 접근지정자(private/protected/public)
### 클래스(Class)
```cpp
class Car // 틀, 설계도
{
//멤버 변수(field, 속성, state, 데이터)
private: // 외부 엑세스 불가
    float moveSpeed;
    float maxMoveSpeed;
    short gear;
    string color;
    RECT rc;

//멤버 함수(method, 동작, 기능, 함수)
public: // 외부 엑세스 가능
    void Setup(float moveSpeed, float maxMoveSpeed, short gear, string color, RECT rc) {
        // this 키워드
        // 해당 인스턴스의 주소를 말한다.
        // this를 통해 파라미터와 멤버변수의 이름이 같아도 멤버변수 지정 가능
        // 주소라서 역참조 가능(*this) / this -> (이쪽이 선호됨)
        this -> moveSpeed = moveSpeed; 
        this -> maxMoveSpeed = maxMoveSpeed;
        this -> gear = gear;
        this -> color = color;
        this -> rc = rc;
    }
    void SpeedUp(){}
    void SpeedDown(){}
    void ChangeGear(){}
    void Run(){}
    void Draw()
    {
        HDC hdc = GetWindowDC(GetForegroundWindow());
        Ellipse(hdc, rc.left, rc.top, rc.right, rc.bottom);
    }
};

int main()
{
    Car car1, car2;
    RECT rc{ 100,100, 200, 200 };
    car1.Setup(0.0f, 5.0f, 1, "Red", rc);
    car2.Setup(0.0f, 10.0f, 1, "Blue", rc);

    while (1) {
        car1.Draw();
        Sleep(200);
    }
}```
---
### 전날 하던거 이어서해서 제출
- 클래스도 더 해도 좋다
- 다한사람들 도전과제
	- 일반적인 바닥있고, 숲바닥있고, 물웅덩이같은게 있는데, 랜덤하게...
	- 숲은 숲끼리, 늪은 늪끼리, 모양이 무작위로
---
# 오후
### UML
- 프로그램 그림의 역사 :  순서도(알고리즘 기반) -> 구조도(모듈/기능 사이의 관계) -> 클래스 다이어그램(대표적으로 UML) 
- UML의 구성
	1. 클래스 다이어그램
	2. 객체 다이어그램
	3. 상태 다이어그램
	4. 시퀸스 다이어그램
- 클래스 다이어그램의 구성
	- 클래스 이름
	- 멤버 변수
	- 멤버 함수
- 접근지정자 -(private), +(public),...
- 관계를 가지고 말할때 화살표 사용
- 찾아보기
### 팀 과제
해야하는것
UML 
관계 관련된거 관련해서 같이 알아보고
책으로 같이 본게 181p 정도
이 뒤에 188p ~ 201p 까지 팀원들이랑 다시 보고
클래스에 대해 개념적으로 정리를 하고
UML이랑 클래스에

체스를 구현을 한다
UML을 그린다
3명이 다 같이 모여서

이후 작업 분배
누가 이거 구현할건지
담당하는 클래스들을 구현까지 하면 된다.

룰이 정해져있고
역할 나누기 안어려울거같아서 체스로 하면 된다

특수룰은 제외하고 기본룰로만 해도 좋다

두가지가 나와야 한다
UML(누가 어떤거 만들기로 했다까지 있어야 함), 결과물

게임 러닝이 가능해야한다

배운 내용까지만 쓴다

---
만들어야 하는거(내일 5시까지)
1. 체스 게임 UML(각자 역할배분)
2. 게임 러닝이 가능한 코드
### 체스 게임 UML
##### UML에 관하여
- 클래스 다이어그램
	- 네모들
	- 화살표
		- 연관 : 한 클래스가 다른 클래스를 알고있거나 사용하는 경우
```cpp
class Student {
private:
    Course* course;
public:
    void enrollCourse(Course* c) {
        course = c;
    }
};

class Course {
    // Course implementation
};
// 여기서 Student 클래스는 Course 클래스와 연관 관계를 가집니다
```
- 집합 : has-a 관계를 나타내며, 한 클래스가 다른 클래스를 포함하지만
	포함된 클래스가 독립적으로 존재할수 있는 경우
```cpp
class Engine {
    // Engine implementation
};

class Car {
private:
    Engine* engine;
public:
    Car(Engine* e) : engine(e) {}
};
// Car 클래스는 Engine 클래스를 집합 관계로 가집니다. Engine은 Car 없이도 존재할 수 있습니다
```
### 체스 유닛
- 폰
	properties
	- positionX
	- positionY
	- icon
	- team(color)
	- moveRange
	- moveDir
	- 생존여부
	functions
	- move
	- onCollide(OR takeDamage... whatever)
	- getValidMove
- 룩
- 나이트
- 비숍
- 퀸
- 킹
### 게임시스템적인것들
- board 있어야 함
	 - 판 번호, 위에 말 있는 여부, 색상?
	 - 이동 유효판정을 여기에서?
- 게임 클래스
	- 제한 시간, 남은 시간, 
	- 턴 플레이어
	- 승리 패배 체크, 

### 유닛의 정보
- positionX
- positionY
- 생명
- icon
- 방향
- 팀(or 색상)
- 겹치는 여부
- 움직인 곳에 뭐가 있는지(게임에 대한 정보?)
- 유닛들
- 턴 시간
- (체스판에서) 이게 몇,몇인지
### 액션/함수
- 이동
- 겹칠떄 판단
- 겹쳤을떄 액션
- (체스 액션) 체크메이트
### 여담
UML 써서 역할나누는거 어려워요
하지만 우리 다른사람들이랑 작업하는 스킬들을 익혀야 합니다
결국 회사가서 같이 일할것
다른사람들 짜는거랑 다를수 있는거랑 합의점을 찾아서 공통 설계도를 그려놓는게 중요

다른 모듈이 선행되지 않아도 짤수 있게 되어야 잘 짜야진것
인터페이스를 통해서 어떤식으로 상호작용하겠다가 정해지는것
= 구현이 되있던 안되있던 만들수 있게 된다