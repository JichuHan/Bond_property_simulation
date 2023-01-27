#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


# # 程序说明
# 
#     这个程序可以画出一个债券所有时期的价格。下面每一个定理的验证按照指示操作即可，需要输入债券的期数，建议20。

# In[2]:


Price=[]
def cash_flow(t,r,i,C):
    global Price
    if t==0:
        Price.append(C)
        return
    #cash=[]
    I=0
    for k in range(1,t+1):
        I=I+C*r/pow((1+i),k)
        #cash.append(I)
    total=I+C/pow((1+i),k)
    #cash.append(total)
    Price.append(total)
    return cash_flow(t-1,r,i,C)

def cash_flow_1(t,r,i,C):
    Price=[]
    cash_flow(t,r,i,C)
    return Price


# In[15]:


Price=[]
cash_flow(30,0.009,0.01,100)


# # 定理一：市场价格与到期收益率成反比

# # 定理二：收益率下降带来的利润大于上升带来的损失

# ### 1. 可视化
#     需要使用者输入债券的数量，程序会根据债券的数量将到期收益率在0-1之间等分。债券的其他参数也可以调整，在下面的程序前四行调整即可。
#     
#     第一张图Y轴代表债券价格，X轴代表期限（越大到期越近），不同曲线代表不同到期收益率。
#     第二张图为期初价格与到期收益率的关系，相当于市第一张图在x=0的时候的截面展示。

# In[14]:


n=eval(input('请输入实验的债券数量：'))
#期数
T=30
#票面利率
r=0.05
#面值
C=100

price_total=[]
return_total=np.linspace(1/n,1,n)

for i in range(1,n+1):
    Price=[]
    cash_flow_1(T,r,i/n,C)
    price_total.append(Price)
    
Frame=pd.DataFrame(price_total)
Frame.T.plot(xticks=Frame.T.index,xlabel='Days to Due',ylabel='Price',figsize=(20,10),fontsize=10)
plt.legend(return_total)
plt.xlabel('Days to Due',fontsize=15)
plt.ylabel('Price',fontsize=15)
plt.title('Price Changes of Bonds with Different YTM',fontsize=20)
print('基本信息：期数{}，票面利率{}，面值{}。'.format(T,r,C))

plt.figure(figsize=(20,10))
Price_t0=Frame.iloc[:,0]
plt.plot(return_total,Price_t0)
plt.xlabel('YTM',fontsize=15)
plt.ylabel('Price',fontsize=15)
plt.title('Price of Bonds at T0 with Different YTM',fontsize=20)


# ### 2. 实验数据
#     下面的数据行为到期收益率，列为时间（最长的就是到期日，0就是期初）。数值为债券价格。

# In[4]:


Frame.index=return_total
Frame.head(10)


# ### 3. 实验结果
#     从第一张图可以看出，到期收益率越大（线越靠下），价格越低。
#     从第二张图可以看出，函数具有凸性，因此到期收益率下降带来的收益大于上升的损失（控制收益率变化幅度）。

# # 定理三：票面利率与债券价格波动幅度成反比

# # 定理四：到期时间与债券价格的波动幅度成正比

# # 定理五：随着债券到期时间的临近，价格波动幅度以递增的速度减少

# ### 1. 可视化
#     需要使用者输入债券的数量，程序会根据债券的数量将票面利率在0-1之间等分。债券的其他参数也可以调整，在下面的程序前四行调整即可。
#     
#     Y轴表示因为到期收益率变化债券价格上升或者下降的百分比，X轴代表期限，越大到期时间越近。不同曲线代表不同票面利率值。

# In[5]:


n=eval(input('请输入实验的债券数量：'))
#期数
T=30
#到期收益率下限
r0=0.01
#到期收益率
r=0.05
#到期收益率上限
r1=0.09
#面值
C=100


price_total=[]
Days=np.linspace(0,T+1,T+1)

Rise_total=[]
Drop_total=[]
for i in range(1,n+1):
    R=[]
    for j in np.array([r0,r,r1]):
        Price=[]
        cash_flow_1(T,i/n,j,C)
        price_total.append(Price)
        R.append(np.array(Price))
    Rise=(R[0]-R[1])/R[1]
    Drop=(R[2]-R[1])/R[1]
    Rise_total.append(Rise)
    Drop_total.append(Drop)

L=[]
return_total=np.linspace(1/n,1,n)
plt.figure(figsize=(20,10))
for i in range(0,len(Rise_total)):
    plt.plot(Rise_total[i])
    L.append(str(round(return_total[i],2))+' ('+' YTM+'+str(round(r-r0,2))+')')
    plt.plot(Drop_total[i])
    L.append(str(round(return_total[i],2))+' ('+' YTM-'+str(round(r-r1,2))+')')
plt.xticks=Days
plt.legend(L)

plt.xlabel('Days to Due',fontsize=15)
plt.ylabel('Ratio of Price Change',fontsize=15)
plt.title('Price Responses to YTM of Bonds with Different Interest Rates',fontsize=20)
print('基本信息：期数{}，到期收益率{}，到期收益率波动幅度{}，面值{}。'.format(T,r,r-r0,C))


# ### 2. 实验数据
#     下面的数据行为票面利率，列为时间（最长的就是到期日，0就是期初）。数值为价格变化幅度（相较于到期收益率没有变化的）。

# In[6]:


Frame1=pd.DataFrame(Rise_total)
Frame1.index=return_total
print("债券价格上升幅度")
Frame1.head(10)


# In[7]:


Frame2=pd.DataFrame(Drop_total)
Frame2.index=return_total
print("债券价格下降幅度")
Frame2.head(10)


# ### 3. 实验结果
#     从图中任意一个x（期限）截面都可以看到，债券票面利率越大，价格受到到期收益率扰动的程度越大。
#     从图中任意一条（组）曲线可以看到，随着期限的临近，债券波动幅度下降，最后为0，并且减小的速度递增。
#     

# In[ ]:




