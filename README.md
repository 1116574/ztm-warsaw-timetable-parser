# ztm-warsaw-timetable-parser

Parsing script for data from Warsaw's public transit authority. If you need GTFS look [here at MKuran's work](https://github.com/MKuranowski/WarsawGTFS).

This converts from Warsaw's proprietary format to my proprietary™ format thats json based.
This includes (in `output/`):
- `routes.json` - descripton of bus and tram routes
- `stop_groups.json` - list of all stops and related data
- `timetables.json` - departure times for each stop on each route. Useful since you can serve this directly to users with little processing.
- `symbols.json` - some trips are special, like to depot, extended trip to schools etc. They are marked with letters next to them like `m` or `s` or even `#`. This file maps `trip_id`s to those symbols and (in the future) their human readable description

This format preserves more information about the data, like above mentioned symbols and (in the future) theirs explenations, but also descriptive stop locations (street name or 'under bridge'), general travel directions from stops (this stop has busses towords X), road names on route, detailed information about semi-permament detours, permament route changes and shortened routes.
This is very specific to Warsaw transit authority and their setup.
As a bonus (or a penalty?) it includes timetables for every stop on every route already pre-proccessed for you!
However, it lacks `frequencies.txt`, line coloring, and (for now) `stop_times.txt` of GTFS.

This doesnt include any GPS data (...for now? We'll see)
