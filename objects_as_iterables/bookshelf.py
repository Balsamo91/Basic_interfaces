# Getting a item/index from a list using __getitem__

# class Bookshelf:
#     def __init__(self):
#         self.books = ["Book 1", "Book 2", "Book 3"]

#     def __getitem__(self, index):
#         return self.books[index]
    
# shelf = Bookshelf()
# print(shelf[1])

#############################
# changing the list with __setitem__

# class Bookshelf:
#     def __init__(self):
#         self.books = ["Book 1", "Book 2", "Book 3"]

#     def __getitem__(self, index):
#         return self.books[index]
    
#     def __setitem__(self, index, value):
#         self.books[index] = value

    
# shelf = Bookshelf()
# print("Old Book: " + shelf[1])

# shelf[1] = "Super cool Book"
# print("New Book: " + shelf[1])


#################################

# Iterate ove the list/object using 

class Bookshelf:
    def __init__(self):
        self.books = ["Book 1", "Book 2", "Book 3"]

    def __getitem__(self, index):
        return self.books[index]
    
    def __setitem__(self, index, value):
        self.books[index] = value

    def __iter__(self):
        return iter(self.books)


    
shelf = Bookshelf()
print("Old Book: " + shelf[1])

shelf[1] = "Super cool Book"
print("New Book: " + shelf[1])

print("\nAll books:")
for book in shelf:
    print(book)


print("\nAll books:")
print(next(shelf))