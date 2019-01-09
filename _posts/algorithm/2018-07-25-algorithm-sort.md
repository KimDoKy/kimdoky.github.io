---
layout: post
section-type: post
title: algorithm - sort and searching with python
category: algorithm
tags: [ 'algorithm' ]
---

## Bubble Sort

```Python
def bubbleSort(alist):
  for passnum in range(len(alist)-1,0,-1):
    for i in range(passnum):
      if alist[i]>alist[i+1]:
        temp = alist[i]
        alist[i] = alist[i+1]
        alist[i+1] = temp
```

## Selection Sort

```Python
def selectionSort(alist):
  for fillslot in range(len(alist)-1,0,-1):
    positionOfMax=0
    for location in range(1, fillslot+1):
      if alist[location]>alist[positionOfMax]:
        positionOfMax = location

      temp = alist[fillslot]
      alist[fillslot] = alist[positionOfMax]
      alist[positionOfMax] = temp
```

## Insertion Sort

```python
def insertionSort(alist):
  for index in range(1,len(alist)):

    currentvalue = alist[index]
    position = index

    while position>0 and alist[position-1]>currentvalue:
      alist[position]=alist[position-1]
      position = position-1

    alist[position]=currentvalue
```

## Shell Sort

```Python
def shellSort(alist):
  sublistcount = len(list)//2
  while sublistcount > 0:

    for startposition in range(sublistcount):
      gapInsertinSort(alist, startposition, sublistcount)

    print("After increments of size", sublistcount, "The list is", alist)

def gapInsertinSort(alist, start, gap):
  for i in range(start+gap, len(alist),gap):

    currentvalue = alist[i]
    position = i

    while position>=gap and alist[position-gap]>currentvalue:
      alist[position]=alist[position-gap]
      position = position-gap

    alist[position]=currentvalue
```

## Merge Sort

```Python
def mergeSort(alist):
  if len(alist)>1:
    mid = len(alist)//2
    lefthalf = alist[:mid]
    righthalf = alist[mid:]

    mergeSort(lefthalf)
    mergeSort(righthalf)

    i=0
    j=0
    k=0
    while i < len(lefthalf) and j < len(righthalf):
      if lefthalf[i] < righthalf[j]:
        alist[k]=lefthalf[i]
        i=i+1
      else:
        alist[k]=righthalf[j]
        j=j+1
      k=k+1
    while i < len(lefthalf):
      alist[k]=lefthalf[i]
      i=i+1
      k=k+1
    while j < len(righthalf):
      alist[k]=righthalf[j]
      j=j+1
      k=k+1
```

## Quick Sort

```Python
def quickSort(alist):
  quickSortHelper(alist,0,len(alist)-1)

def quickSortHelper(alist,first,last):
  if first<last:

    splitpoint = partition(alist,first,last)

    quickSortHelper(alist,first,splitpoint-1)
    quickSortHelper(alist,splitpoint+1,last)

def partition(alist,first,last):
    pivotvalue = alist[first]

    leftmark = first+1
    rightmark = last

    done = False
    while not done:

      while leftmark <= rightmark and alist[leftmark] <= pivotvalue:
          leftmark = leftmark +1

      while alist[rightmark] >= pivotvalue and rightmark >= leftmark:
          rightmark = rightmark -1

      if rightmark < leftmark:
          done = True
      else:
          temp = alist[leftmark]
          alist[leftmark] = alist[rightmark]
          alist[rightmark] = temp

    temp = alist[first]
    alist[first] = alist[rightmark]
    alist[rightmark] = temp

    return rightmark
```
