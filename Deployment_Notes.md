21 May 2013
***

1. Router seems to have gone crazy. Not giving proper names to different hardware.
-Added as an issue currently.
2. Tested from hostel room if data is getting collected on the server. Unfortunately, 
for both smart meter and jPlug there was no data since a long time. RPi which was 
attached to the Smart Meter had lose Power, whereas jPlug is unresolved. 
-Need to buy Belkin extension cables asap.
+Providing SSH access was helpful in finding which system is working,
else coming to the lab and testing might have resulted in more data loss


22 May 2013
***

1. It was observed that monitoring process (which sends emails) was getting killed.
The reason behind the same is that internet was down and that exception was not handled.
This makes a stronger case of also using SMS based notifications and alerts in order
to be independent of frequent internet losses. Also, exception handling was added.


23 May 2013
***

Today i took all the stuff home. It is actually a lot of stuff. As of 22:19 the following has
been configured:

1. Router: 3 routers have been bridged. The main router is connected to the modem. As such, internet
is pathetic. Need to work on GSM based notifications asap else if we wait for internet to be up,
lot of data loss might occur. Another solution is to ensure that local mail servers are used.
The details of how to setup routers will be added in How To section. Also had removed AP capabilities
of ADSL modem
2. Desktop (Main server): A lot of cables to moved, but still the easiest part of the puzzle. Reserved 
an IP for it in the address table.
3. Smart Meter and RPi: Most of the stuff had already been done before. Just replaced the
older system with the newer one and everything just worked.
4. Phones: Charged them all very quickly using Belkin DC powered USB (Idea courtesy Manoj). 
On some phones the time was way different from the current time. Need to look into this, since
i think time will go out of sync mutiple time. Has been added as an issue for the repo.
5. jPlug: Once, Twice and .. don't know how many times did i set them up in the day. They 
would keep on dying every now and then.
6. Water Meter: The plumber came and we found that the tank has a thicker pipe, so we 
would need a newer meter. Last time, shipping took a lot of time, so efforts (trip
to Chawri)  would be needed to ensure that timely deployment. Plumber would do the
fitting on Saturday morning.
7. Zwave based stuff. Could not get it to work. Since internet was pathetic, could not
download some required packages. 
8. Testing PIR on RPi: Could not get sufficient time to do it today, goes in TODO for
tomorrow.

24 May 2013
***

7 AM
1. Internet continues to be pathetic. Hardly any time when it works. MTNL!
2. All jPlug were dead when i woke up. Thought for some time and felt that maybe i tried
to optimize the server side PHP script and forgot that jPlug will work ONLY the way it does!
Put everything in adhoc mode and set everything up again. Now jPlugs didn't die of their own.
Next, i tested if they would work after electricity failure, so just turned off the power
and turned it back on. IT DOES NOT WORK. Another few hours of effort wasted. Clueless!
Next step i am taking is to try and disable MAC binding for a particular jPlug and see if
it works.
3. Smart Meter and Raspberry Pi worked throughout. They survived a power failure and have
reported all the data so far without any hiccup.

9 AM
4. Smart meter data collection was stopped. Log says: Input/ Output Error [5]. Absence of a 
traceback hurts now! Don't know exactly what caused the issue. Also i need to add a script in 
every RPi etc. to ensure that all it's scripts for data collection, uploading are working.
If not, explicitly start them. Adding this as a high priority issue. 
5. All jPlugs dead now. Accidentally turned off power. Would call Radio Labs to figure out
what is going on.
6. Plug Computer does not have the required s/w. With "blazing" fast internet, may take years 
to download all the s/w required to run the ZWave stuff.
7. Found contact details of the vendor for Water Meter. Factory in Faridabad. Can give it a try
to call them and ask them if they can deliver asap.
8. Yet Another issue (enhancement). Filename started with 0 for smart meter data collection.
Since all the data had been cleaned. Should not cause any problems, but should be avoided.

10 AM
9. We felt jPlug could be giving issues due to MAC binding. This was something we had not
done in the lab. Removed the MAC binding. Still on power reset jPlug won't work.

11 AM
10. This time tried configuring only the n/w settings of jPlug. And then see if it would
work after reset. Again no success. 

