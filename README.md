# GIST v3.0

An OMOP CDM Based Automatic Clinical Trial Generalizability Assessment Framework.


## Table of Content
- [Installation](#installation)
- [Usage](#usage)
- [Config](#config)
- [Main Packages Used](#main-packages-used)
- [Notes](#notes)
    - [Entities](#entities)
- [Databases](#databases)
    - [Criteria Database](#criteria-database)
    - [EHR Database](#ehr-database)
- [Previous Implementation](#previous-implementation)
- [Paper](#paper)
- [Contributing](#contributing)
- [License](#license)

## Installation

1. Clone this [repository](https://github.com/thisisibrahimd/gist).

```bash
git clone https://github.com/thisisibrahimd/gist.git
cd gist
```

2. Create a [virtual env](https://docs.python.org/3/library/venv.html).

```bash
python3 -m venv venv
source venv/bin/activate
```

3. Use the package manager [pip](https://pip.pypa.io/en/stable/) to install dependencies.

```bash
pip3 install -r requirements.txt
```

4. Install gist cli (this will allow you run the ```gist``` command instead of ```python3 gist/cli.py``` .

```bash
pip3 install --editable .
```

## Usage

By default, gist automatically grabs the following environment variables
```
GIST_DEBUG # boolean
GIST_EHR_CONN_STR # postgresql://username:password@hostname:port/database
GIST_CRIT_CONN_STR # postgresql://username:password@hostname:port/database
GIST_TRIAL_IDS # space delimited trial ids
```

Run trial NCT02885496 showing debug output

```bash
gist --debug --trial_id NCT02885496
```

Run trial NCT02885496 and NCT00562356 with out debug output

```bash
gist -t NCT02885496 -t NCT00562356
```

Run trial NCT02885496 and NCT00562356 with trial ids and debug env placed in .env. When all options/arguments are placed in the .env, you can just run ```gist``` in the terminal.

```bash
gist
```

## Config

GIST needs two [postgresql connection strings]((https://docs.sqlalchemy.org/en/14/core/engines.html#database-urls)) in your environment variables.

An example .env file to place in root

```bash
GIST_DEBUG=True
GIST_EHR_CONN_STR=postgresql://username:password@hostname:port/database
GIST_CRIT_CONN_STR=postgresql://username:password@hostname:port/database
GIST_TRIAL_IDS=NCT02885496 NCT00562356
```

## Main Packages used

- [```Click```](https://click.palletsprojects.com/en/7.x/) to create the cli interface
- [```sqlalchemy```](https://www.sqlalchemy.org/) as an ORM to simplify query generation 
- [```python-dotenv```](https://pypi.org/project/python-dotenv/) to automatically grab envs from .env file(s).

## Notes

### Entities

Entities were generated with ```sqlacodegen``` and modifiyed to allowed for subqueryload of ehr data in the person entity.

```python
condition_occurrence = relationship('ConditionOccurrence')
drug_exposure = relationship('DrugExposure')
procedure_occurrence = relationship('ProcedureOccurrence')
measurement = relationship('Measurement')
observation = relationship('Observation')
```

## Databases

### Criteria Database

GIST reads criteria in a certain schema. ddl can be found in the repo linked below.

[criteria database](https://github.com/thisisibrahimd/gist-criteria)

### EHR Database

GIST currently supports OMOP CDM 5.2.2. It may work with later version but not for certain.

An [synpuf database](https://github.com/thisisibrahimd/synpuf) has been made available to test with gist.

## Previous Implementation

- [```MATLAB```](https://github.com/ChunhuaWeng/GIST-2.0-for-Population-Representativeness-Measurement)
- [```JavaScript```](https://github.com/thisisibrahimd/GIST-2.0-JS) version 2
- [```Javascript```](https://github.com/WengLab-InformaticsResearch/GIST) version 3
- [```C#```](https://github.com/thisisibrahimd/gist-skeleton) implementation with no interface

## Paper

- [GIST 2.0: A scalable multi-trait metric for quantifying population representativeness of individual clinical studies](https://www.sciencedirect.com/science/article/pii/S1532046416301150)
- [A knowledge base of clinical trial eligibility criteria](https://www.sciencedirect.com/science/article/abs/pii/S1532046421001003)

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License
[Apache 2.0](http://www.apache.org/licenses/LICENSE-2.0)
