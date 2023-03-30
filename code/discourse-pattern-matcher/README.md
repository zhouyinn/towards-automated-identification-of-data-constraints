# Discourse Pattern Matcher

This is a discourse pattern matcher which uses spaCy Matcher to identify the 15 discourse patterns, applying a set of linguistic features: part-of-speech tags, dependencies and entities.  



## Usage

- Discourse pattern matching & Operands extraction
  - Output:  `out_fragments.json`


```
python extractor.py -in ../../data/negative-sentences.csv
```

- Constraint type detection

``` python
python constype_to_fragment.py -in out_fragments.json
```



## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.



## License

[MIT](https://choosealicense.com/licenses/mit/)

