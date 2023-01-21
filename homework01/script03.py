import names

def name_length(name): 
    return len(name)-1  

name_list = [names.get_full_name() for x in range(5)] 

for name in name_list: 
    print(name, name_length(name)) 
