# Text Analysis Tool 

This tool preforms preliminary data analysis and visualization to understand trends and information from text. This tool was orginally created to analyze survey data, but could be used to analyze other text such as tweets. 

The script includes the following: 

* general frequency word count 
* specific word search/count
* bar graphs of word counts 
* word cloud of responses 
* calculation of polarity and sentiment 
* file export of dataframe to csv file 

## Set up 

This tool requires a data import of strings and importing specific libraries. 

1. Set up libraries  

```
install pandas

`pip install pandas` 

install textblob

`pip install textblob`

install matplotlib

`pip install matplotlib` 
```

2. Add text to analyze to text_data.csv CSV file in this repository

3. Run command from terminal 

`python text_analysis_tool.py`

4. Go through user prompts and after viewing graphs click out of visualization to continue to next part of the program
