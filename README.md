# G-Findit.py
A tool to help locate files for a specific domain (similar to PowerMeta or Metagoofil) using a Google Custom Search API key and extract out specific fields of metadata using Exiftool. (Free keys give 100 queries a day, which is enough to search for up to 5 filetypes a day set to 10 pages searched. The filetypes and number of searched pages can be altered as needed. You can also have more than one API key and it will alternate to the next as a failover as extra error handling. 429 errors means you are out of queries for that day.)


Document Search and Metadata Extraction Tool

**Overview**

This Python-based tool is designed to search for and download documents hosted on a specified domain. It leverages the Google Custom Search API to locate files with various extensions, downloads these files into a dedicated folder, and then extracts key metadata from the downloaded documents using ExifTool. Additionally, it logs the URLs of all discovered files into a separate file.

**Key Features**


  •	Multi-Format Document Search:
  
      Searches for a wide range of file types including common document formats such as PDF, DOCX, TXT, XLS, and many others (e.g., doc, bak, tmp, gho, odt, ods, odp, odg, odf, gdoc).
      
  •	Automated File Download:
  
      Downloads the discovered documents and saves them into a folder named after the target domain.
      
  •	URL Logging:
  
      Keeps a record of all URLs where documents were found in a file named metadata-urls.txt within the domain folder.
      
  •	Metadata Extraction:
  
      Uses ExifTool to extract useful metadata fields (Author, Creator, CreatorTool, Producer, and Title) from each downloaded file and saves the results in metadata.txt.


**Prerequisites**


  •	Python 3.x:
  
    Ensure Python is installed on your system.
    
  •	Google API Key and Search Engine ID:
  
    You must have a valid API key and a Custom Search Engine (CSE) ID from Google. These credentials are required to access the Google Custom Search API.

    
      https://programmablesearchengine.google.com/about/ 
      
  •	ExifTool:
  
    Install ExifTool and make sure it is available in your system’s PATH. This is necessary for the metadata extraction functionality.
    
  •	Required Python Libraries:
  
    The script uses the requests, os, time, and subprocess modules.
    
      	You can install the requests library using:

      
Copy to install prerequisites (However you shouldn’t need to run this)


pip install requests

**How the Tool Works**
  1.	User Input & Setup:
  	  When the script runs, it prompts the user to enter the domain they want to search (e.g., example.com).
      It creates a folder named after the domain (with dots replaced by underscores) to store the downloaded files and output logs.
  3.	Document Search:
      The script uses the Google Custom Search API to search for documents on the specified domain.
      It filters searches by file type by appending filetype:<extension> to the search query.
      Multiple file types are supported, covering a broad range of document formats.
  4.	File Download & URL Logging:
     	For each file found, the tool downloads the file to the designated folder.
     	It simultaneously collects the URL of each found file.
     	After the search is complete, it writes all discovered URLs to a file named metadata-urls.txt within the same folder.
  5.	Metadata Extraction:
     	Once all files are downloaded, the tool iterates over each file (excluding the log files) and runs ExifTool on them.
     	It extracts specific metadata fields: Author, Creator, CreatorTool, Producer, and Title.
     	The metadata for each file is appended to a file called metadata.txt, along with a header indicating which file the metadata belongs to.
  6.	Rate Limiting & Pausing:
     	To respect Google’s rate limits, the script includes short pauses (2 seconds) between individual search requests and longer pauses (2 minutes) between searches for different file types.

**Usage**
  1.	Configure API Credentials:
    Edit the script to include your Google API key and Custom Search Engine ID.
  2.	Run the Script:
    Execute the script using Python:
  Copy Command to Run
    python g-findit.py
  3.	Follow Prompts:
    Enter the domain when prompted. The tool will then perform the search, download files, and extract metadata.
  4.	Review Output:
    o	Downloaded documents will be saved in a folder named after the domain.
    o	metadata-urls.txt contains all the URLs where documents were found.
    o	metadata.txt contains the extracted metadata for each downloaded file.

