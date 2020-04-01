# python3
import random
import ctypes


# this class reads the query and structures it in a searchable format
class Query:
    def __init__(self, query):
        self.type = query[0]
        self.number = int(query[1])
        if self.type == 'add':
            self.name = query[2]

    def __str__(self):
        return "type: {}, number: {}".format(self.type, self.number)

# this function reads the queries using the Query class
def read_queries():
    n = int(input())
    return [Query(input().split()) for i in range(n)]

# this function writes the output in the required format
def write_responses(result):
    print('\n'.join(result))

# this function implements the naive approach to process queries for stress testing purposes
def process_queries_naive(queries):
    result = []
    # Keep list of all existing (i.e. not deleted yet) contacts.
    contacts = []
    for cur_query in queries:
        if cur_query.type == 'add':
            # if we already have contact with such number,
            # we should rewrite contact's name
            for contact in contacts:
                if contact.number == cur_query.number:
                    contact.name = cur_query.name
                    break
            else: # otherwise, just add it
                contacts.append(cur_query)
        elif cur_query.type == 'del':
            for j in range(len(contacts)):
                if contacts[j].number == cur_query.number:
                    contacts.pop(j)
                    break
        else:
            response = 'not found'
            for contact in contacts:
                if contact.number == cur_query.number:
                    response = contact.name
                    break
            result.append(response)
    return result

# this function returns a, b - the parameter of a hash function used to hash the value of a phone number
def choose_hash_function(L):
    p = 10**L + 3
    a = random.randrange(1, p-1)
    b = random.randrange(0, p-1)
    return a,b

# this function calculates and return the hash value of a phone number (in integer format)
# using parameters a, b, p, m
# a, b = parameters of the hash function being used
# p, m = prime number and cardinality of the hash function
# this function is built upon an integer hashing formula: hash_value = ((a*phone_number + b) % p) % m
# this phone number will then be looked up or added to the phone book using its hash value
def get_hash(number, a, b, L, m):
    p = 10**L + 3
    hash = ((a*number + b) %p) %m
    return hash

