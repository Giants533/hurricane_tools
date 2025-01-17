# hurricane_tools
documents of all modules -> `./documents`


axisym_vortex
------
[document](./documents/axisym_vortex.md) 

| Function / Class | Description |
| :--------------- | :---------- |
| <font color="#a77864"> **rankine_vortex** </font> | Classic rankine vortex. |
| <font color="#a77864"> **holland80** </font> | The empirical formula of TC axisymmetric structure by Holland (1980). |
| <font color="#a77864"> **willoughby04** </font> | The empirical formula of TC axisymmetric structure by Willoughby (2006). |


******
bst_parser
------
[document](./documents/bst_parser.md) 

| Function / Class | Description |
| :--------------- | :---------- |
| <font color="#a77864"> **DownloadWarning** </font> |  |
| <font color="#a77864"> **JMAbstParser** </font> | Parse JMA best track information. |


******
center
------
[document](./documents/center.md) 

| Function / Class | Description |
| :--------------- | :---------- |
| <font color="#a77864"> **tc_center_mslp** </font> | Find TC center by minimum sea level pressure grid (no weighted). |
| <font color="#a77864"> **weighted_tc_center** </font> | Calculate TC center by weighted method. |


******
circular
------
[document](./documents/circular.md) 

| Function / Class | Description |
| :--------------- | :---------- |
| <font color="#a77864"> **interp_circle** </font> | Interpolating data on the circles. |
| <font color="#a77864"> **interp_circle_closure** </font> | Return a function, which can interpolate data on the circle. |
| <font color="#a77864"> **circular_avg** </font> | Calculate circular mean. |
| <font color="#a77864"> **circular_avg_closure** </font> | Return a closure function to calculate circular mean. |
| <font color="#a77864"> **rmw** </font> | Find TC RMW |
| <font color="#a77864"> **axisymmetricity** </font> | Calculate axisymmetricity based on Miyamoto and Takemi (2013). |
| <font color="#a77864"> **axisymmetricity_closure** </font> | Return a closure function to calculate axisymmetricity (Miyamoto and Takemi 2013). |


******
destag
------
[document](./documents/destag.md) 

| Function / Class | Description |
| :--------------- | :---------- |
| <font color="#a77864"> **destagger** </font> | Convert variable from staggered to unstagger grid. |


******
distance
------
[document](./documents/distance.md) 

| Function / Class | Description |
| :--------------- | :---------- |
| <font color="#a77864"> **latlon2distance** </font> | calculate the distance (km) of two positions |
| <font color="#a77864"> **find_lonlat_with_distance** </font> | Find the longtitude/latitude which the horizontal or vertical distance to the (clon, clat) is equal to 'distance'. |


******
fourier
------
[document](./documents/fourier.md) 

| Function / Class | Description |
| :--------------- | :---------- |
| <font color="#a77864"> **interp_xy_closure** </font> | Same as `interp_xy`, but return a closure function to perform the interpolation. |
| <font color="#a77864"> **interp_xy** </font> | Interpolating data from radius-theta coordinate to x-y coordinate. |
| <font color="#a77864"> **CircularFourier** </font> | Perform Fourier transformation on circles. |


******
getvar
------
[document](./documents/getvar.md) 

| Function / Class | Description |
| :--------------- | :---------- |
| <font color="#a77864"> **GetVar** </font> | Get variables. It is similar to `wrf.getvar` by wrf-python, but here I store every intermediate variables, reduce the amount of function calling and rewrite the fortran functions to speed up. |
| <font color="#a77864"> **Interpz3d** </font> | Interpolating variables on specified vertical coordinate. |


******
interpolate
------
[document](./documents/interpolate.md) 

| Function / Class | Description |
| :--------------- | :---------- |
| <font color="#a77864"> **FastGriddata** </font> | Faster version of scipy.interpolate.griddata (in repeatly interpolating case). |


******
parse_wrf_center_mesg
------
[document](./documents/parse_wrf_center_mesg.md) 

| Function / Class | Description |
| :--------------- | :---------- |
| <font color="#a77864"> **parse_wrf_rsl_error** </font> | Parse `rsl.error.0000` outputed from WRF to get the center information. If parse file successfully, it would create `center.txt` in the current folder. |
| <font color="#a77864"> **find_centers_nearest_time** </font> | Find the hurricane center data at specific times from the file which contains center information based on WRF rsl.error.0000. |


******
plot
------
[document](./documents/plot.md) 

| Function / Class | Description |
| :--------------- | :---------- |
| <font color="#a77864"> **CWBcmapDBZ** </font> | Colormap, colors, contour levels and norm of CWB dbz pictures. |
| <font color="#a77864"> **CWBcmapRain** </font> | Colormap, colors, contour levels and norm of CWB accumulated daily/hourly rainfall pictures. |


******
pseudo_coord
------
[document](./documents/pseudo_coord.md) 

| Function / Class | Description |
| :--------------- | :---------- |
| <font color="#a77864"> **lonlat2xy** </font> | Convert to distance-based coordinate. |
| <font color="#a77864"> **xy2lonlat** </font> | Convert to longtitude-latitude coordinate. |


******
specialvar
------
[document](./documents/specialvar.md) 

| Function / Class | Description |
| :--------------- | :---------- |
| <font color="#a77864"> **inertial_stability_xy** </font> | Calculate (cyclinic) inertial stability at x-y (longtitude-latitude) coordinate. |
| <font color="#a77864"> **inertial_stability_rt** </font> | Calculate (cyclinic) inertial stability at cylindrical (radius-theta) coordinate. |


******
temporary
------
[document](./documents/temporary.md) 

| Function / Class | Description |
| :--------------- | :---------- |
| <font color="#a77864"> **TemporaryObj** </font> | Using this instance to collecte some temporary variables. |


******
transform
------
[document](./documents/transform.md) 

| Function / Class | Description |
| :--------------- | :---------- |
| <font color="#a77864"> **uv2vrvt_rt** </font> | Calculate Vr (radial wind) and Vt (tangential wind) on r-theta coordinate (polar coordinate). |
| <font color="#a77864"> **uv2vrvt_xy** </font> | Calculate Vr (radial wind) and Vt (tangential wind) on cartesian coordinate. |


******