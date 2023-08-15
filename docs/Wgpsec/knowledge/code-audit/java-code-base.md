---
title: JAVA基础
---

# 前言

本章节主要内容为JAVA基础中比较重要的知识点小记。未来会不断的补充。

针对JAVA基础，没有必要进行长篇大论，对JAVA语法不熟悉的同学可以找视频或者在菜鸟教程中把JAVA基础知识过一遍。

# JAVA基础数据类型

## 内置数据类型

byte 8位(-128 - 127)、short 16位(-32758 - 32767)、int 32位(-2147483648 - 2147483647)、long 64位(-9,223,372,036,854,775,808 - 9,223,372,036,854,775,807)、float 32位、double 64位、boolean 1位、char 16位Unicode字符(\u0000 - \uffff)

对于数值类型的基本类型的取值范围，我们无需强制去记忆，因为它们的值都已经以常量的形式定义在对应的包装类中了。

例如 Byte.SIZE、Byte.MIN_VALUE、Byte.MAX_VALUE......

实际上，JAVA中还存在另外一种基本类型 void，它也有对应的包装类 java.lang.Void，不过我们无法直接对它们进行操作。

## 引用数据类型

- 在Java中，引用类型的变量非常类似于C/C++的指针。引用类型指向一个对象，指向对象的变量是引用变量。这些变量在声明时被指定为一个特定的类型，比如 Employee、Puppy 等。变量一旦声明后，类型就不能被改变了。
- 对象、数组都是引用数据类型。
- 所有引用类型的默认值都是null。
- 一个引用变量可以用来引用任何与之兼容的类型。
- 例子：Site site = new Site("Runoob")。

## Java常量

final关键字修饰常量。byte、int、long、和short都可以用十进制、16进制以及8进制的方式来表示。

当使用字面量的时候，前缀 **0** 表示 8 进制，而前缀 **0x** 代表 16 进制, 例如：

```
int decimal = 100;
int octal = 0144;
int hexa =  0x64;
```

字符串常量和字符常量都可以包含任何Unicode字符。例如：

```
char a = '\u0001';
String a = "\u0001";
```

# Java变量类型

- 类变量(静态变量)：独立于方法之外的变量，用 static 修饰。
- 实例变量：独立于方法之外的变量，不过没有 static 修饰。
- 局部变量：类的方法中的变量。

```java
public class Variable{
    static int allClicks=0;    // 类变量 
    String str="hello world";  // 实例变量 
    public void method(){
        int i =0;  // 局部变量
    }
}
```

# Java修饰符

## 访问控制修饰符

Java中，可以使用访问控制符来保护对类、变量、方法和构造方法的访问。Java 支持 4 种不同的访问权限。