12:25 PM
11. Even electrician is amazed! Nothing works. Motor fitting when removed direct on/off to
socket type resets the jPlug. Don't know what's the fault- jPlug or connection. Also experienced
last night when i plugged in my latop charger in running jPlug and it also reset. Then, i felt 
i did something wrong. But, now i am not sure if jPlug handles this case.
12. No scope of inverter points. That would really mess up the entire home, which i think clearly is 
not needed. Battery backup for RPi working for collecting Water data seems like a plausible solution.
 
25 May 2013
***

11 AM
1. Water meter fitting going on. A lot of scope for non intrusive sensors, 
which can just attach to the pipe without the need to breaking anything.
2. Tried setting up jPlug with MTNL AP. Thought maybe something we did wrong
with the way we set up bridging. But alas, doesn't work even with it after 
turning off. 3 LED's blink which according to their documentation means that
IP is not being assigned. 

4 PM
3. One water meter installed. Tested in the noon at low pressure. Was giving 
proper pulse.
4. Range is not an issue for Zwave stuff. Tested even with closing the door.
Currently the power cable to Zwave devices is broken. Need to solder rather 
than weakly taping.
5. Placed 5 Multisensors at different locations in home. Put a doc showing
mapping between room and node id. ZWave stuff working fine for now. Need
to write sripts to upload data to main server.
6. Started data collection on phones also. Also turned on bluetooth for
the 3 occupants rooms.
 
26 May 2013
***

1. Woke up and saw that some of the phones ran out of juice overnight! Pretty bad,
need to perpetually charge them. Also need to create a mapping of phone to location.
2. ZWave stuff was still working. But probably error in upload script cost data loss.
Looking into it.
3. RasPi was not on n/w. Data collection was still working. Just removed ethernet cable
and put it back. It was again back on attached devices page.

27 May 2013
***

1. Got the second water meter installed. Gives a pulse every 10 l. Tested with RPi
and were able to detect the pulse. Cabling and installing in ~45 degrees without cover
is tough! Moreover, had to drill through window to bring the data cable down.
SADLY there is a decrease in water pressure from tank
2. Similarly tested with RPi for the water meter connected with motor. Works fine.
3. Motor remains an issue and can't use it with jPlug. Got a phase loop out. Would
test with Current Cost to see if it works. Had tested it in lab earlier. Should work.
4. For jPlug Deepak told that maybe putting new MPFS image might work. Tried the same
without success.
5. Bought multiplugs for charging phones
6. Put CT's in ground panel. For some reason didn't work. Manoj felt maybe we got more
current than expected
7. Overall an extremely tiring day. Output fairly limited
Walkie Talkie might be useful in such deployments :-)

28 May 2013
***

1. Electricity again tripped in the night. I turned off my AC. Eventually woke up 
at 2:30
2. Saw the data from Multisensor. Feel that something is wrong. It is maybe wrongly
detecting presence
3. The long CAT 5 cable prepared seems a little short. Would put it for now.
Put the Water tank RPi on LAN and ran the currently adhoc program to display rising/
falling edges.
4. Internet woes continue. The risk of getting a new fitting is that whatever works
might stop!
5. Reduced joins coming to Electric Meter, should reduce the noise
6. Again got the same error in Electric Meter script. Checked the logs.
At exactly the same point dmesg logs show that ttyUSB0 disconnected and ttyUSB1 
connected. Anyone has ideas why this may happen?
7. Tested motor consumption with Current Cost. It consumes ~685W. From previous 
tests, i recall that CC shows about 10-15 W less than jPlug. How critical is this 
calibration. Moreover, the 433 MHz communication works across 2 floors, so that is
some good news. CC sends readings every 6 s. But only the real power.
8. Observing false positives from Water Meter. Hard to say where the fault lies.
The s/w looks for a rising edge followed by a falling edge. New issue created 
to this effect containing more information about the same.

29-31 May
***

1. Current Cost now send data directly to the server
2. jPlugs reprogrammed and thicker wires put for heavier loads. Put up a mapping
of jPlug ID to Appliance Name in configuration folder
3. 


15 June
***

1. A post after 15 days! Its been so many days yet not fully stabilized
2. Water meter seems to be stable
3. Electricity meter is stable
4. Phone data collection was stopped on some phones
5. Zwave data looks good, will need a lot of post processing, but cant do more
with current sensors
6. Didnt look into CT data today, need to look it today
7. Took an image of "glowing" setup in night (with/without) flash.
Confirms findings in Hitchiker..., LED's can be troublesome for 
occupant, in this case I suffer!
8. Current cost is working
9. Water meter data from motor NOT working. Script stopped, will look into early tomorrow morning
