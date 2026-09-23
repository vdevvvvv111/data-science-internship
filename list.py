#list is a collection of data , a list can contain any data type and list is indexed
# a = []
# numbers = [1,2,3,4,rrr,cc]
# print(numbers)
# print(numbers))

#list is an ordered

# a = [1,2,3]
# b = [3,2,1]

# a = [11,22,33,44,55,66,77,88,99,100]
# print(type(a))
# print(a[3])
# print(a[0:7])
# print(a[:])
# print(a[0:9:2])
# print(a[-1])
# print(a[::-1])
# print()

# b = "vishnudev"
# print(b[5])
# print(b[::-1])
# print(b[0:7:2])

#list is mutuable and string is immutuable

# a = [2,3,4,5,6]
# a[2] = "vishnudev"
# print(a)

# inbuilt function iin list

#append
a = [11,22,33,44,55,66,77]
a.append(12)
print([a])

#extend
a = [11,22,33,44,55,66,77]
a.extend("mohanan")
print([a])

#insert
a = [11,22,33,44,55,66,77]
a.insert(3,5)
print(a)

#pop 
a = [11,22,33,44,55,66,77]
a.pop(0)
print(a)

#clear
a = [11,22,33,44,55,66,77]
a.clear()
print(a)

#remove
a =[11,22,33,44,55,66,77]
a.remove(11)
print(a)

#tuple() is immutable, ordered and indexed, it can contain any element any size
#t1 = (11,22,33,44,55,66)

#nested list
a = [11,22,33,44,["mohan"],44,55]
print(a[4])






