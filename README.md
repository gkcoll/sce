# Swift-Cavalier-Encrypt

## About Naming

***Swift Cavalier*** is the English translation of my nickname – *灰尘疾客*. Notably, I chose not to include the meaning of 灰尘 (*dust*) in the translation. This decision reflects my unwavering resolve, as you will discover in the following paragraph.

This project embodies some of my deepest convictions.  Although it may appear naive or insignificant, it represents my  steadfast determination to oppose all forms of inhuman censorship.

I sincerely hope that anyone with the power to do so will lend their support to the advancement of this project!

## Introduction

An encryption algorithm created by myself.

It integrates a self-created and highly customizable Base 94 conversion algorithm, as well as a highly customizable Vigenere  encryption algorithm.

Entered text will be encrypted using mathematical operations, then confused using the two methods mentioned above.

## Detail

### Key System

Except basic magic methods (`__init__`, `__str__` and `__repr__`), the class `Key` provides the following methods: `save`, `gen_random`, `gen_key_string`, `encrypt`, `decrypt`. Let's delve into their specifics.

The basic operations of these methods are explained with  example code in the next section. For now, let's focus on the  principles.

In the `gen_key_string` method, I have used different obfuscations to make it difficult to crack. Most of them depend on mathematical operations.

```python
# Code Snippet
t = int(time.time())
random.seed(t * sum([ord(i) for i in password]))
pwd_int = str2int(password)
s = self.__step * t * pwd_int
p = self.__prec * sum([random.randint(1, t) for _ in range(10)])
i = s * p * self.__index * pwd_int
c = str2int(self.__chars)
code = int(md5_digest(f'{t * pwd_int}'), 16)
```

### Encryption & Decryption

In the `encrypt` and `decrypt` methods, multiple encryptions are applied. Vigenere (a Caesar Cipher  variant) and Base94 (customized) are used here. Similarly to `gen_key_string`, some simple but high-level mathematical operations are applied to  confuse the observer. Additionally, the constant e (the base of natural  logarithm) is also used.

If you are interested in these methods, please take a look at the code files: `sce.py`, `vigenere.py`, `base94.py`.

```python
# Code Snippet
digit = int(e.get(self.__index, self.__step, self.__prec))
coefficient = ((digit + 1)**(digit + 2))**(digit + 3)
int_data = str2int(string)
base_94_data = b94(int_data * coefficient, self.__chars)
vg_key = b94((self.__step * self.__prec * self.__index)**2)
```

## Usage

If it's your first time using this project, the following example code  will guide you through encrypting a string in the simplest way:

```python
from sce import Key

# Initialization
key_obj = Key(50, 620, 612, ''.join([chr(i) for i in range(33, 127)]), 'password_123')

string = "Their starting point is the finish line that most people can't reach in their entire life, while their finish line is the punchline that most people rarely get to see in their entire life."
# 他们的起点是大多数人一辈子都达不到的终点；他们的终点是大多数人一辈子难得一见的笑点。

# Start encryption
cipher = key_obj.encrypt(string, 'password_123')
print(cipher)
# )H=9kGW>-W3u?4gS0V-{Lg0Df\dv9KjB51;*9e*gMu`|fM57;};-tUtr;LwYrX!n6"x'-m"-A@$:*iHVr.sw8*Ec%_"v*S!-hfgy1UV(7:kew[@-!4/b-f]:IM|v*,R~DYCw;Q,kV^2RkW2q?.;M&m[|y_v>.]aGz1=f7n:9\sMD2~y1k2KCKx3,\25qDsXn\>[O78'S)E+*A(*`OUEVq0RZ.S@hy&33P*e0v/c1G#)F/XQl;A8*iCMXfy#\

# Check decryption result
plain = key_obj.decrypt(cipher, 'password_123')
print(plain == string)  # True
```

Now, let's have take a look at the details.

The example above is the most basic framework when you use this project. In the code, variable `key_obj` is a Key object, a class realized in the key system. To initialize a Key object, there are two ways: one is customize every parameter by yourself, and the another way is randomly generate. If you need a customize one, the former code have gave you answer, if you need to generate one random, please follow this code:

```python
from sce import Key

key_obj = Key().gen_random()
```

The example above demonstrates how  to generate Key randomly. Yes, it's incredibly easy, and only requires  two lines of code to accomplish.

When you run the code, pay close attention to the terminal  output. It will display the password of the Key object. Make sure to  save it if you plan on using this Key object in the future.

Since this is a Key object, you can quickly glance at its information by accessing the `__dict__` attribute.

Now, how can you save your own key? Saving an instance isn't feasible, and saving plaintext information isn't the most secure option either. Fortunately, the Key class provides a solution for this  problem.

```python
key_obj.save()
# You can complete an argument (it will be the file name) in parentheses,
# If nothing entered, the default value if the now time integer time stamp.
```

When you run the code, a file with the suffix `.k` will be created in the project directory. The file's content might look like this:

```
eyZzJkJHWD1UJHNYRV1YWHk8IEciIjdxZGYgRWM4VyhtbV1DLFM1YWlvTShPIV9nVFhtR1I8TWFDZUVp
SU1JSCMgekEsfkhINl93NiNvcUUra0kqZlV+bn0hXXhdQ155aHUyc1l+TVF1TC48LVxCe3E8O15RcHMm
cmNuRHdEQU8/dkMndjFCamovfUdBWmgrVyIqfEdTJ25nYVZpKjdHVHUuJjciO2RhczRHQkF7K3dGKVxD
WyBReEVCOCB0PlxoUkV4JUdTdVo0LysyWD0keQ==
```

This file contains the full information for the Key object. Make  sure to keep this file and its password securely stored, as it is crucial for using the  Key object in the future.

> The above example key corresponds to a Key object with password 123, try to read it using `Key().load(filename)` or `Key().load(key_string)`

To use this key string, you can utilize the `load` method of the Key object. However, merely holding onto the key string  is insufficient. When the key string was generated, it was encrypted.  Therefore, you need to provide the corresponding password in order to  decrypt and recover it.

### More

For basic usage, that's all for now. If you require more advanced  features, feel free to explore the code. The code includes comments to  guide you through the advanced features available.

## Enhancement

Since the project publish, I still have no idea to test the safety of the cipher texts, I don't know how long can a super computer crack the algorithm. If you can help me for free, please get contact with me, thank you!

If you found bug when using this project, welcome to new a issue!

### Long Text Test

> **Test Environment**
>
> Windows 11
> 11th Gen Intel(R) Core(TM) i5-11400H @ 2.70GHz

The program has passed the 5,000 character long text test in 0.9 seconds.

## License

MIT
