import matplotlib.pyplot as plt
import csv
import pandas as pd
import numpy as np



account_list = ["dataset@ALPublicHealth", "dataset@ADHPIO", "dataset@CDCgov","dataset@AZGovEducation", "dataset@CAgovernor","dataset@delaware_gov", "dataset@DHSWI", "dataset@DougBurgum", "dataset@GovBillLee", "dataset@GovernorVA", "dataset@GovInslee",
                "dataset@govkristinoem", "dataset@GovLauraKelly", "dataset@GovMikeDeWine", "dataset@GovNedLamont", "dataset@GovPritzker", "dataset@HealthyOklahoma", "dataset@GovSisolak", "dataset@HIgov_Health", "dataset@MassGov", "dataset@MassDPH", "dataset@MichiganHHS", "dataset@migov", "dataset@MoGov", "dataset@NC_Governor", "dataset@NJDeptofHealth",
                "dataset@NYGov", "dataset@OHAOregon", "dataset@OHdeptofhealth", "dataset@OregonGovBrown", "dataset@PAHealthDept", "dataset@PennsylvaniaGov", "dataset@StateMaryland", "dataset@TDEM","dataset@TexasDSHS", "dataset@texasgov", "dataset@US_FDA","dataset@UtahCoronavirus","dataset@UtahGov", "dataset@VDHgov","dataset@vermontgov", "dataset@wvgov", "dataset@WADeptHealth", "dataset@WVGovernor"]


print(len(account_list))
whole_list = []
follower_num_list = []
for i in account_list: #read all csv files
    print("dataset name: ", i)
    with open(i + '.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)
        row = [row for row in reader]
        data = pd.DataFrame(row)


    location_set = ["AL", "Alabama", "AZ", "Arizona", "AR", "Arkansas", "CA", "California", "CO", "Colorado", "CT", "Connecticut", "DE", "Delaware", "FL", "Florida",
                    "GA", "Georgia", "HI","Hawaii","ID", "Idaho", "IL", "Illinois", "IN","Indiana", "IA", "Iowa","KS", "Kansas", "KY","Kentucky", "LA", "Louisiana", "ME", "Maine", "MD",
                    "Maryland", "MA", "Massachusetts", "MI", "Michigan", "MN", "Minnesota", "MS", "Mississippi", "MO", "Missouri", "MT", "Montana", "NE", "Nebraska", "NV", "Nevada",
                    "NH", "New hampshire", "NJ", "New jersey", "NM", "New mexico", "NY", "New York", "NC", "North Carolina", "ND", "North Dakota", "OH", "Ohio", "Oklahoma", "OK",
                    "OR", "Oregon", "PA", "Pennsylvania", "RI", "Rhode island", "SC", "South carolina", "SD", "South dakota", "TN", "Tennessee", "TX", "Texas", "UT", "Utah", "VT",
                    "Vermont", "VA", "Virginia", "WA", "Washington", "WV", "West Virginia", "WI", "Wisconsin", "WY", "Wyoming"]

    print(len(data))
    for i in data.index: # select location format like city_name, state_name
        location = data.loc[i][1]
        res = location.split(",")
        if i % 1000 == 0:
            print(i)
        if len(res) > 1 and res[1].strip() in location_set:
            pass
        else:
            data.drop([i], inplace=True)

    print(len(data))
    whole_list.append(data)

res = pd.concat(whole_list, axis=0, ignore_index=True)
city_list = []

#filter out dupilicated item
for i in res.index:
    if i == 0:
        continue
    city_list.append(str(res.loc[i][1]))
print(res)
print(city_list)
city_set = set(city_list)
print(len(city_set), city_set)
a_matrix = np.zeros((len(city_set), len(whole_list)))
print(a_matrix.shape)

city_set = list(city_set)
print(len(city_set))

#calculate adjacancy matrix
for i in range(0, len(whole_list)):
    df_i = whole_list[i]
    print("df_i:", df_i)
    for j in range(0, len(city_set)):
        city_j = city_set[j]
        df_i.columns = ["user_id", "location", "activity"]
        data_index = df_i[df_i["location"] == city_j]
        a = data_index.index.to_numpy(dtype=int)
        act = 0
        for k in a:
            if df_i.loc[k][2] == -1 or df_i.loc[k][2] == 0:
                act = act + 0
            else:
                x = float(df_i.loc[k][2])
                act = act + np.exp(-x)

        act = round(act, 4)
        a_matrix[j][i] = act
pd.DataFrame(a_matrix).to_csv("Ad_matrix.csv", index=False)
