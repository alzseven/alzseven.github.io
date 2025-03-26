---
title: "Factory Pattern"
categories:
  - Study
tags:
  - GOF Design Pattern
  - Creational Pattern
  - WantedGameDeveloperCourseSeason2
---

# 1. Factory Pattern
- 동일한 구조인데 실제 구현이 다를때 팩토리란 곳에서 생성하겠다
- 책임 소재 명확히 하는데 좋다(생성은 factory클래스가 책임)

```cpp
// Product.h

class Product
{
//...
public:
    virtual void Use() = 0;
//...
};

```
```cpp
// Factory.h

class Product;
class Factory
{
//...
private:
	virtual Product* CreateProduct() = 0;
//...
};

```
```cpp
// ConcreteProduct.h

class ConcreteProduct
{
//...
public:
    void Use() override;
//...
};

```
```cpp
// ConcreteFactory.h

class ConcreteFactory
{
//...
private:
	Product* CreateProduct() override;
//...
};

```