# ztm-warsaw-timetable-parser

Parsing script for data from Warsaw's public transit authority. If you need GTFS look [here at MKuran's work](https://github.com/MKuranowski/WarsawGTFS).

This converts from Warsaw's proprietary format to my proprietary™ format thats json based.
This includes (in `output/`):
- `stop_groups.json` - list of all stops and related data
- `routes.json` - descripton of bus and tram routes
- `timetables.json` - departure times for each stop on each route. Useful since you can serve this directly to users with little processing. Also includes symbols and their explanations, as well as other 'comments' normally left on a physical timetable.
- `stop_times.json` - a simple dump of all stops of each trip. Analogous to GTFS's `stop_times.txt`.
- `calendar.json` - lists what type of day each line runs on today.
- `brigades.json` - connects `trip_id`s to brigades to use with realtime data, aswell as headings from their online API that includes headings to depots.

`brigades.json` is in beta right now!

This format preserves more information about the data, like above mentioned symbols and their explenations, but also descriptive stop locations (street name or 'under bridge'), general travel directions from stops (this stop has busses towards X), road names on route, detailed information about semi-permament detours, permament route changes and shortened routes.
This is very specific to Warsaw transit authority and their setup.
As a bonus (or a penalty?) it includes timetables for every stop on every route already pre-proccessed for you!

However, it lacks `frequencies.txt`, line coloring, and universal adoption of GTFS. (possibly more if you want to include station layouts that dont exist for Warsaw and their somewhat advanced fare system)

Coverage of data from source open data is at about 75ish%

## Usage
To generate static files (everything except `brigades.json`) you will use `python parser.py`. *Generally* it *should* work out of the box and download everything for you. There is helpful `-h` flag that shows some options (like not generating some files, or using patrticular file)

For `brigades.json` you need to create `apikey.txt` that contains just your apikey from [api.um.warszawa.pl](api.um.warszawa.pl). After that it *should* work on its own just by running first running the static portion, as this depends on it, and then `python brigades.py`. Again, `-h` is available for more options.

