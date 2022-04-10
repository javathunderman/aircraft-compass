# Aircraft Compass

A SocketIO based web app to automatically move a compass needle in the direction of incoming
aircraft, based off of data obtained from a software defined radio (SDR) tuned to the ADS-B
radio band used by commercial aircraft transponders. 

Built in (less than) 24 hours at Bitcamp 2022. 

Special thanks to Dr. Marc Lichtman for his great workshop on SDRs and for letting me borrow equipment.

Completed: 
- Parsed ADS-B messages on 1.09 GHz radio band using the PlutoSDR and GNURadio. 
- Passed ADS-B messages through to Python Socket.IO server
- Obtained geolocation and heading data from individual users connected to the server
- Calculated (inaccurate) bearing angle between the two geolocations. 

TODO: 
- Actually move needle on web app
- Fix issue with incorrect bearing calculations
- Attach to a Raspberry Pi micro servo because that was the original plan anyway