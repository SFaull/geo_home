# Intro

This is a fork of https://github.com/mmillmor/geo_home
The original author limits the polling rate to once every 120s. This fork adds a configuration parameter that allows the user to choose the polling rate.
Default rate is 10s which is the maximum rate most devices report data.
Original readme continues below...

# Geo Home

Integrate with Geo Home smart meters in Home Assistant

## Instructions

To collect Geo Home smart meter data, you must have a WiFi connected
smart meter from Geo Together. If you have a smart meter that is not
WiFi connected by default, you can buy a WiFi module from 
Geo Together at https://geotogether.com/product-category/accessories/.

Once you have a WiFi connected smart meter, create an account on the Geo Home app. The username and password for this account are used to
connect the Geo Home integration.

After downloading the Geo Home integration into HACS, remember to install it by navigating to Settings -> Devices & services -> Add integration, then
select "Geo Home". You will be prompted for
a username and password. Enter the ones you created from the app. This will create Gas and Electricity sensors, tracking the lifetime
energy usage of your meters. If you get a 401 error, you may have entered the wrong credentials, or your account may be blocked for remote access. Unfortunately there is nothing we can do to resolve that.

## Energy Dashboard Configuration

To display Electricity in the energy dashboard, add sensor.electricity as your _Electricity Consumed Energy (kWh)_, and set _Use an entity tracking the total costs_ with a cost sensor of sensor.electricity_cost_today

To display Gas in the energy dashboard, add sensor.gas or sensor.gas_m3 as your _Gas usage_, and set _Use an entity tracking the total costs_ with a cost sensor of sensor.gas_cost_today


## Upgrading

If you are upgrading from version 1.2, the units of your cost sensors will have been £/kWh instead of GBP/kWh. You can go to https://my.home-assistant.io/redirect/developer_statistics to correct that
