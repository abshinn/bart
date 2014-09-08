bart
====

### Purpose

Access real-time BART train departures using python and the [Real Bart API](http://api.bart.gov/). I always have a terminal window open, so I wrote this little command-line tool just so I don't have to open up a browser window to check the BART schedule.

</br>

### Setup

Your very own BART API key is required and can be requested from [api.bart.gov](http://api.bart.gov/). Once obtained, name an environment variable named BART\_API\_KEY in your appropriate login script:

```bash
$ echo export BART_API_KEY=YOUR_KEY >> ~/.bash_profile
```

</br>

To use `bart` as I do in the terminal, alias `bart.py` by adding `alias bart="~/bart/./bart.py"` to your appropriate shell profile, or append by the following command:

```bash
$ echo alias bart="~/bart/./bart.py" >> ~/.bash_profile
```

To display the ETAs for north-bound trains at the 16th Street Mission station.

```bash
$ bart 16th n
```

```
Bart Service Status
	No delays reported.

16th St. Mission at 10:57:34 AM 
 Dublin/Pleasanton train in  6 minutes,
 Dublin/Pleasanton train in 20 minutes,
 Dublin/Pleasanton train in 35 minutes,
           Fremont train in 12 minutes,
           Fremont train in 27 minutes,
           Fremont train in 42 minutes,
Pittsburg/BayPoint train in  9 minutes,
Pittsburg/BayPoint train in 23 minutes,
Pittsburg/BayPoint train in 38 minutes,
          Richmond train in 15 minutes,
          Richmond train in 30 minutes,
          Richmond train in 46 minutes,
```

To automatically display the ETAs every minute, include the tracking flag.

```bash
$ bart civc s -t
```

</br>

### Pipe it!

Perfrom a numeric sort on the ETA field.

```bash
$ bart 16th n | tail +2 | sort -n -k4,4
```

Only show Richmond trains.

```bash
$ bart 19th n | grep Richmond
```

Say it.

```bash
$ bart plza s | say
```
