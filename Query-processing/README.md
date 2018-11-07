Instructions:

1. Use index.py for creating the index - path to the wiki-dump and the folder for index should be specified. This will create multile indexes
2. Use merger.py to merge the above created index into one sorted file
3. After step 2, run byte_finder.py. This creates multiple files by spltting into multiple categories - body, title, infobox etc. and a file that stores pointers to all the words in the above files
4. Now, use search.py to search for queries. There can be two types of queries - field/general. On choosing f, you wil be asked to search by multiple field types - infobox, body, categories etc. Otherwise, you can type in a general query. Note that there is a lot of loading time before this step as all the required pointers for all the files are stored in memory.

Check the example.ipynb for demonstration. 

Use Python 2 to run all the codes

