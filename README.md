# ner_srv

Tiny Flask app for NE tagging with some additional features.

## Starting the Server

First, place storages of trained ***MorDL*** `UposTagger`, `FeatsTagger` and
`NeTagger` into `ner_srv/models` directory. Change the parameter `emb_path` in
`ds_config.json` file of every storage, so that that path became correct.
Note, that the root point for relevant paths there is `ner_srv`. Thus, if your
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

```
http://\<server>:\<port>/api/phonetize/\<text>?level=\<level>&syllables=<true|false>
```

## License

***CORS API Proxy*** is released under the Apache License. See the
[LICENSE](https://github.com/fostroll/ner_srv/blob/master/LICENSE) file for
more details.
