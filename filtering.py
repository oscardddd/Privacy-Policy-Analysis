### This file is used to filter out the largest overlapping dataset



import os
from functools import reduce
import shutil
def filtering():
    obj = {}
    l = []
    for region in os.listdir('./final1'):
        rlist = []
        os.makedirs(f'./final3/{region}')
        for domain in os.listdir(f'./final1/{region}'):
            rlist.append(domain[3:])
        obj[region] = set(rlist)

        l.append(set(rlist))

    common_domains = l[0]



    # Iterate over the remaining sets and update common_domains with the intersection
    for domain_set in l[1:]:
        # print(domain_set)
        common_domains = common_domains.intersection(domain_set)

    print(len(common_domains))
    move(common_domains)

def move(common_list):
    des_path = './final3'

    for region in os.listdir('./final1'):
        print("moving ", region)
        for filename in os.listdir(f'./final1/{region}'):
            if filename[3:] in common_list:
                shutil.copy(f'./final1/{region}/{filename}',f'final3/{region}')


if __name__=="__main__":
    filtering()