---
name: meeting-time-planner
description: Find a meeting time that works for people in different cities. Use when the user wants to schedule a call or meeting across time zones.
---

# Meeting time planner

1. Read [office-hours.md](office-hours.md) to get each office's working hours. For a city not listed there, assume 09:00 to 18:00 on weekdays.
2. Call `get_current_time` once for each city's time zone, to know today's date and each city's current UTC offset.
3. Find slots of the requested length that fall inside working hours in every city. If no slot fits, say so and propose the slot that leaves the fewest people outside their hours.
4. Propose at most three slots, as a table with one column per city showing the local time in 24-hour format.
5. Add one line naming anyone whose slot falls in the first or last hour of their day.
