# ML Constraints Classifier

This is five commonly used classifiers for constraints classification: Logistic Regression, Naive Bayes Classifier, linear Support Vector Machine, non-linear Support Vector Machine, and Decision Tree.

## Contents

- [in/config.json](https://anonymous.4open.science/r/towards-automated-identification-of-data-constraints-8FC1/code/ML-constraints-classifier/in/config.json) - the config file is used to specify the configuration when conducting experiments.
- [ml-code/MLEXpr.py](https://anonymous.4open.science/r/towards-automated-identification-of-data-constraints-8FC1/code/ML-constraints-classifier/ml-code/MLExpr.py) - each class object represents each experiment configuration
- [ml-code/classifier.py](https://anonymous.4open.science/r/towards-automated-identification-of-data-constraints-8FC1/code/ML-constraints-classifier/ml-code/classifier.py) - launch five common classifiers and obtain machine learning results.
- [ml-code/feature_extractor.py](https://anonymous.4open.science/r/towards-automated-identification-of-data-constraints-8FC1/code/ML-constraints-classifier/ml-code/feature_extractor.py) - transform and concatenate the features extracted for machine learning.
- [ml-code/generator.py](https://anonymous.4open.science/r/towards-automated-identification-of-data-constraints-8FC1/code/ML-constraints-classifier/ml-code/generator.py) - generate the data needed to run the machine learning algorithm.
- [ml-code/util.py](https://anonymous.4open.science/r/towards-automated-identification-of-data-constraints-8FC1/code/ML-constraints-classifier/ml-code/util.py) - contain utility functions that are used across different parts of classifiers.

- [requirements.txt](https://anonymous.4open.science/r/towards-automated-identification-of-data-constraints-8FC1/code/ML-constraints-classifier/ml-code/requirements.txt) - generated *requirements.txt* file for any project based on imports.

## Usage

- Generate data that includes n-grams, and n-pos, it will output a `data.json` file under `$root/data`

  `python generator.py`

- Run classifier

  `python classifier.py`

- Example config

  ```json
  ...
  "experiment": [
          {
              "use_frag": false,
              "use_sent": false,
              "use_dispat": false,
              "use_operands": false,
              "use_ct": true,
              "models": [
                  "logisticRegression"
              ],
              "smote_ratio": null
          }
  ]
  ```

  



## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.



## License

[MIT](https://choosealicense.com/licenses/mit/)