- **default** (即默认，什么也不写）: 在同一包内可见，不使用任何修饰符。使用对象：类、接口、变量、方法。
- **private** : 在同一类内可见。使用对象：变量、方法。 **注意：不能修饰类（外部类）**
- **public** : 对所有类可见。使用对象：类、接口、变量、方法
- **protected** : 对同一包内的类和所有子类可见。使用对象：变量、方法。 **注意：不能修饰类（外部类）**。

## 访问控制和继承

请注意以下方法继承的规则：

- 父类中声明为 public 的方法在子类中也必须为 public。
- 父类中声明为 protected 的方法在子类中要么声明为 protected，要么声明为 public，不能声明为 private。
- 父类中声明为 private 的方法，不能够被继承。

## 非访问控制修饰符

为了实现一些其他的功能，Java 也提供了许多非访问修饰符。

- static 修饰符，用来修饰类方法和类变量。
- final 修饰符，用来修饰类、方法和变量，final 修饰的类不能够被继承，修饰的方法不能被继承类重新定义，修饰的变量为常量，是不可修改的。被声明为 final 类的方法自动地声明为 final，但是实例变量并不是 final
- abstract 修饰符，用来创建抽象类和抽象方法。
- synchronized(修饰方法) 和 volatile(修饰变量) 修饰符，主要用于线程的编程。
- transient 修饰符表示序列化该对象时，跳过该变量。

# Number、Math、Character、String类

![Java Number类](https://www.runoob.com/wp-content/uploads/2013/12/OOP_WrapperClass.png)

所有的包装类**（Integer、Long、Byte、Double、Float、Short）**都是抽象类 Number 的子类。

Character 类在对象中包装一个基本类型 **char** 的值

String类有11种构造方法，new在堆上，直接赋值在公共池上。String 类是不可改变的，所以你一旦创建了 String 对象，那它的值就无法改变了。如果需要对字符串做很多修改，那么应该选择使用 [StringBuffer & StringBuilder 类](https://www.runoob.com/java/java-stringbuffer.html)。

# StringBuffer、StringBuilder类

![img](https://www.runoob.com/wp-content/uploads/2013/12/java-string-20201208.png)

StringBuilder不是线程安全的，不支持同步访问。但StringBuilder比较快。

# 数组

 建议使用 **dataType[] arrayRefVar** 的声明风格声明数组变量。 dataType arrayRefVar[] 风格是来自 C/C++ 语言 ，在Java中采用是为了让 C/C++ 程序员能够快速理解java语言。

## For-Each循环操作数组

```java
      double[] myList = {1.9, 2.9, 3.4, 3.5};
 
      // 打印所有数组元素
      for (double element: myList) {
         System.out.println(element);
      }
```

## Arrays 类

java.util.Arrays 类能方便地操作数组，它提供的所有方法都是静态的。

# JAVA IO流

![img](https://www.runoob.com/wp-content/uploads/2013/12/iostream2xx.png)

# Java异常处理

- **检查性异常：**最具代表的检查性异常是用户错误或问题引起的异常，这是程序员无法预见的。例如要打开一个不存在文件时，一个异常就发生了，这些异常在编译时不能被简单地忽略。
- **运行时异常：** 运行时异常是可能被程序员避免的异常。与检查性异常相反，运行时异常可以在编译时被忽略。
- **错误：** 错误不是异常，而是脱离程序员控制的问题。错误在代码中通常被忽略。例如，当栈溢出时，一个错误就发生了，它们在编译也检查不到的。Java 程序通常不捕获错误。错误一般发生在严重故障时，它们在Java程序处理的范畴之外。

## Exception类的层次

所有的异常类是从 java.lang.Exception 类继承的子类。Exception 类是 Throwable 类的子类。

除了Exception类外，Throwable还有一个子类Error 。Error类用来指示运行时环境发生的错误。例如，JVM 内存溢出。一般地，程序不会从错误中恢复。

![img](https://www.runoob.com/wp-content/uploads/2013/12/12-130Q1234I6223.jpg)

# 重写、重载

## 重写的规则

- 参数列表与被重写方法的参数列表必须完全相同。
- 返回类型与被重写方法的返回类型可以不相同，但是必须是父类返回值的<u>子类</u>（java5 及更早版本返回类型要一样，java7 及更高版本可以不同）。
- 访问权限不能比父类中被重写的方法的访问权限更低。例如：如果父类的一个方法被声明为 public，那么在子类中重写该方法就不能声明为 protected。
- 声明为 final 的方法不能被重写。
- 声明为 static 的方法不能被重写，但是能够被再次声明。
- 子类和父类在同一个包中，那么子类可以重写父类所有方法，除了声明为 private 和 final 的方法。
- 子类和父类不在同一个包中，那么子类只能够重写父类的声明为 public 和 protected 的非 final 方法。
- 重写的方法不能抛出新的强制性异常，或者比被重写方法声明的更广泛的强制性异常，反之则可以。
- 构造方法不能被重写。

## 重载(Overload)

重载(overloading) 是在一个类里面，方法名字相同，而参数不同。返回类型可以相同也可以不同。

每个重载的方法（或者构造函数）都必须有一个独一无二的参数类型列表。

最常用的地方就是构造器的重载。

- 被重载的方法必须改变参数列表(参数个数或类型不一样)；
- 被重载的方法可以改变返回类型；
- 被重载的方法可以改变访问修饰符；
- 被重载的方法可以声明新的或更广的检查异常；
- 方法能够在同一个类中或者在一个子类中被重载。
- 无法以返回值类型作为重载函数的区分标准。

# 多态

## 多态存在的三个必要条件

- 继承
- 重写
- 父类引用指向子类对象：**Parent p = new Child();**

当使用多态方式调用方法时，首先检查父类中是否有该方法，如果没有，则编译错误；如果有，再去调用子类的同名方法。

## 多态的实现方式

方式一：重写：

方式二：接口

方式三：抽象类和抽象方法

# Java抽象类

在面向对象的概念中，所有的对象都是通过类来描绘的，但是反过来，并不是所有的类都是用来描绘对象的，如果一个类中没有包含足够的信息来描绘一个具体的对象，这样的类就是抽象类。抽象类除了不能实例化对象之外，类的其它功能依然存在，成员变量、成员方法和构造方法的访问方式和普通类一样。

一个类只能继承一个抽象类，但一个类却可以实现多个接口。

- 如果一个类包含抽象方法，那么该类必须是抽象类。
- 任何子类必须重写父类的抽象方法，或者声明自身为抽象类。
- 抽象类中不一定包含抽象方法，但是有抽象方法的类必定是抽象类。
- 构造方法，类方法（用 static 修饰的方法）不能声明为抽象方法。

# Java接口

接口（英文：Interface），在JAVA编程语言中是一个抽象类型，是抽象方法的集合，接口通常以interface来声明。一个类通过继承接口的方式，从而来继承接口的抽象方法。一个实现接口的类，必须实现接口内所描述的所有方法，否则就必须声明为抽象类。

- 接口不能用于实例化对象。
- 接口没有构造方法。
- 接口中每一个方法也是隐式抽象的,接口中的方法会被隐式的指定为 **public abstract**（只能是 public abstract，其他修饰符都会报错）。
- 接口中所有的方法必须是抽象方法。
- 接口中可以含有变量，但是接口中的变量会被隐式的指定为 **public static final** 变量
- 接口不是被类继承了，而是要被类实现。
- 接口支持多继承。

> JDK 1.8 以后，接口里可以有静态方法和方法体了。

## 接口的声明

接口的声明语法格式如下：

```
[可见度] interface 接口名称 [extends 其他的接口名] {
        // 声明变量
        // 抽象方法
}
```

> - 接口是隐式抽象的，当声明一个接口的时候，不必使用**abstract**关键字。
> - 接口中每一个方法也是隐式抽象的，声明时同样不需要**abstract**关键字。
> - 接口中的方法都是公有的。

重写接口中声明的方法时，需要注意以下规则：

- 类在实现接口的方法时，不能抛出强制性异常，只能在接口中，或者继承接口的抽象类中抛出该强制性异常。
- 类在重写方法时要保持一致的方法名，并且应该保持相同或者相兼容的返回值类型。
- 如果实现接口的类是抽象类，那么就没必要实现该接口的方法。

在实现接口的时候，也要注意一些规则：

- 一个类可以同时实现多个接口。
- 一个类只能继承一个类，但是能实现多个接口。
- 一个接口能继承另一个接口，这和类之间的继承比较相似。

## 接口的多继承

在Java中，类不能多继承，但接口允许多继承。

```java
public interface Hockey extends Sports, Event
```

## 标记接口

```java
package java.util;
public interface EventListener
{}
```

没有任何方法的接口被称为标记接口。标记接口主要用于以下两种目的：

- 建立一个公共的父接口：

  正如EventListener接口，这是由几十个其他接口扩展的Java API，你可以使用一个标记接口来建立一组接口的父接口。例如：当一个接口继承了EventListener接口，Java虚拟机(JVM)就知道该接口将要被用于一个事件的代理方案。

- 向一个类添加数据类型：

  这种情况是标记接口最初的目的，实现标记接口的类不需要定义任何接口方法(因为标记接口根本就没有方法)，但是该类通过多态性变成一个接口类型。

# Java枚举类

```java
enum Color 
{ 
    RED, GREEN, BLUE; 
} 
```

枚举类也可以声明在内部类中：

```java
public class Test
{
    enum Color
    {
        RED, GREEN, BLUE;
    }
 
    // 执行输出结果
    public static void main(String[] args)
    {
        Color c1 = Color.RED;
        System.out.println(c1);
    }
}
```

每个枚举都是通过 Class 在内部实现的，且所有的枚举值都是 public static final 的。

以上的枚举类 Color 转化在内部类实现：

```java
class Color
{
     public static final Color RED = new Color();
     public static final Color BLUE = new Color();
     public static final Color GREEN = new Color();
}
```

迭代枚举元素：

```java
    for (Color myVar : Color.values()) {
      System.out.println(myVar);
    }
```

## 枚举类默认方法

enum 定义的枚举类默认继承了 java.lang.Enum 类，并实现了java.lang.Seriablizable 和 java.lang.Comparable 两个接口。

- values() 返回枚举类中所有的值。
- ordinal()方法可以找到每个枚举常量的索引，就像数组索引一样。
- valueOf()方法返回指定字符串值的枚举常量。

枚举跟普通类一样可以用自己的变量、方法和构造函数，构造函数只能使用 private 访问修饰符，所以外部无法调用。

```java
enum Color
{
    RED, GREEN, BLUE;
 
    // 构造函数
    private Color()
    {
        System.out.println("Constructor called for : " + this.toString());
    }
 
    public void colorInfo()
    {
        System.out.println("Universal Color");
    }
}
```

枚举既可以包含具体方法，也可以包含抽象方法。 如果枚举类具有抽象方法，则枚举类中的每个对象都必须实现它。

```java
enum Color{
    RED{
        public String getColor(){//枚举对象实现抽象方法
            return "红色";
        }
    },
    GREEN{
        public String getColor(){//枚举对象实现抽象方法
            return "绿色";
        }
    },
    BLUE{
        public String getColor(){//枚举对象实现抽象方法
            return "蓝色";
        }
    };
    public abstract String getColor();//定义抽象方法
}

public class Test{
    public static void main(String[] args) {
        for (Color c:Color.values()){
            System.out.print(c.getColor() + "、");
        }
    }
}
```

# Java数据结构

Java工具包提供了强大的数据结构。在Java中的数据结构主要包括以下几种接口和类：

- 枚举（Enumeration）
- 位集合（BitSet）
- 向量（Vector）
- 栈（Stack）
- 字典（Dictionary）
- 哈希表（Hashtable）
- 属性（Properties）

# Java集合框架

Java 集合框架提供了一套性能优良，使用方便的接口和类，java集合框架位于java.util包中， 所以当使用集合框架的时候需要进行导包。

![img](https://www.runoob.com/wp-content/uploads/2014/01/2243690-9cd9c896e0d512ed.gif)

> 最虚线接口、二虚线抽象类、实线实现类

集合框架定义了几种算法，可用于集合和映射。这些算法被定义为集合类的静态方法。集合框架定义了三个静态的变量：EMPTY_SET，EMPTY_LIST，EMPTY_MAP的。这些变量都不可改变。

在尝试比较不兼容的类型时，一些方法能够抛出 ClassCastException异常。当试图修改一个不可修改的集合时，抛出UnsupportedOperationException异常。

## 使用迭代器遍历集合元素

```java
import java.util.*;
 
public class Test{
 public static void main(String[] args) {
     List<String> list=new ArrayList<String>();
     list.add("Hello");
     list.add("World");
     list.add("HAHAHAHA");
     //第一种遍历方法使用 For-Each 遍历 List
     for (String str : list) {            //也可以改写 for(int i=0;i<list.size();i++) 这种形式
        System.out.println(str);
     }
 
     //第二种遍历，把链表变为数组相关的内容进行遍历
     String[] strArray=new String[list.size()];
     list.toArray(strArray);
     for(int i=0;i<strArray.length;i++) //这里也可以改写为  for(String str:strArray) 这种形式
     {
        System.out.println(strArray[i]);
     }
     
    //第三种遍历 使用迭代器进行相关遍历
     
     Iterator<String> ite=list.iterator();
     while(ite.hasNext())//判断下一个元素之后有值
     {
         System.out.println(ite.next());
     }
 }
}
```

# Java ArrayList

![img](https://www.runoob.com/wp-content/uploads/2020/06/ArrayList-1-768x406-1.png)

ArrayList 类位于 java.util 包中。ArrayList 是一个数组队列，提供了相关的添加、删除、修改、遍历等功能。 add() 、 get() 、set() 、remove() 、size() 

迭代遍历：

```java
for (String i : sites) {
    System.out.println(i);
}
```

## ArrayList排序

Collections 类也是一个非常有用的类，位于 java.util 包中，提供的 sort() 方法可以对字符或数字列表进行排序。` Collections.sort(sites); `

# Java LinkedList

![img](https://www.runoob.com/wp-content/uploads/2020/06/linkedlist-2020-11-16.png)

链表（Linked list）是一种常见的基础数据结构，是一种线性表，但是并不会按线性的顺序存储数据，而是在每一个节点里存到下一个节点的地址。

与 ArrayList 相比，LinkedList 的增加和删除对操作效率更高，而查找和修改的操作效率较低。

# Java HashSet

![img](https://www.runoob.com/wp-content/uploads/2020/07/java-hashset-hierarchy.png)

HashSet 基于 HashMap 来实现的，是一个不允许有重复元素的集合。允许有 null 值。无序的。不是线程安全的。

# Java HashMap

![img](https://www.runoob.com/wp-content/uploads/2020/07/WV9wXLl.png)

HashMap 是一个散列表，它存储的内容是键值对(key-value)映射。实现了 Map 接口，不支持线程同步

# Java Iterator

Java Iterator（迭代器）不是一个集合，它是一种用于访问集合的方法，可用于迭代 [ArrayList](https://www.runoob.com/java/java-arraylist.html) 和 [HashSet](https://www.runoob.com/java/java-hashset.html) 等集合。

Iterator 是 Java 迭代器最简单的实现，ListIterator 是 Collection API 中的接口， 它扩展了 Iterator 接口。

![img](https://www.runoob.com/wp-content/uploads/2020/07/ListIterator-Class-Diagram.jpg)

```java
// 引入 ArrayList 和 Iterator 类
import java.util.ArrayList;
import java.util.Iterator;

public class RunoobTest {
    public static void main(String[] args) {

        // 创建集合
        ArrayList<String> sites = new ArrayList<String>();
        sites.add("Google");
        sites.add("Runoob");
        sites.add("Taobao");
        sites.add("Zhihu");

        // 获取迭代器
        Iterator<String> it = sites.iterator();

        // 输出集合中的第一个元素
        System.out.println(it.next());
    }
}
```

# Java Object类

![img](https://www.runoob.com/wp-content/uploads/2020/10/classes-object.gif)

Java Object 类是所有类的父类，也就是说 Java 的所有类都继承了 Object，**子类可以使用 Object 的所有方法**。Object 类位于 java.lang 包中，编译时会自动导入，我们创建一个类时，如果没有明确继承一个父类，那么它就会自动继承 Object，成为 Object 的子类。

Object 类可以显示继承，也可以隐式继承，以下两种方式时一样的：

显示继承:

```java
public class Runoob extends Object{

}
```

隐式继承:

```java
public class Runoob {

}
```

# Java泛型

Java 泛型（generics）是 JDK 5 中引入的一个新特性, 泛型提供了编译时类型安全检测机制，该机制允许程序员在编译时检测到非法的类型。

泛型的本质是参数化类型，也就是说所操作的数据类型被指定为一个参数。

## 泛型方法

可以写一个泛型方法，该方法在调用时可以接收不同类型的参数。根据传递给泛型方法的参数类型，编译器适当地处理每一个方法调用。

```java
public class GenericMethodTest
{
   // 泛型方法 printArray                         
   public static < E > void printArray( E[] inputArray )
   {
      // 输出数组元素            
         for ( E element : inputArray ){        
            System.out.printf( "%s ", element );
         }
         System.out.println();
    }
 
    public static void main( String args[] )
    {
        // 创建不同类型数组： Integer, Double 和 Character
        Integer[] intArray = { 1, 2, 3, 4, 5 };
        Double[] doubleArray = { 1.1, 2.2, 3.3, 4.4 };
        Character[] charArray = { 'H', 'E', 'L', 'L', 'O' };
 
        System.out.println( "整型数组元素为:" );
        printArray( intArray  ); // 传递一个整型数组
 
        System.out.println( "\n双精度型数组元素为:" );
        printArray( doubleArray ); // 传递一个双精度型数组
 
        System.out.println( "\n字符型数组元素为:" );
        printArray( charArray ); // 传递一个字符型数组
    } 
}
```

### 有界的类型参数

要声明一个有界的类型参数，首先列出类型参数的名称，后跟extends关键字，最后紧跟它的上界。

```java
public static <T extends Comparable<T>> T maximum(T x, T y, T z){
}
```



## 泛型类

泛型类的声明和非泛型类的声明类似，只是在类名后面添加了类型参数声明部分。

```java
public class Box<T> {
   
  private T t;
 
  public void add(T t) {
    this.t = t;
  }
 
  public T get() {
    return t;
  }
 
  public static void main(String[] args) {
    Box<Integer> integerBox = new Box<Integer>();
    Box<String> stringBox = new Box<String>();
 
    integerBox.add(new Integer(10));
    stringBox.add(new String("菜鸟教程"));
 
    System.out.printf("整型值为 :%d\n\n", integerBox.get());
    System.out.printf("字符串为 :%s\n", stringBox.get());
  }
}
```

## 类型通配符

1、类型通配符一般是使用?代替具体的类型参数。例如` List<?> `在逻辑上是`List<String>`,`List<Integer>` 等所有List<具体类型实参>的父类。

2、有界的类型通配符

```java
   public static void getUperNumber(List<? extends Number> data) {
          System.out.println("data :" + data.get(0));
       }
```

3、类型通配符下限通过形如` List<? super Number>`来定义，表示类型只能接受Number及其三层父类类型，如 Object 类型的实例。

# Java序列化

一个类的对象要想序列化成功，必须满足两个条件：

- 该类必须实现 java.io.Serializable 接口。
- 该类的所有属性必须是可序列化的。如果有一个属性不是可序列化的，则该属性必须注明是短暂的。

# super

JAVA规定，子类继承父类，子类的构造方法必须调用super()，即父类的构造方法，而且必须放在构造方法的第一行。

有时我们写子类时，并没有调用super()方法，那是因为系统默认会在子类的构造方法中的第一行加上super()方法，即父类的无参构造方法。

# 类中$符号的含义

在一些源码里经常会看到，类名中会包含`$`字符，例如fastjson中`checkAutoType`方法就会将`$`替换成`.`。

`$`字符的主要含义是查找内部类。

Java中的普通类`C1`中支持编写内部类`C2`。编译后，会生成两个文件：`C1.class`和`C1$C2.class`，它们两个可以看作两个互不干扰的独立的类。通过`Class.forName("C1$C2")`可以加载这个内部类。

# 单例模式

JAVA设计模式之单例模式，常用场景为数据库的连接类。

对于WEB应用来说，数据库的连接只需要建立一次，而不是每次用到数据库时都新建一个连接。这时，就需要将数据库类的构造函数设置为私有，然后编写一个静态变量存储一个连接，再通过静态方法来获取这个连接。这样，需要使用数据库时，只需要调用静态方法获得这个静态变量中存储的数据库连接，来实现所有对象共用一个连接，而不是重复的建立。

```java
public class TrainDB {
	public static TrainDB instance = new TrainDB();
	public static TrainDB getInstance() {
		return instance;
	}
	private TrainDB() {
		//	建立连接的代码......
	}
}
```

# Java中方法和函数的区别?

面向过程的语言称为函数,面向对象的语言成为方法.函数是大家的函数,方法是类的方法.

> https://m.yisu.com/zixun/132813.html

# Java重载和重写的区别？

重载overload就是方法名相同,参数不同,返回值可以相同也可以不同.

重写overwrite就是方法名相同,参数相同,返回值相同,方法体被子类重写.