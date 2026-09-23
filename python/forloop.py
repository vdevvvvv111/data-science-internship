#forloop
#range(start,stop,step)
sum = 0
# for i in range (1,10):
#     sum = sum+i
#     print(i)

# print(sum)

# num = int(input("enter the  number"))
# fact = 1
# for i in range(1,10):
#     fact = fact*i
#     print(i)

# print(fact)

# count = int(input("enter the count"))
# sum = 0
# avg = 0
# for i in range (count):
#     b = int(input("enetr the number"))
#     sum = sum+b
#     avg = sum/count
# print(sum)
# print(avg)


#pass
#continue
#break

# for i in(1,10):
#     if i==6:
#         continue


# print(i)

num=int(input("enter the number"))
flag=False
if num == 1:
    print("not a prime")
else:
    for i in range(2,num):
        if num % i ==0:
            flag = False
            break
        if  flag == True:
            print("prime")
        else:
            print("not prime")


    
        
         
          




    
    