# this is a class that stores a hash table
# this hash table represents a phone book with contact info (name, number) stored using their respective hash values
class HashTable(object):
    '''
    HASH TABLE IMPLEMENTED AS A DYNAMIC ARRAY CLASS (Similar to Python List)
    '''

    def __init__(self, L, a, b):
        self.L = L # L = allowed length of phone numbers to be added to hash table
        self.a = a # parameter of the current hash function
        self.b = b # parameter of the current hash function
        self.n = 0 # Count the number of phone numbers stored in the hash table (Default is 0)
        self.m = 1 # m = cardinality of the hash table (default is 1)
        self.A = self.make_array(self.m) # each of the element in array A has been initialized as an empty list. each element represents a particular hash value and stores a list of phone number associated with said hash value

    # this function adds new contact info (name, number) to the hash table
    # if there's already a name associated with the passed in phone number, overwrite the name
    def add(self, name, number):
        """
        Add a contact (name, phone number) to the hash table using a hash value calculated from the phone number
        """
        # alpha (load factor) = n/m : represents how filled up the hash table is
        # collision is a scenario where two different phone numbers are assigned the same hash value, causing the operation of looking up phone number to have a long runtime
        # the goal is to keep alpha low to avoid collisions in the hash table (if we're storing too many contact info a small hash table, the probability of collision is high)
        # in this algorithm, once alpha = 0.9 or above, the hash table will be resized to accomodate more contact info
        # if alpha = n/m < 0.9, add the contact to the hash table using hash value and overwrite the number if needed. no need to resize the hash table
        if self.n/self.m < 0.9:
            self.add_contact(name, number, self.a, self.b)

        # otherwise, resize the hash table (double in size), get a new hash function, rehash all values, and add the contact info to the new hash table
        else:
            # get a new hash function
            self.a, self.b = choose_hash_function(self.L)
            # resize the hash table and rehash all value
            self._resize(2 * self.m)
            # add new contact to the new hash table
            self.add_contact(name, number, self.a, self.b)

    def add_contact(self, name, number, a, b):
        hash = get_hash(number, self.a, self.b, self.L, self.m)
        # if there is no contacts associated the hash values,check if any of these contacts is the same of the contact being added
        # add this contact to the hash table under this hash value
        if len(self.A[hash]) == 0:
            self.A[hash].append([name, number])
            self.n += 1

        # otherwise, check if there's any name stored in the hash table is the same as the name in the contact being added
        # if yes, overwrite the number phone
        # if no, add this contact to the hash table
        else:
            count = 0 # count the number of phone number associated with the passed-in name
            # if there is an existing phone number associated with the passed in name, overwrite the phone number
            for contact in self.A[hash]:
                if contact[1] == number:
                    contact[0] = name
                    count += 1
                    break
            # if there is no existing phone number associated with the passed in name,
            # add this contact info (name, number) to the hash table
            if count == 0:
                self.A[hash].append([name, number])
                self.n += 1


    def _resize(self, new_cap):
        """
        Resize internal array to capacity new_cap
        """
        B = self.make_array(new_cap) # New bigger array
        for i in range(self.m): # Reference all existing values
            if len(self.A[i]) != 0:
                for contact in self.A[i]:
                    newHash = get_hash(contact[1], self.a, self.b, self.L, new_cap)
                    B[newHash].append(contact)

        self.A = B # Call A the new bigger array
        self.m = new_cap # Reset the capacity



    def make_array(self, new_cap):
        """
        Returns a new array with new_cap capacity
        """
        A = (new_cap * ctypes.py_object)()
        for hashValue in range(new_cap):
            A[hashValue] = []

        return A


    def delete(self, number):
        hash = get_hash(number, self.a, self.b, self.L, self.m)
        if len(self.A[hash]) == 0: # if the number to be deleted in not yet stored in the phonebook, ignore the query
            return
        else: # otherwise, track down and delete the contact info associated with the phone number
            for i, contact in enumerate(self.A[hash]):
                if contact[1] == number:
                    del self.A[hash][i]


    # this function returns the name associated with the passed in phone number
    def find(self, number):
        hash = get_hash(number, self.a, self.b, self.L, self.m)
        if len(self.A[hash]) == 0: # if the phone number is not in the phonebook, return 'not found'
            return 'not found'
        else: # return the name of the person whose number has been passed in
            count = 0 # keep track whether a name has been return for a particular number
            for contact in self.A[hash]:
                if contact[1] == number:
                    name = contact[0]
                    count += 1
                    break
            if count == 0: # if no name was found associated with the phone number, return 'not found'
                return 'not found'
            else: # otherwise, return the name
                return name


# this function implements a phone book as a hash table
# and processes a series of queries
# add query: add a number to the phone book. if such number already exists in the phone book, overwrite the name associated with said number
# del query: delete a phone number from the phone book. if such number does not exist in the phone book, ignore the query
# find query: search the phone book and return the name associated with a particular phone number. if the phone number was not found in the phone book, return 'not found'
# after all queries have been processed, the function returns a list of return values (called 'result') from the find queries
def process_queries(queries):
    # the maximum length of a phone number is at max 7 digits (from the assignment description)
    L = 7
    # choose the initial hash function represented by a,b to generate hash values for different phone numbers
    a, b = choose_hash_function(L)
    # create a hash table to represent a phone book and store all contact info
    phonebook = HashTable(L, a, b)
    # create a list results to store all names retrived from the phone book using find query
    result = []

    for query in queries:
        if query.type == 'add':
            phonebook.add(query.name, query.number)

        if query.type == 'del':
            phonebook.delete(query.number)

        if query.type == 'find':
            name = phonebook.find(query.number)
            result.append(name)

    return result

if __name__ == '__main__':
    write_responses(process_queries(read_queries()))
    # example query with correct result = ['Mom', 'not found', 'police', 'not found', 'Mom', 'daddy']
    #queries = [Query(['add', 911, 'police']), Query(['add', 76213, 'Mom']), Query(['add', 17239, 'Bob']), Query(['find', 76213]), Query(['find', 910]), Query(['find', 911]), Query(['del', 910]), Query(['del', 911]), Query(['find', 911]), Query(['find', 76213]), Query(['add', 76213, 'daddy']), Query(['find', 76213])]
    #write_responses(process_queries(queries))
