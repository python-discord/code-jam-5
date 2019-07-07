
<p align="center">
<img width="600" src="https://i.imgur.com/PMQv01Y.png">
</p>

Leafify is a simple, climate change / environment focused music player, which aims to encourage action against climate change/environmental crisis in a subtle but effective manner. The project allows you to play your music in a beautiful interface while also being reminded of interesting climate change facts. 

This is done in 3 ways: 

* A dedicated widget in the User Interface
* As advertisement segments in between songs
* An audio visualiser which shows the Earth being on fire, or glowing green depending on what is being played.

## Features Summary

* A environment-themed user interface;
* The ability to play songs from your local computer as you select them through a file browser; (the program will attempt to use `~/Music` as the root folder by default)
* Between each song, an audio ad is played. This audio ad is a climate change fact scraped from the web from a list of curated sources, then played using `gtts`.
* An audio visualizer circling around the Earth, which turns red for regular songs (to figure the earth burning, under the effect of impending global warming) and green for ads;
* An embedded fact widget which refreshes itself every 8 seconds. The facts shown here are fetched by the same components has the audio ads.

## Install & Use

Dependencies are stored in a `Pipfile`.

```
pipenv install && pipenv run setup-nlp
```
then, to start the application:
```
pipenv run start
```

## The music player

The music player contains 2 fundamental parts:
* The actual audio player
* The controls

### The audio player

The audio player was created using PyQt’s QMediaPlayer. The QMediaPlayer can be used as an easy way to play audio very quickly using code like the following

```python
player = QtMultimedia.QMediaPlayer()
media = QMediaContent(QUrl.fromLocalFile('song.mp3'))
player.setMedia(media)
player.play()
```

However, because of the adverts which had to play before each song, it made more sense to integrate a QMediaPlaylist, in which an advert and desired song are added together at the same time every time you want to play something.

### The controls

The controls are fairly simple, a play/pause button, seeker bar and a label for displaying the current time/duration. The seeker bar was created using a custom QProgressBar, which detected for QMouseEvents to allow the user to “seek” through the song. Also, the progress bar “knob” was created by overriding the paintEvent function and drawing a circle at the current value of the progress bar.

## The audio visualizer

The audio visualiser changes depending on what is being played. If an advert is being played, the audio visualiser will be green; if any other song is being played, the audio visualiser will be coloured as if the Earth is on fire (to represent global warming). The amplitudes are calculated in a QThread which are then passed to the main program using PyQt’s signal/slot mechanics.

### The calculations

The audio visualiser was created using an FFT (fast fourier transform) algorithm to calculate the amplitudes and frequencies of the samples. Using numpy and pydub, the values were calculated using the following method:

```python
from pydub import AudioSegment
import numpy as np

# the song is set to 1 channel so that it doesn’t contain duplicate samples
song = AudioSegment.from_file("sample.mp3").set_channels(1)
samples = np.array(song.get_array_of_samples)
# the fft algorithm calculates the amps and frequencies
fourier = np.fft.fft(samples)
frequencies = np.fft.fftfreq(fourier.size, d=song.duration)
amps = 2/samples.size * np.abs(fourier)
```

