Script to convert newer MCNP inputs which have 'read file' cards into a single file for use with MCNPX 2.4.0, which is openly distributed. Can be useful in situations where people are waiting for license approval. Also will wrap lines at 80 characters iteratively, which can be useful when
dealing with inputs that have segmented volumes and column highlighting makes life easier.

Installation should place the script in your _userbase/bin_ folder, which hopefully is in your PATH, and then the script can simply be executed by name.  Running the example goes like this:

```bash
$ convert2singlefile.py sample.i sample_singlefile.i
```

Or one can run the ```run.sh``` script, which does the same thing.
