# Trolls-Terminator
We try to classify the trolls on PTT, which is the most popular forum in Taiwan.  
[Technical report](https://github.com/joeychang0204/Trolls-Terminator/blob/master/documents/report.pdf)
[data](https://drive.google.com/drive/u/1/folders/0AH9reGUEmVJkUk9PVA)

## Data Collection
![Flow chart of building ground truth](https://github.com/joeychang0204/Trolls-Terminator/blob/master/documents/data.png)
Since there's no existing data, we made the ground truth by ourselves, including labeling articles and users.  
We first crawled all the articles and comments in the period of one week before the mayoral election in 2018.  
From this data, we manually classify the popular articles as political-related or not.  
We also manually labeled the users who made a lot of comments as trolls or not (according to their comments) as our ground truth.  
Users who with obvious political tendency while attacking others or urging others to vote for somebody would be classified as trolls.  
As a result, 835 (about one-third) of users are classified as trolls while the others are normal users. And among the 3020 popular articles, 2200 of them are political articles.


## Methods

![The architecture of PTT Trolls Terminator](https://github.com/joeychang0204/Trolls-Terminator/blob/master/documents/overview.png)
* Comment Length Analysis
* Used IP Number Analysis
* Content-based SVM classifier


## Result
![Final performance](https://github.com/joeychang0204/Trolls-Terminator/blob/master/documents/result.png)
