# Georgia 2020 precinct-level data
The results directory contains data from all precincts in Georgia, grouped by contest.
Note that in some cases, the same contest may appear with slightly different names in the source files, in which case results will be split across files - be careful.

## Data source
* XML data for each county was downloaded as XML from https://results.enr.clarityelections.com/GA/105369/web.264614/#/reporting
* XML data used is in the count-xml file - you'll need to decompress it before parsing.
* Data has been pivoted, denormalized, consolidated, and grouped by contest.
* A data version timestamp is retained in each file, though it's important to note multiple raw XML files contributed to each contest file.