This dataset contains two types of datasets:

1. Electrical events annotation: which shows electrical events captured at different granularities for different appliances
2. Multi-modal dataset: Smaller dataset where residents recorded their activity, across appliance usage, water consumption, occupancy etc.

#### Electrical events annotation

Event sequence was recorded on 4th August 2013. All times are Indian Standard Time (IST = GMT+5.5 hrs). Here ID refers to ID in the room. For example, if there are 4 identical fans in the room, it would suffice to label one of them, which may take ID from 1-4.

|Sno|Time|Floor|Room|Type|Specific|ID|Event|
|----|------|----|----|-----|-----|--------|----|
|1|12: 17|1|Big|Lighting|Tubelight|1|Turned ON|
|2|12: 18|1|Big|Lighting|Tubelight|1|Turned OFF|
|3|12: 19|1|Big|Fan|Ceiling fan|1|Turned ON|
|4|12: 20|1|Big|Fan|Ceiling fan|1|Turned OFF|
|5|12: 21|1|Big|Iron|Electric Iron|1|Turned ON|
|6|12: 25|1|Big|Iron|Electric Iron|1|Turned OFF|
|7|12: 26|1|Washing Area|Washing Machine|Washing Machine|1|Turned ON|
|8|12: 30|1|Washing Area|Washing Machine|Washing Machine|1|Turned OFF|
|9|12: 31|1|Small|Fan|Ceiling fan|1|Turned ON|
|10|12: 32|1|Small|Fan|Ceiling fan|1|Turned OFF|
|11|12: 33|1|Small|Lighting|Tubelight|1|Turned ON|
|12|12: 34|1|Small|Lighting|Tubelight|1|Turned OFF|
|13|12: 35|1|Small|Lighting|CFL|1|Turned ON|
|14|12: 36|1|Small|Lighting|CFL|1|Turned OFF|
|15|12: 37|1|Bathroom|Water Heating|Geyser|1|Turned ON|
|16|12: 39|1|Small|Charger|Laptop |1|Turned ON|
|17|12: 47|1|Bathroom|Water Heating|Geyser|1|Turned OFF|
|18|12: 50|1|Small|HVAC|AC|1|Turned ON|
|19|13: 15|1|Big|HVAC|AC|1|Turned ON|
|20|13: 23|1|Small|HVAC|AC|1|Turned OFF|
|21|13: 27|1|Big|HVAC|AC|1|Turned OFF|
|22|13: 29|1|Small|Charger|Laptop |1|Turned OFF|
|23|13: 31|1|Bathroom|Lighting|CFL|1|Turned ON|
|24|13: 32|1|Bathroom|Lighting|CFL|1|Turned OFF|
|25|13: 33|1|Bathroom|Lighting|Tubelight|1|Turned ON|
|26|13: 34|1|Bathroom|Lighting|Tubelight|1|Turned OFF|
|27|13: 35|1|Bathroom|Fan|Ceiling fan|1|Turned ON|
|28|13: 36|1|Bathroom|Fan|Ceiling fan|1|Turned OFF|
|29|13: 37|1|Bathroom|Lighting|Bulb|1|Turned ON|
|30|13: 38|1|Bathroom|Lighting|Bulb|1|Turned OFF|
|31|13: 39|2|Staircase|Lighting|CFL|1|Turned ON|
|32|13: 40|2|Staircase|Lighting|CFL|1|Turned OFF|
|33|13: 41|2|Store|Lighting|Bulb|1|Turned ON|
|34|13: 42|2|Store|Lighting|Bulb|1|Turned OFF|
|35|13: 43|2|Main|Lighting|Tubelight|1|Turned ON|
|36|13: 44|2|Main|Lighting|Tubelight|1|Turned OFF|
|37|13: 45|2|Main|Fan|Ceiling|1|Turned ON|
|38|13: 46|2|Main|Fan|Ceiling|1|Turned OFF|
|39|13: 47|2|Main|Lighting|CFL|1|Turned ON|
|40|13: 48|2|Main|Lighting|CFL|1|Turned OFF|
|41|13: 49|2|Main|Lighting|Bulb|1|Turned ON|
|42|13: 50|2|Main|Lighting|Bulb|1|Turned OFF|
|43|13: 51|2|Main|Lighting|Study table tubelight|1|Turned ON|
|44|13: 52|2|Main|Lighting|Study table tubelight|1|Turned OFF|
|45|13: 53|2|Bathroom|Lighting|Tubelight|1|Turned ON|
|46|13: 54|2|Bathroom|Lighting|Tubelight|1|Turned OFF|
|47|13: 55|2|Bathroom|Lighting|CFL|1|Turned ON|
|48|13: 56|2|Bathroom|Lighting|CFL|1|Turned OFF|
|49|13: 57|2|Bathroom|Fan|Exhaust fan|1|Turned ON|
|50|13: 58|2|Bathroom|Fan|Exhaust fan|1|Turned OFF|
|51|13: 59|1|Small|Charger|PhON|e|1|Turned ON|
|52|14: 00|1|Small|Charger|PhON|e|1|Turned OFF|
|53|14: 01|2|Bathroom|Water Heating|Geyser|1|Turned ON|
|54|14: 03|2|Bathroom|Water Heating|Geyser|1|Turned OFF|
|55|14: 04|1|Washing area|Ligting|Bulb|1|Turned ON|
|56|14: 05|1|Washing area|Ligting|Bulb|1|Turned OFF|
|57|14: 06|1|Veranda|Ligting|2 * Halogen|1|Turned ON|
|58|14: 07|1|Veranda|Ligting|2 * Halogen|1|Turned OFF|
|59|14: 08|0|Staircase|Lighting|CFL|1|Turned ON|
|60|14: 09|0|Staircase|Lighting|CFL|1|Turned OFF|
|61|14: 10|0|Big |Lighting|Tubelight|1|Turned ON|
|62|14: 11|0|Big |Lighting|Tubelight|1|Turned OFF|
|63|14: 12|0|Big|Fan|Ceiling Fan|1|ON| at speed 5|
|64|14: 13|0|Big|Fan|Ceiling Fan|1|ON| at Speed 4|
|65|14: 14|0|Big|Fan|Ceiling Fan|1|ON| at Speed 3|
|66|14: 15|0|Big|Fan|Ceiling Fan|1|ON| at Speed 2|
|67|14: 16|0|Big|Fan|Ceiling Fan|1|ON| at Speed 1|
|68|14: 17|0|Big|Fan|Ceiling Fan|1|Turned OFF|
|69|14: 18|0|Big|Ligting|Bulb|1|Turned ON|
|70|14: 19|0|Big|Ligting|Bulb|1|Turned OFF|
|71|14: 20|0|Big|TV|TV|1|Turned ON|
|72|14: 25|0|Big|TV|TV|1|Turned OFF|
|73|14: 42|0|Big|Ligthing|Tubelight|2|Turned ON|
|74|14: 43|0|Big|Ligthing|Tubelight|2|Turned OFF|
|75|14: 44|0|Store|Lighting|CFL|1|Turned ON|
|76|14: 45|0|Store|Lighting|CFL|1|Turned OFF|
|77|14: 46|0|Kitchen|Lighting|Tubelight|1|Turned ON|
|78|14: 47|0|Kitchen|Lighting|Tubelight|1|Turned OFF|
|79|14: 48|0|Kitchen|Microwave|Microwave|1|Turned ON|
|80|14: 52|0|Kitchen|Microwave|Microwave|1|Turned OFF|
|81|14: 53|0|Kitchen|Lighting|CFL|1|Turned ON|
|82|14: 54|0|Kitchen|Lighting|CFL|1|Turned OFF|
|83|14: 55|0|Small|Lighting|CFL|1|Turned ON|
|84|14: 56|0|Small|Lighting|CFL|1|Turned OFF|
|85|14: 57|0|Small|Fan|Ceiling Fan|1|Turned ON|
|86|14: 57: 30|0|Small|Fan|Ceiling Fan|1|Turned OFF|
|87|14: 58|0|Small|Lighting|Tubelight|1|Turned ON|
|88|14: 59|0|Small|Lighting|Tubelight|1|Turned OFF|
|89|15: 00|0|Bathroom|Lighting|CFL|1|Turned ON|
|90|15: 01|0|Bathroom|Lighting|CFL|1|Turned OFF|
|91|15: 02|0|Bathroom|Water heater|Geyser|1|Turned ON|
|92|15:  04|0|Bathroom|Water heater|Geyser|1|Turned OFF|
|93|15: 05|0|Bathroom|Lighting|CFL|2|Turned ON|
|94|15: 05: 10|0|Bathroom|Lighting|CFL|2|Turned OFF|
|95|15: 06|0|Washing area|Fan|Exhaust|1|Turned ON|
|96|15: 07|0|Washing area|Fan|Exhaust|1|Turned OFF|
|97|15: 08|0|Washing area|Lighting|CFL|1|Turned ON|
|98|15: 09|0|Washing area|Lighting|CFL|1|Turned OFF|
|99|15: 10|0|Kitchen|Mixer|Mixer|1|Turned ON|
|100|15: 11|0|Kitchen|Mixer|Mixer|1|Turned OFF|
|101|15: 12|0|Kitchen|Refrigerator|Refrigerator|1|Turned ON|


