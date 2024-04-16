"""
This program connects to quotable API and uses setitem, getitem and iter function.

1. Fetch quote from QPI
2. Allow accessing individual quotes by index (when making the request there might be limits on how many requests can be made)
3. Permit modification of quotes at a specific index (only for local cache)
4. enable interation over all fetched quotes
"""

#############  https://github.com/lukePeavey/quotable ####################


import requests

class QuotableCollection:
    def __init__(self, tag=None): # tags is needed when in the API call of the website there is something like subcategory and are like to search for tags for every quote 
        self.quotes = self.fetch_quotes(tag)
    
    def fetch_quotes(self, tag):
        """Fetch quotes frtom the Quotable API by tag"""
        url = "https://api.quotable.io/quotes"

        if tag:
            url += f"?tags={tag}" # the ? if for teh website that is called query parameter
        
        response = requests.get(url)

        return response.json()['results']
    
    def __getitem__(self, index):
        """Allow accessing a quote by index"""
        return f'"{self.quotes[index]["content"]}" ~{self.quotes[index]["author"]}'
    
    def __setitem__(self, index, value):
        """Allows setting a quote at a specific index."""
        # Setitem expects a obj[index] = value it will work with only the 3 above in ()
        self.quotes[index]['content'] = value

    def __iter__(self):
        return (quote['content'] for quote in self.quotes) # this is saved as a tuple and iter it will overwrites the getitem for showing all the quotes


quotable_collection = QuotableCollection(tag="technology")

# for quote in quotable_collection.quotes:
#     print(quote)

print("First quote is: " + quotable_collection[0])


print("Old quote:\n" + quotable_collection[3])
quotable_collection[3] = "AI will replace us"

print("New quote:\n" + quotable_collection[3])


for quote in quotable_collection: # If __iter__ is there it will print the quotes with only content and it will not go through getitem
    print(quote)