To learn more about FFTs go [here](https://www.nti-audio.com/en/support/know-how/fast-fourier-transform-fft).

### The visuals

The audio visualiser is displayed using polar coordinate formulae, if you didn’t know, you can plot into a circle very easily using the equations

```
y = rsinθ
x = rcosθ
```

Where `r` is the distance from the origin, and θ is the angle away from the positive x axis in the counterclockwise direction (in radians). Having x and y values makes it much easier to plot with Qt’s QPolygonF class as it uses cartesian coordinates to represent each point.

So plotting the visualiser in this way was quite easy as it allows you to let r = amplitude and plot them all with even intervals of θ.

## The fact aggregator

Our objective was to include facts in the user interface to entice the user to keep using the tool, and to present them with facts that would increase their awareness of the bigger problems today’s society is facing with climate change looming over.

We chose to source those facts from the web. We did not find tools such as APIs that would give us climate change facts, so we elected to scrape the data we needed from various websites that would allow for it through their ToS (or absence thereof) and for which scraping isn’t explicitly disallowed (robots.txt). Most of these websites usually sourced their data from external sources such as publicly available studies.

Such scraping is usually performed through HTTP requests and XPath queries. For that, we used `requests` to perform HTTP requests and `lxml` to parse the HTML and process XPath queries.

Because of the variety of sources, we needed to build a system that would allow us to manage sources with little overhead cost and to avoid writing redundant boilerplate code for each new source.

The said system we call HQuery. Its implementation can be found in `scrapetools/scrapetools/hquery.py`.

### Hquery

Hquery is simply a system that processes a query. This query takes the form of a dictionary, and each key in it points to the XPath expression which would result in the desired value:
```yaml
    loc: //a  # Select all ‘a’ tags in the HTML document
    body:
        href: @href  # For each element, retrieve its href attribute
        text: text()  # And its text content
```
The idea is to return a list of records (dictionaries), one for each element detected in the `loc` expression. For our case, imagine that `loc` points to a `li` element in which all the data we want about a climate change fact is found; for each such element, we may want to retrieve several values, as shown in the example above. This is also nestable, with the context location element passed down as we go deeper.

### Pipes

To increase the scope of this system, we added two things;
A top level namespace where one can place crucial elements such as the url to fetch and whether the GET request should be performed with Javascript support (`dynamic`);
 what we call pipe expressions, allowing us to insert processing steps in the query itself :

```yaml
url: http://www.cowspiracy.com/facts
dynamic: false
content:
  loc: //div[@class="sqs-block-content"]/h2/strong
  prefix: $ { single }
  finally: $ { filter:not_empty }
  body:
    content: $ { list, filter:sound, map:clean } text()
```
A pipe expression always either precedes a XPath query, or appears in one of the special query fields `prefix`, `postdict` or `finally`. It is structured as following:
```
$ A:B{ C,… } <XPath>
```
where `C` is a list of pipe identifiers delimited by commas, `A` is a higher-order mode and `B` a regular mode.

A pipe identifier can be a single identifier (`strip`), or can be passed through a higher-order pipe: `map:strip`. A XPath expression always returns a list of elements. A regular pipe is applied to the list as its target, whereas a `map:pipe` is applied to each element of said list. Pipe identifiers refer to functions that have been registered in the pipe dictionaries which you can find in `hquery.py`.

Modes are optional. A regular mode behaves like a pipe unit that stands at the end of the pipeline for the current expression, and higher-order modes are meant to alter the behavior of every unit in the pipeline:
```
$ m:{ strip, upper }
Is equivalent to
$ { map:strip, map:upper }
```

You can find out more details in `scrapetools/hquery.py`.

### New pipes & higher-order pipes

To easily extend the library of pipes available to use, we have implemented decorators `HierarchicalXPathQuery.pipe` and `HierarchicalXPathQuery.high_pipe` which allow you to easily register your own functions as pipe elements. They will be summonable under their associated nickname in a query you pass to the object that registered them.

```python
hxq = HierarchicalXPathQuery.from_yml('query.yml')

@hxq.pipe
def is_valid(item):
  return 'doctor' in item

# ...
$ { filter:is_valid } //li/text()
```

### QML WIdgets

To add on to this philosophy of least overhead cost on integrating new sources, we use Qt widgets written in QML to speed up the process. They represent a minor part of the Qt code written in this project, as they are meant to be simple.

They are found in the `qml` folder.

### Fact Factories

A `FactFactory` binds the previously mentioned concepts together. Each source has its own implementation. The dictionary records are fetched by a HQuery, then each fact can be passed down to a suitable QML widget, which is then sent to the UI which requested it, either on the user’s request, or on fact refresh time.

### Tags

Fact factories each have a set of tags which allows for selecting between facts that are more suited for the UI (such as the counters found at theworldcounts.com), or facts more suited to be played in audio (e.g. the facts found at cowspiracy.com).

## The ads

Audio ads are provided by the fact factories in the same fashion as for the UI facts.
Every song the user selects will first be preceded by an audio ad which read a fact aloud using `gtts`, a Python package which interfaces with Google Translate’s text-to-speech API. 


## Self-contained tools

**Hquery** is one of those. It should prove of use to more than just this situation.

**Resourcely** is a package we wrote to handle resource folders. It simply parses a config file where you list your resources (take a look at the `images` folder), and enables you to import them through the Python import system. Each resource is stored in a `Resource` object.

```
images:
  resources.yml
  next.png
  previous.png
  play.png
  pause.png
```
resources.yml:
```yaml
resources:
  type: namespace # must specify this to be considered a namespace
  buttons:
    Next: next.png
    Pause: pause.png
    Previous: previous.png
    Play: play.png
  icons:
    Logo: spotleafy.png
```

With just a few lines, you can open your resource folders to the rest of the package :
```python
import only_otters.resourcely as rly

from argparse import Namespace

__resources__: Namespace = rly.from_located_file(near=__file__)
rly.expand(__resources__, globals())
```

```python
from images import icons

window.setIcon(icons.Logo.url)
```

## Future features

To make the ads more relevant to increase user engagement, we wanted to implement a progress bar to which each heard ad would add progress to. At completion, a tree would be planted, in the same fashion [Ecosia](https://www.ecosia.org/) does. This would give the user a goal to look forward to, and entice them to continue using the application (A sense of accomplishment and all that).

