# my_list = [1, 2, 3, 4, 5]

# for item in my_list:
#     print(item)

# create a GENERATOR, if it has a yield it will be called a generator
# Also generator is used when there is a lot data and instead of loading the memory and slow down the PC it will check only for you need

def my_list():
    yield 1
    yield 2
    yield 3
    yield 4
    yield 5

for num in my_list():
    print(num)





