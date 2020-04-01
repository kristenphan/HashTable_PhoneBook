# Hash Table_Phone Book

__Repository Description:__
<br/>
This repository stores the work as part of the Data Structures and Algorithms specialization courses by University California of San Diego. Course URL: https://www.coursera.org/learn/data-structures/. Code in this repository is written by myself, Kristen Phan.
<br/>
<br/>
__Assignment Description:__
<br/>
<br/>
Task: In this task your goal is to implement a simple phone book manager. It should be able to process the
following types of user’s queries:
<br/>
<br/>
-----add number name. It means that the user adds a person with name name and phone number
number to the phone book. If there exists a user with such number already, then your manager
has to overwrite the corresponding name.
<br/>
<br/>
-----del number. It means that the manager should erase a person with number number from the phone
book. If there is no such person, then it should just ignore the query.
<br/>
<br/>
-----find number. It means that the user looks for a person with phone number number. The manager
should reply with the appropriate name, or with string “not found" (without quotes) if there is
no such person in the book.
<br/>
<br/>
Input Format: There is a single integer 𝑁 in the first line — the number of queries. It’s followed by 𝑁
lines, each of them contains one query in the format described above.
<br/>
<br/>
Constraints: 1 ≤ 𝑁 ≤ 105. All phone numbers consist of decimal digits, they don’t have leading zeros, and
each of them has no more than 7 digits. All names are non-empty strings of latin letters, and each of
them has length at most 15. It’s guaranteed that there is no person with name “not found".
<br/>
<br/>
Output Format: Print the result of each find query — the name corresponding to the phone number or
“not found" (without quotes) if there is no person in the phone book with such phone number. Output
one result per line in the same order as the find queries are given in the input.
<br/>
<br/>
Time Limits: C: 3 sec, C++: 3 sec, Java: 6 sec, Python: 6 sec. C#: 4.5 sec, Haskell: 6 sec, JavaScript: 9
sec, Ruby: 9 sec, Scala: 9 sec.
<br/>
<br/>
Memory Limit: 512MB.
<br/>
<br/>
__Disclaimer__: 
<br/>
If you're currently taking the same course, please refrain yourself from checking out this solution as it will be against Coursera's Honor Code and won’t do you any good. Plus, once you're worked your heart out and was able to solve a particularly difficult problem, a sense of confidence you gained from such experience is priceless :)"
