# Events sync project
We aim to develop the functionality to update iAnn events using the TeSS web service. More information about the project coming soon.

## Installation
You will need **pip** to install the script requirements, [over here](https://pip.pypa.io/en/stable/installing/) you will find documentation about installing **pip** in your OS. The safer way to get your requirements installed without affecting any other Python project you have is using [**virtualenv**](http://docs.python-guide.org/en/latest/dev/virtualenvs/).
```{r, engine='bash', count_lines}
git clone https://github.com/elixirhub/events-sync-tess-to-iann.git
cd events-sync-tess-to-iann
viartualenv .venv
source activate .venv/bin/activate
pip install -r requirements.txt
```

After you finish the script execution you will need to deactivate your virtual environment:
```{r, engine='bash', count_lines}
deactivate
```

## Configuration
You can configure this script using one of this methods:

* Modifying the parameters in [docs/conf.py](https://github.com/elixirhub/events-sync-tess-to-iann/blob/master/docs/conf.py)
* Setting those same parameters as environment variables
* Passing them as options to the command line interface


>## Notice
>You will have to set at leats the following parameters: LOG_FILE, IANN_URL


## How to use
```{r, engine='bash', count_lines}
Usage: tess_to_iann.py [OPTIONS]

  ELIXIR TeSS to iAnn events synchronizer script V 0.0 Script to get TeSS
  events and push them to iAnn. It can be used as a batch process or as a
  daemon process.

Options:
  --delay INTEGER          Seconds between executions when the script is run
                           as a daemon (eg. 60)
  --log TEXT               Log file absolute path, if not defined will usethe
                           one on the conf.py (eg.
                           /Users/niceusername/logs/ny_log.txt)
  --tess_url TEXT          TeSS service URL, if not defined will use the one
                           on conf.py(eg. http://tess.elixir-uk.org/)
  --iann_url TEXT          iAnn Solr URL, if not defined will use the one on
                           conf.py(eg. http://localhost:8983/solr/iann)
  --daemonize              Flag to run the script as a daemon
  --include_expired        Flag to fetch expired events from TeSS
  --start TEXT             Start date (eg. 2000-01-01)
  --reset                  Flag to reset the Solr target instance and retrieve
                           all the TeSS events
                           BE CAREFUL!!! 
                           This option will erase all the events on iAnn and will do acomplete
                           fetch of the TeSS events.
  --daily_reset_time TEXT  Time of the day to do the Solr instance reset (eg.
                           10:30)
                           BE CAREFUL!!!
                           This option will erase all the events on iAnn and will do acomplete fetch of the
                           TeSS events.
  --help                   Show this message and exit.
```
>## Notice
>If you are using a virtual environment to manage your dependencies you will have to activate before running the script:

```{r, engine='bash', count_lines}
cd [SCRIPT_PATH]
source activate .venv/bin/activate
```
### Run as batch
```{r, engine='bash', count_lines}
python tess_to_iaan.py --start 2016-10-17
```
### Run as daemon
If you don't want to set a daily reset on your iAnn Solr instace you should run the script like this:
```{r, engine='bash', count_lines}
python tess_to_iaan.py --daemonize --delay 3600
```

If you want to reset your iAnn Solr instance every day at 23:00 you should run the script like this:

```{r, engine='bash', count_lines}
python tess_to_iann.py --daemonize --daily_reset_time 23:00 --delay 3600
```
This way the script will run every hour and in some time around 23:00 hours will be deleting all the iAnn events and doing a full fetch from TeSS.
