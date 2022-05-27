# zaptec

## Business questions to be answered

### Question 1:  What can we infer from the charging behaviour of different drivers?

### Question 2:  Does the data suggest any value-added services that EV Charging Point Operators (CPO) might consider offering in the future?

### Question 3:  What charging pattern should EV owners adopt in order to extend the lifetime of their vehicle's battery?






business insights:
- projected power grid load as number of EVs grows over time?
- 
- how are the charging session start and end times distributed across the different EVs?  What conclusions can we draw from this?

- can we predict the electrical power demand for EV charging at the site for a given day of the week and hour in the day, based on historical EV charge patterns?

- during the period that a given EV is cable-connected to the charger (aka a "session"), how much power is actually drawn during the low- and high-tariff time windows?  What's the potential cost saving for the EV owner that could have been realized simply by making the charging periods (the time periods that the EV actually draws power from the charger) smarter?  Do price incentives work?

- When session stops with "externally ended", that is when the charging cable was disconnedted from the vehicle, and this is probably also the time that the vehicle leaves the garage.  what can we do with this info?  eg entry and exit times into and from the garage corresponding to cable-connected cable-disconnected.

- what can we infer from the energy that is charged during a session and the corresponding end-time of the previous session and the start time of the current session?  For example, how many kWh the vehcile charges may be an indication of how many kilometers were driven between charging session?  

- What kind of vehicle is it?  Plug-in hybrid, or bare-electric?

- What is the likely size of the battery?

- 



Data wrangling approach:
1.  need to anonymize the data, as the data is actual real-life data from an existing CPO installation.




- 
- 


Sample use of Zaptec API

Zaptec is a Norwegian manufacturer of charging stations for Electric Vehicles (EV), for consumer and industrial use

Find the Swagger-based documentation of Zaptec API here:  https://api.zaptec.com/help/index.html

zaptec.py contains a sample use of the Zaptec API, in order to allow creating reports on Zaptec installations.

Calling the Zaptec API requires a user token with permissions on a given Zaptec installation.


The integration to the Zaptec API is explained in this document:
https://zaptec.com/downloads/ZapChargerPro_Integration.pdf

Add OCPP reference documentation


