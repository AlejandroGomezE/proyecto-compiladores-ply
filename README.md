# My Programming Language

University project.

## How to setup backend for scanning, parsing, and code generation

1. Clone this repo.

2. Make sure you have [`python`](https://www.python.org/downloads/) installed.

3. Use pip to install the requirements:

   ```bash
   pip install -r requirements.txt
   ```

4. Run the flask application.
   ```bash
   flask run --reload
   ```

## How to install and open web Graphical Interface

1. In a new terminal cd into the folder /frontend
   ```bash
   cd frontend
   ```
2. Install the dependencies
   ```bash
   npm install
   ```
3. Run the project
   ```bash
   npm run dev
   ```
4. Open the browser and go to http://localhost:5173

## Structure

```
program programa;

var string x = "Hello";
function a<float>(float f, float z){
  return f;
};

main(){
  var string y = " World";
  var float a = hola(20.0, 5.0);
  var bool z = True;

  if(z){
    print(a);
  }else{
    print(x + y);
  }

  var int i = 0;
  while(i < 3){
    print("test");
    i = i + 1;
  }
  i = 0;
  var int b[10];
  while(i < 10){
	  a[i] = i * 2;
    i = i + 1;
  }
  print(a[1], a[2], a[3]);
  sort(a, >);
  print(a[1], a[2], a[3]);
  print(find(a, 4));
};
```

## Data Types

**_Int_** Numbers without decimals.

**_Float_** Numbers with decimals.

**_String_** Text inside " "

**_Bool_** True, or False

## Global Variables

Declare before other functions.;

```
var string m = "Hello";
```

## Functions

Declare before main function, and after global variables. Acceptable return types:

**_Int_**

**_Float_**

**_String_**

**_Bool_**

**_Void_**

```
function ID<type>(type param_1, type param_2){
  return return_value;
};
```

## IF, IF Else Statements

```
if(condition){
   ...
}

if(condition){
   ...
}else{
   ...
}
```

## Arithmetic Operators

**`+`** , **_`-`_** , **_`/`_** , **`*`**

## Logical Operators

**_`<`_** , **_`>`_** , **_`==`_** , **_`!=`_** , **_`<=`_** , **_`>=`_**

## While Loop

Execute code while condition is true.

```
while(condition){
   ...
}
```

## Declare variable

```
var type ID = var_value;
var type ID[INT];
```

# Built-in Functions

## Print

```
print(value);
```

## Read

```
read(x);
```

## Absolute

Get the absolute value.

```
absolute(x);
```

## Square Root

Get the square root.

```
sqrt(x);
```

## TRUNCATE

Get the integer part of a number.

```
trunc(x);
```

## To Lower

Get the string in lower case.

```
toLower(x);
```

## To Upper

Get the string in upper case.

```
toUpper(x);
```

## Sub String

Get a substring of a string.

```
subString(x, start, end);
```

## Average

Get the average of a list of numbers.

```
avg(x);
```

## Sort

Sort a list of numbers.

```
sort(x, >);
sort(x, <);
```

## Find

Returns the index of a number in a list.

```
find(x, number);
```

## Max

Get the max value of a list of numbers.

```
max(x);
```

## Min

Get the min value of a list of numbers.

```
min(x);
```

## Sum

Get the sum of a list of numbers.

```
sum(x);
```

## Length

Get the length of a list of numbers.

```
len(x);
```
