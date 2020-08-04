# ner_srv

Tiny Flask app for NE tagging with some additional features.

## Prerequisites

*Python 3* and *PyPI* packages `flask`, `mordl`, `textdistance`, `toxine`,
`transliterate`.

## Starting the Server

First, place storages of trained ***MorDL*** `UposTagger`, `FeatsTagger` and
`NeTagger` into `ner_srv/models` directory. Change the parameter `emb_path` in
`ds_config.json` file of every storage, so that that path became correct.
Note, that the root point for relative paths there is `ner_srv`. Thus, if your
embeddings also placed in the `ner_srv/models` directory, just add `'model/'`
in the beginning of each `emb_path` value.

Second, you may go back to the `ner_srv` directory and correct port in
`main.py` script.

After that, ensure that you're still in the `ner_srv` directory and run
```sh
sh ./run.sh prod
```

Or, if you need debug mode, run just
```sh
sh ./run.sh
```

## Usage

All services return data in *json* format.

```
http://<address>:<port>/api/tokenize/<text>
```
Returns *Parsed CoNLL-U* for tokenized **text** (untagged).

```
http://<address>:<port>/api/tag/<text>
```
Returns *Parsed CoNLL-U* with **text** tokenized and with *UPOS*, *FEATS* and
*MISC:NE* fields filled.

```
http://<address>:<port>/api/phonetize/<text>?level=3&syllables=false
```
Returns phonetized version of **text**. Only texts in Russian are processed
correctly.

**level**: the level of simplification. Allowed values:
- `0` means no changes at all but excess spaces;
- `1` removes all spaces;
- `2` most standard version of phonetization;
- `3` refined phonetization;
- `4` rude phonetization;
- `5` even more rude.
Default level is `3`.

**syllables**: if `true`, returns array of syllables instead of just **text**
phonetized. Default is `false`.

```
http://<address>:<port>/api/text-distance/<text1>/<text2>?ner1=&ner2=&level=3&algorithm=damerau_levenshtein&normalize=true&qval=1
```
Returns text distance between **text1** and **text2**. Only text in Russian
are processed correctly.

**ner1**: if specified, at the start, **text1** will be tokenized and tagged,
and then replaced by *FORM* fields of tokens that have **ner1** as value of
the *MISC:NE* field.

**ner2**: if specified, at the start, **text2** will be tokenized and tagged,
and then replaced by *FORM* fields of tokens that have **ner2** as value of
the *MISC:NE* field.

**level**: before calculating the distance, both **text1** and **text2** will
be phonetized with that level (see `api/phonetize` service).

**algorithm**: what method to use to calculate the distance. Allowed
values are: `hamming`, `levenshtein`, `damerau_levenshtein` (default),
`jaro`, `jaro_winkler`, `gotoh`, `smith_waterman`.

**normalize**: use normalized distance (default is `true`).

**qval**: use `1` (default).

## License

***ner_srv*** is released under the Apache License. See the
[LICENSE](https://github.com/fostroll/ner_srv/blob/master/LICENSE) file for
more details.
