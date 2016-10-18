# Events sync project
We aim to develop the functionality to update iAnn events using the TeSS web service. More inforamtion about the project coming soon.

## Installation
You will need **pip** to install the script requirements, [over here](https://pip.pypa.io/en/stable/installing/) you will find documentation about installing **pip** in your OS. the safer way to get your requirements installed without afecting any other Python project you have is using [**virtualenv**](http://docs.python-guide.org/en/latest/dev/virtualenvs/).
```{r, engine='bash', count_lines}
git clone https://github.com/elixirhub/events-sync-tess-to-iann.git
cd events-sync-tess-to-iann
viartualenv .venv
source activate .venv/bin/activate
pip install -r requirements.txt
```
## Configuration
You can configure this script using one of this methods:

* Modifying the parameters in [docs/conf.py](https://github.com/elixirhub/events-sync-tess-to-iann/blob/master/docs/conf.py)
* Setting those same parameters as eviroment variables
* Passing them as options to the command line interface

## How to use
```{r, engine='bash', count_lines}
Usage: tess_to_iann.py [OPTIONS]

  ELIXIR TeSS to iAnn events synchronizer script V 0.0 Script to get TeSS
  events and push them to iAnn. It can be used as a batch process or as a
  daemon process.

Options:
  --delay INTEGER    Seconds between executions when the script is run as a
                     daemon
  --log TEXT         Log file path, if not defined will use the one on the
                     conf.py
  --tess_url TEXT    TeSS service URL, if not defined will use the one on
                     conf.py
  --iann_url TEXT    iAnn Solr URL, if not defined will use the one on conf.py
  --daemonize        Flag to run the script as a daemon
  --include_expired  Flag to fetch expired events from TeSS
  --start TEXT       Start date
  --help             Show this message and exit.
```
### Run as batch
```{r, engine='bash', count_lines}
python tess_to_iaan.py --start 2016-10-17
```
### Run as daemon
```{r, engine='bash', count_lines}
python tess_to_iaan.py --daemonize --delay 3600
```
