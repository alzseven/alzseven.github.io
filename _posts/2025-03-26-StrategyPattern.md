---
title: "Strategy Pattern"
categories:
  - Study
tags:
  - GOF Design Pattern
  - Behavioural Pattern
  - WantedGameDeveloperCourseSeason2
---

# 2. Strategy Pattern
- 어떤 방식으로 하느냐의 액션은 같게, 세부 구현은 다르게할때 사용
- 상속받는 클래스에서 실제 액션의 구현을 담당한다.
- 동작을 갈아끼울수 있다

```cpp
// Context.h

class Strategy;
class Context
{
//...
private:
	Strategy* strategy;
//...
public:
	void DoBehaviour();
	void SetStrategy(Strategy*);
//...	
};

```
```cpp
// Strategy.h

class Strategy
{
//...
public:
    virtual void Behaviour() = 0;
//...
};

```
```cpp
// ConcreteStrategy.h

class ConcreteStrategyStrategy
{
//...
public:
    void Behaviour() override;
//...
};

```