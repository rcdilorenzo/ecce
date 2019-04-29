# Exploratory Core Concept Extraction (Ecce)

![Screenshot](https://user-images.githubusercontent.com/634167/56903950-46009900-6a6b-11e9-8d8e-51b6fdf21a4c.png)

## Introduction

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
manual fashion. Second, the trained network will be used to predicting both related topics and
Scripture references from arbitrary text (similar in form to Bible verses).

## Results

Both of the highest performing models ended up being extremely large fully-connected neural networks although multiple types of recurrent architectures were explored (LSTMs and GRUs) with word embeddings from [GloVe](https://nlp.stanford.edu/projects/glove/). The topic model came in at 435MB with 36,315,622 parameters with an input size of 13,337 and an output of 853 topics. The cluster model was 2.3GB with 191,259,581 parameters with an input size of 150 (truncated SVD of encoded word vocabulary) and an output of 63,581 clusters of cross-references.

### Topic Model

Using data from Nave's Topical Index (about ~4,200 without filtering), all of the following model revisions were trained on 21,106 verses, validated on 3,725 verses, and evaluated on 6,208 verses.

Name            |  Categorical Accuracy  |  Notes
----------------|------------------------|-----------------------------------------------------------------
lstm-base       |  2.95%                 |  sequence of words, no word embeddings, ~4200 possible topics
lstm-b4cab4     |  5.72%                 |  tuned and tweaked, reduce to ~850 topics, word embeddings from glove.42B.300d (includes 92.55% of ESV words)
svd-bow-cb8915  |  6.91%                 |  switch to truncated SVD with bag-of-words
svd-bow-52a075  |  6.62%                 |  additional experiments, exclude top two topics
svd-bow-88bf90  |  8.21%                 |  make SVD 200 components (102% of last model size)
svd-bow-ced288  |  7.06%                 |  make SVD 150 components (200 was too big for initial production machine)
nave-4576e8     |  13.61%                |  properly filter topics and remove SVD due to smaller model size, use vocabulary count vectorizer as direct input



### Cluster Model

The cluster model was trained on cross-references from the Treasury of Scripture Knowledge . All of the following model revisions were trained on 20,837 verses, validated on 2,678 verses, and evaluated on 6,129 verses (70%-10%-20% split).

Name                |  Categorical Accuracy  |  Notes
--------------------|------------------------|-----------------------------------------------------------
tsk-cluster-87b509  |  0.25%                 |  initial fully-connected model
tsk-cluster-f13345  |  0.33%                 |  add dropout layers and tweak architecture
tsk-cluster-1d7203  |  1.05%                 |  fix verses to have multiple uuids
tsk-cluster-26869f  |  1.14%                 |  add hidden layer and overfit with 10 patience epochs
tsk-cluster-4e1698  |  1.16%                 |  make SVD 200 components (doubled model size)
tsk-cluster-47f717  |  1.24%                 |  make SVD 150 components (200 was too big for production)
tsk-cluster-8a1db9  |  1.32%                 |  change epoch patience to 2 instead of 3