#### Multi-modal dataset

The instrumented home has 3 occupants- A, B and C. The following is a collection of events "recorded" to nearest proximity by the residents. The residents continues their routines and tried to record as many events as possible.

This dataset is of the form

    <-timestamp, [event1, event2, …]->
where

    event = <-person, object, action->

|Time|Event List|
|----|------|
|6:05 AM| [<-B, room 1 first floor, wake up->, <-B, bathroom second floor, flush->]|
|6:35 AM| [<-B, room 1 ground floor, enter->, <-B, room 1 ground floor,turn on light->]|
|7:27 AM| [<-A, room 2 first floor, wake up->, <-A, room 2 first floor, turn on light and laptop charger->]|
|7:29 AM| [<-A, washroom first floor, enter->, <-A, washroom first floor, turns on CFL->]|
|7:31 AM| [<-A, washroom first floor, turns off CFL->, <-A, room 2 first floor, enter->]|
|7:35 AM| [<-B, kitchen ground floor, enter->, <-B, kitchen ground floor, turns on mixer->, <-B, kitchen ground floor, turns off lights->]|
|7:35 AM| [<-C, room 1 ground floor, turns on light and fan->]|
|7:40 AM| [<-B, kitchen ground floor, enter->, <-B, kitchen ground floor, turn off mixer->]
|8:05 AM| [<-C, bathroom ground floor, enter->, <-C,bathroom ground floor, light on->]|
|8:06 AM| <-A, room 2 first floor, enter->, <-A, room 1 ground floor, turns off fan->], <-A, room 2 first floor, turn on fan->]|
|8:35 AM| [<-A, room 2 first floor, turns off fan->]|
|8:36 - 8:58 AM| [<-A, bathroom second floor, enter->, <-A, bathroom second floor, turns on CFL+ Fan-> , <-A, bathroom second floor, turns off CFL+ Fan->, <-A, room second floor, enter->,<-A, room second floor, light+fan on->, <-A, room second floor, light+fan off->]|
|8:59 AM| [<-A, room 2 first floor, enter->, <-A, room 2 first floor, turns on fan and laptop charger->]|
|9:42 AM| [<-C, room 1 ground floor, turns on TV->]|
|9:52 AM| [<-B, room 1 ground floor, turns off TV->]|
|9:53 AM| [<-A, room 2 first floor, turns off light, fan, laptop->, <-A, room 2 first floor, exit->, <-A, ground floor, enter->]|
|10:25 AM| [<-A, kitchen, takes water from water filter->]|
|10:30 AM| [<-A, wash basin ground floor,  washes hands->]|
|10:33 AM| [<-B, kitchen, CFL turned on->]|
|10:54 AM| [<-A, room 2 first floor, enter->, <-A, room 2 first floor, turns on light, fan, laptop->]|

