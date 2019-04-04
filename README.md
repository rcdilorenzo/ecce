# Exploratory Core Concept Extraction (Ecce)

_ecce_ = "behold" (Latin)

> Deuteronomy 5:24 (ESV)
>
> And you said, ‘Behold, the Lord our God has shown us his glory and greatness, and owe have heard
his voice out of the midst of the fire. This day we have seen God speak with man, and man still
live.

For thousands of years, people have studied the Bible from countless perspectives with diverse
approaches towards various goals. As a Christian myself, I have read, discussed, and learned
from it both in personal study and through others. With the plethora of related documents in
the form of commentaries, topical indexes, dictionaries, and cross-references, the Bible has
been scoured from cover to cover throughout the ages.

The application of this project is two-fold. The first objective is to create a visual exploration of
the topics from the Bible. If time permits, this would be accomplished using an interactive
website that gives users a way to see related passages that were only previously linked in a
manual fashion. Second, the trained recurrent neural network will be used to predicting both
related topics and Scripture references from arbitrary text (similar in form to Bible verses).

# Results (In Progress)

## Word Embeddings

| Embedding          | Included Words | Preprocessing                    | Sample of Missing Values                                                 |
|--------------------|----------------|----------------------------------|-------------------------------------------------------------------------|
| glove.6B.100d.txt  | 84.47%         | NA                               | ['jehoiada' 'ephah' 'benaiah' ... 'shebat' 'hadrach' 'famish']          |
| glove.6B.100d.txt  | 84.48%         | Replace possessive with singular | ['jehoiada' 'ephah' 'benaiah' ... 'shebat' 'hadrach' 'famish']          |
| glove.42B.300d.txt | 92.55%         | Replace possessive with singular | ['bosheth' 'whorings' 'netophah' ... 'siegeworks' 'hodiah' 'shelomoth'] |

### Models

| Model Type          | Data Type                           | Data Split          | Metric Type | Metric Value |
|---------------------|-------------------------------------|---------------------|-------------|--------------|
| Logistic Regression | Bag of Words                        | 75% Train, 25% Test | Accuracy    | 1.65%        |
| LSTM (100 nodes)    | Sequence (by frequency, no weights) | 75% Train, 25% Test | Accuracy    | 2.95%        |
