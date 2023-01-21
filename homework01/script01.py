
words = []
sorted_words = []

with open('words', 'r') as f:
            words = f.read().splitlines()                # careful of memory usage


            sorted_words = words.sort(key=len, reverse =True)

            for x in range(5):
                    print(words[x],'\n')
