from ctypes import sizeof
from dataclasses import dataclass


n = 20
ans = [] 
for i in range(1,n+1):
    for j in  range(1,n+1):
        if i <  j:
            ans.append([i, j])


data = [[1, 2, 3], [2,3,4], [3,4,5], [4,5,6], [1,3,5], [2,4,6], [1,3,4], [2,4,5], [3,5,6],  [1,2,4],  [2,3,5], [3,4,6]]
ans = [0] * 11
vis = [0] * 11

for i in data:
    ans[(i[0] * i[1]) % 11] += 1
    ans[(i[0] * i[2]) % 11] += 1
    ans[(i[1] * i[2]) % 11] += 1



    print(i)
    print((i[0] * i[1]) % 11)
    print((i[0] * i[2]) % 11)
    print((i[1] * i[2]) % 11)
    print("------------------")
print(ans)

        
