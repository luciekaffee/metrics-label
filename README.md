# Metrics Multilingual
Pipeline to analyse the multilinguality of a given semantic web dataset

This code is usable for any dataset containing triples (with graphs), to analyze it based on the following metrics:

- Completeness
- Efficient Accessibility
- Unambiguity
- Multilinguality
- MonolingualIsland
- Usage of Objects and whether those are labeled (LabelAndUsage)


Each of those metrics is a class in *labelMetrics*.

Each dataset has its own run file, given the metrics that's needed for the respective dataset.
E.g. Wikidata can not be analyzed with the metrics Efficient Accessibility as it does not contain multiple graphs.

The input is the dataset either as nt dump, or a gzipped nt dump.
The separator between the different elements of the triple can be specified in the call of each class (default is \t).

For especially big datasets, such as BTC, the whole dataset can be compressed, using the *Preprocessing* toolset.
Following this procedure, each part of the triple is compressed using python’s sha25 lib. Take care that following this, the language metrics can not be used as they expect unencrypted text.

To compare the language codes extracted by the Multilinguality, we compared them with https://gist.github.com/jrnk/8eb57b065ea0b098d571 and excluded all that are not in this list.
