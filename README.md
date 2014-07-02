bart
====

### Purpose

Access real-time BART train departures using python and the [Real Bart API](http://api.bart.gov/). I always have a terminal window open, so I wrote this little command-line tool just so I don't have to open up a browser window to check the BART schedule.

</br>

### Setup and Use

A BART API key is required and easily obtained from bart.gov. Once obtained, name an environment variable named BART\_API\_KEY in your appropriate login script, like so:

```bash
$ echo export BART_API_KEY=YOUR_KEY >> ~/.bash_profile
```

</br>

Personally, I alias the python script for easy access within the terminal shell.

```bash
$ echo alias bart="~/bart/./stn.py" >> ~/.bash_profile
```

To display the ETAs for north-bound trains for the 16th Street Mission station:

```bash
$ bart 16th n
16th St. Mission at 03:20:06 PM 
 Dublin/Pleasanton train in 13 minutes,
 Dublin/Pleasanton train in 28 minutes,
 Dublin/Pleasanton train in 43 minutes,
           Fremont train in  7 minutes,
           Fremont train in 25 minutes,
           Fremont train in 37 minutes,
Pittsburg/BayPoint train   now Leaving,
Pittsburg/BayPoint train in 15 minutes,
Pittsburg/BayPoint train in 30 minutes,
          Richmond train in  8 minutes,
          Richmond train in 23 minutes,
          Richmond train in 39 minutes,
```

To automatically display the ETAs every minute, add the tracking flag:

```bash
$ bart civc s -t
```

</br>

### Pipe it!

Sort on ETA field.

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
