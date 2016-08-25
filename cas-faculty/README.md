Extraction of Faculty Member from Suffolk University CAS Faculty Directory
---

Abstract
---
1. Retrieve html of main page
2. Extract individual faculty pages via links
3. Individually retrieve html of each faculty
4. Extract name, rank/position, degree type, and institution of degree

Procedures
---
In order for the program to function properly, it is assumed that the link to the main page "http://www.suffolk.edu/college/6578.php" is accessible and had not been modified recently. 

Multiple tools from urllib and BeautifulSoup are used to extract the parsed html. From observation, all the individual faculty links are embedded within a div tag with class name "item" which can easily be extracted using BeautifulSoup. First the div is extracted from the parsed html and then the children of the div element are extracted and stored into a list. However, the list contains extra links and from observation all the extras appear before the first faculty links and thus the links are from the index of the first faculty link to the end of the list.

After acquiring a list of links, the program iterates through the links and does the following procedures for each faculty link:

First, the parsed html is retrieved and from observation, the information about the faculty is embedded within the first div element with class name "colBox"; the html is converted to a text, strip of leading and trailing whitepsaces, removed of empty strings, and stored in a list. From observation, the name and rank of the faculty member is in the second element of the list and thus extracted using split by ", "; however there are cases where the rank is replaced with "PhD" or is not provided -- in such such scenario, "PhD" (an exception) is replaced with "Associate Professor" and when not provided the rank is "Professor" (verified when compared with actual faculty page). 

The degree and institution information begins after the heading "Education" (from observation of several faculty pages) and thus the program starts searching for the information after the index of the heading string; however if the heading string is not found then start from the beginning of the list. The program stops iterating through the list when:
1. the length list of the string when split by "," is less than 2
2. and length of the list[0] is less than 5 char or when "Master" or "Bachelor" is in list[0]
The third condition is to account for the variation in spelling where "MA" can be written as "Master." When conditioon one and two are true then stop iterating through the list and save the most recent index.

Now looking through the list from the begin to end index, each string is split by "," and stored in a list and if:
1. length of list is x where 2 <= x <= 3
2. length of list[0] when replaced by "." is less than 5
3. all char in list[0] are a letter a-Z or list[0] starts with "Master" or "Bachelor"
If the begin and end index equals then the faculty member does not specify their education and degree and institution is an empty string. Otherwise, only if the length of degree is three (format: MA, Arts, Suffolk) then check if an institutional name ("University", "College", "Academy") is in list[2]; if yes then the name of the institution is in list[2] else the name is in list[2]. If the length is not three then it must be two and the degree and institution is respectively list[0] and list[1].

The information are stored to a list with string of institution strip of trailing and leading whitespaces and written to a csv file.
