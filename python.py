string = "376 calories; protein 7.3g; carbohydrates 40.4g; fat 22.4g; cholesterol 90.4mg; sodium 897.3mg. \
                                Full Nutrition"

cal,sod,pro,fat,chol,carbo =[],[],[],[],[],[]

arr = string.split(";")

for i in range(len(arr)):
    arr[i] = arr[i].strip()
    if(i==0):
        cal.append(arr[i].split(" ")[0])
    elif(i==len(arr)-1):
        sod.append(arr[i].split(" ")[1])
    elif(i==1):
        pro.append(arr[i].split(" ")[1])
    elif(i==2):
        carbo.append(arr[i].split(" ")[1])
    elif(i==3):
        fat.append(arr[i].split(" ")[1])
    elif(i==4):
        chol.append(arr[i].split(" ")[1])


print(cal,sod,pro,fat,chol,carbo)

df["calories"] = cal
df["carbohydrtes"] = carbo
df["sodium"] = sod
df["cholestrol"] = chol
df["fat"] = fat
df["protiens"] = pro

