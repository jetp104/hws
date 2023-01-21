import names

for i in range(5):
        name = names.get_full_name() 
        while len(name) != 9: 
            name = names.get_full_name()
        print(name) 
