# Tool to get the list of the czech schools from the MŠMT registry

## Table of contents
* [General info](#general-info)
* [Technologies](#technologies)
* [Setup](#setup)
* [Other sources](#other-sources)

## General info

The Ministerstvo školství, mládeže a tělovýchovy privides registers of schools and school organizations on the  data.gov.cz portal (Portál otevřených dat). Anyone can get xml file - list of schools for particular district (kraj). This library helps to parse and convert xml file to csv file - the whole xml file or based on user defined address (city/town/village) search.

## Technologies

* Python 3
* Xml library
* Pandas

## Setup

Clone the repo:
https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository

Go to the data.gov.cz and download the registry file of your district (kraj):
For example: https://data.gov.cz/datov%C3%A1-sada?iri=https%3A%2F%2Fdata.gov.cz%2Fzdroj%2Fdatov%C3%A9-sady%2F00022985%2F2cd115ecd204aadabe9dab96d4c3733c. And download the source file in xml to the root directory of the repo.

In the command line go to the directory with the repo and use like this:
"python xml-to-csv.py name_of_the_source_file name_of_the_city"

For example:
"python xml-to-csv.py vrejcz020.xml Kladno"

Csv file with the name "output.csv" from the registry is saved in the working directory.

Due to the structure of the source xml file, you can use only those provided by the MŠMT.

## Other sources
Code list of the types of schools and school organization is f.e. under this link:
http://stistko.uiv.cz/katalog/cslnk.asp?aad=&aak=&aap=on&idc=AKDT&ciselnik=Druhy+a+typy+%9Akol+a+%9Akolsk%FDch+za%F8%EDzen%ED+%28nov%E9%29&poznamka=