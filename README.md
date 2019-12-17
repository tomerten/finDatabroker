# FinDataBroker

FinDataBroker is a databroker that is aimed at working in combination with
[FinanceJSON](https://github.com/tomerten/financejson/), to ease the saving
and loading to different formats. In short
it is nothing else than a wrapper to save and load dicts of lists of dicts in a convenient
way. The motivation for this packages is to logically separate data storage and loading from 
packages analysing the data, reducing the complexity of the analysis packages.

The databroker package provides classes to save data stored in the 
the FinanceJSON format to the following storage systems:
- MongoDb
- Sqlite

In future versions the following formats will be added:
- JSON
- HDF5
- PostGreSQL
- ElasticSearch

When data is loaded back it is always returned as a dict, where the value
is a list of dicts. This way, when different of these loaded dicts are combined,
in a single dictionary, the overall dictionary is consistent with 
the [FinanceJSON schema](https://github.com/tomerten/financejson/financejson/schema.json)
and can be validated to check if all the loaded data is consistent, at
the same time making the tools of FinanceJSON available for this dataset.

## Requirements
- pymongo
- dataset


## Installation
````bash
pip install FinDataBroker
````

## Example

A FinanceJSON file for a stock:
```json
{
            "yh_symbol": [{"symbol": "XYZ"}],
            "ms_symbol": [{"symbol": "US_XYZ"}],
            "yh_assetProfile": [
                {
                    "index_symbol": "XYZ",
                    "date": "2019-01-01",
                    "address1": "foo",
                    "auditRisk": 1,
                    "boardRisk": 2,
                    "city": "bar",
                    "country": "a"
                }],
        }
```
 
 
# FinDataBroker CLI
[![Python 
Version](https://img.shields.io/pypi/pyversions/FinDataBroker)](https://pypi.org/project/FinDataBroker/)
[![PyPI](https://img.shields.io/pypi/v/FinDataBroker.svg)](https://pypi.org/project/FinDataBroker/)
[![CI](https://github.com/tomerten/FinDataBroker/workflows/CI/badge.svg)](https://github.com/tomerten/FinDataBroker/actions?query=workflow%3ACI)

This repository also contains a Python based commandline tool which is able 
validate and extract data from financeJSON files and written to the
selected database format. 

Write a financeJSON file to a mongodb:
```bash
FinDataBroker write2mongo /path/to/financejsonfile user:pwd@url:port databasename
```

Write a financeJSON file to an sqlite database:
```bash
FinDataBroker write2sqlite /path/to/financejsonfile sqlite:///database.db
```

## License
[GNU General Public License 
v3.0](https://github.com/andreasfelix/latticejson/blob/master/LICENSE)


