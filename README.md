# Towards Automated Identification of Data Constraints in Software Documentation

This repository contains information about and the replication package for the paper "Towards Automated Identification of Data Constraints in Software Documentation", submitted to ICSE 2024.

### Content

- [paper.pdf](https://anonymous.4open.science/r/towards-automated-identification-of-data-constraints-8FC1/paper.pdf) - the submission to ICSE 2024
- [discourse-pattern-catalog.pdf](https://anonymous.4open.science/r/towards-automated-identification-of-data-constraints-8FC1/discourse-pattern-catalog.pdf) - the catalog with the 15 discourse patterns used for data constraints description. (Todo: the completed catalog)
- [data/constraints.csv](https://anonymous.4open.science/r/towards-automated-identification-of-data-constraints-8FC1/data/constraints.csv) - comma-separated file with 2338 labeled constraints. Each row corresponds to one constraint, and has the following columns:
  - _id - constraint id, unique 
  - system - system name, string type
  - file - file name, string type
  - start - start offset, numeric
  - end - end offset, numeric
  - constraint_text - constraint text, string type
  - sentence - sentence text, string type
  - operands - constraint operands, comma-separated string 
  - constraint_type - one of *binary-value*, *value-comparison*, *categorical-value*, *concrete-value* constraint types
  - discourse_pattern - one of 15 defined discourse patterns
  - filter - If the value is not null, it is excluded from our study and not utilized further.
- [data/negative-sentences.csv](https://anonymous.4open.science/r/towards-automated-identification-of-data-constraints-8FC1/data/no-constraints.csv) -  comma-separated file with 14,659 labeled negative sentences. Each row corresponds to one negative sentence, and has the following columns:
  - _id - negative sentence id, unique
  - system - system name, string type
  - file - file name, string type
  - start - start offset, numeric
  - end - end offset, numeric
  - sentence - sentence text, string type
- [data/negative-fragments.csv](https://anonymous.4open.science/r/towards-automated-identification-of-data-constraints-8FC1/data/negative-fragments.csv) - comma-separated file with 36,839 fragments divided from negative sentences. Each row corresponds to one negative fragment, and has the following columns:
  - system - system name, string type
  - file - file name, string type
  - start - start offset, numeric
  - fragment - fragment text, string type
  - discourse_pattern - one of 15 defined discourse patterns
  - operands - fragment operands extracted by our tool, comma-separated string 
  - constraint_type - one of four constraint types, identified by our tool
- [data/system-info.csv](https://anonymous.4open.science/r/towards-automated-identification-of-data-constraints-8FC1/data/system-info.csv) - comma-separated file with 15 systems. Each row corresponds to one system, and has the following columns:
  - System - system name, string type
  - Domain - specific area of application 
  - Version - system version
  - Type of Artifacts - artifact type (e.g., HTML pages)
  - Amount of Artifacts - the number of artifacts in the system
  - Links - URL links to documentation system
- [data/ml-results](https://anonymous.4open.science/r/towards-automated-identification-of-data-constraints-8FC1/data/ml-results) 
  - [cross-system.zip](https://anonymous.4open.science/r/towards-automated-identification-of-data-constraints-8FC1/data/ml-results/cross-system.zip) - the results of the cross-system validation, including positives and negatives.
  - [decision tree.zip](https://anonymous.4open.science/r/towards-automated-identification-of-data-constraints-8FC1/data/ml-results/decision%20tree.zip) - the evaluation results of Decision Tree
  - [Naive Bayes.zip](https://anonymous.4open.science/r/towards-automated-identification-of-data-constraints-8FC1/data/ml-results/Naive%20Bayes.zip) - the evaluation results of Naive Bayes Classifier
  - [linear SVM.zip](https://anonymous.4open.science/r/towards-automated-identification-of-data-constraints-8FC1/data/ml-results/linear%20SVM.zip) - the evaluation results of linear Support Vector Machine
  - [logistic regression.zip](https://anonymous.4open.science/r/towards-automated-identification-of-data-constraints-8FC1/data/ml-results/logistic%20regression.zip) - the evaluation results of  Logistic Regression 
  - [nonlinear SVM.zip](https://anonymous.4open.science/r/towards-automated-identification-of-data-constraints-8FC1/data/ml-results/nonlinear%20SVM.zip) - the evaluation results of  non-linear Support Vector Machine
- [code/ML-constraints-classifier](https://anonymous.4open.science/r/towards-automated-identification-of-data-constraints-8FC1/code/ML-constraints-classifier) - source code of machine learners
- [code/discourse-pattern-matcher](https://anonymous.4open.science/r/towards-automated-identification-of-data-constraints-8FC1/code/discourse-pattern-matcher) - source code of the discourse pattern matcher 