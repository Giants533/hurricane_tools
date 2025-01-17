import numpy as np
from scipy.interpolate import griddata
from scipy.integrate import trapz, simps

from .distance import latlon2distance
from .interpolate import FastGriddata


__all__ = [
    'interp_circle',
    'interp_circle_closure',
    'circular_avg',
    'circular_avg_closure',
    'rmw',
    'axisymmetricity',
    'axisymmetricity_closure'
]


def _interp_circle_xy_closure(X, Y, cx, cy, radius, theta, dxdy):
    """interpolating data on the circle for cartesain coordinate"""
    def inner(values):
        raise ValueError("This function is not finished yet")


def _interp_circle_lonlat_closure(lon, lat, clon, clat, radius, theta, dxdy, **kwargs):
    """interpolating data on the circle for lon/lat coordinate"""
    dx, dy = dxdy
    nums_r = radius.size
    nums_t = theta.size
    
    # the meridional/zonal distance between center and every grid points
    dist_lon = latlon2distance(clon, lat, lon, lat)    # (ny, nx)
    dist_lat = latlon2distance(lon, clat, lon, lat)
    dist_full = np.sqrt(dist_lon**2 + dist_lat**2)
    
    # give signs to dist_lon/lat (west of `clon` or south of `clat` would be negative)
    dist_lon[lon < clon] *= -1
    dist_lat[lat < clat] *= -1
    
    # set a box area to reduce the amount of computation
    max_r = radius.max()
    L_lon = int(max_r // dx) + 6
    L_lat = int(max_r // dy) + 6
    cix = np.unravel_index(dist_full.argmin(), dist_full.shape)  # (nearly) center index
    box_slice = (slice(cix[0]-L_lat, cix[0]+L_lat), slice(cix[1]-L_lon, cix[1]+L_lon))
    dist_lon_b = dist_lon[box_slice]
    dist_lat_b = dist_lat[box_slice]
    
    # reshape into interpolation form
    dist_lonlat_b = np.vstack((dist_lon_b.ravel(), dist_lat_b.ravel())).T
    
    # construct circular samples points and interpolate
    circle_pts = np.zeros((nums_t*nums_r, 2))
    circle_pts[:,0] = radius.repeat(nums_t) * np.cos(np.tile(theta, nums_r))
    circle_pts[:,1] = radius.repeat(nums_t) * np.sin(np.tile(theta, nums_r))
    
    # FastGriddata instance
    fgd_obj = FastGriddata(dist_lonlat_b, circle_pts)
    
    def inner(values):
        values_b = values[box_slice]
        val_b = values_b.ravel()
        interp = fgd_obj.interpolate(val_b)
        return interp.reshape(nums_r, nums_t)
    
    return inner
    

def interp_circle(X, Y, values, cx, cy, radius, theta=None, dxdy=None, coord='lonlat'):
    """
    Interpolating data on the circles.
    
    Parameters:
    ----------
    X, Y: 2-d array, shape = (ny, nx)
        The coordinates of the `values`.
    values: 2-d array, shape = (ny, nx)
        Values on `X` and `Y` coordinate.
    cx, cy: scalar
        Center coordinate of the circle.
    radius: scalar or 1-d array-like, shape = (nradius,)
        The radius of circles.
    theta: 1-d array, shape = (ntheta,). Optional
        The angles (radians) of each sampled points on the circle.
        Default is np.arange(*np.deg2rad([0, 360, 1])), the whole circle.
        Examples:
        >>> theta = np.arange(*np.deg2rad([0, 360, 1]))   # whole circle
        >>> theta = np.arange(*np.deg2rad([0, 180, 1]))   # upper half circle
        >>> theta = np.arange(*np.deg2rad([90, 270, 10]))   # left half circle, coarser samples
    dxdy: 2-elements tuple, (dx, dy). Optional
        Spatial resolution. 
        Default is None, and it would automatically derived based on `X` and `Y`.
    coord: str, 'lonlat' or 'xy'. Optional
        The coordinate system of `X` and `Y`.
        If coord = `xy`, then `X` and `Y` are cartesain coordinate.
        If coord = 'lonlat', then `X` and `Y` are longtitude and latitude.
        Default is `lonlat`.       
        
    Return:
    ------
    Interpolating result, shape = (nradius, ntheta)
    """
    interp_func = interp_circle_closure(X, Y, cx, cy, radius, theta, dxdy, coord)
    return interp_func(values)


def interp_circle_closure(X, Y, cx, cy, radius, theta=None, dxdy=None, coord='lonlat'):
    """
    Return a function, which can interpolate data on the circle.
    
    The Returned function accept a argument `values`, the data values on the `X` and `Y`
    coordinate.
    
    These two methods are almost the same:
    >>> # method 1: using `interp_circle` twice
    >>> X, Y, cx, cy, radius, values1, values2 = get_fake_data()
    >>> res1 = interp_circle(X, Y, values1, cx, cy, radius)
    >>> res2 = interp_circle(X, Y, values2, cx, cy, radius)
    >>>
    >>> # method 2: using `interp_circle_closure`
    >>> interp_func = interp_circle_closure(X, Y, cx, cy, radius)
    >>> res1 = interp_func(values1)
    >>> res2 = interp_func(values2)
    
    But the method 2 (using `interp_circle_closure`) is faster because it avoids some repeated 
    calculations.
    
    Parameters:
    ----------
    X, Y, cx, cy, radius, theta, dxdy, coord:
        See `interp_circle`
        
    Return:
    ------
    A function, which its argument is `values` (see `interp_circle`).
    """
    # convert `radius` to iterable
    if isinstance(radius, (int, float)):
        radius = np.array([radius])
    elif isinstance(radius, list):
        radius = np.array(radius)
    
    if theta is None:
        theta = np.arange(*np.deg2rad([0, 360, 1]))
    
    if coord == 'xy':
        if dxdy is None:
            dx = X[0,1] - X[0,0]
            dy = Y[1,0] - Y[0,0]
            dxdy = (dx, dy)
        return _interp_circle_xy_closure(X, Y, cx, cy, radius, theta, dxdy)
    
    elif coord == 'lonlat':
        if dxdy is None:
            dx = latlon2distance(X[0,0], Y[0,0], X[0,1], Y[0,0])
            dy = latlon2distance(X[0,0], Y[0,0], X[0,0], Y[1,0])
            dxdy = (dx, dy)
        return _interp_circle_lonlat_closure(X, Y, cx, cy, radius, theta, dxdy)
    
    else:
        raise ValueError(f"Unavailable coord: {coord}. It shold be 'lonlat' or 'xy'.")


def circular_avg(lon, lat, values, clon, clat, radius, theta=None, dxdy=None):
    """
    Calculate circular mean.
    
    Parameters:
    ----------
    lon, lat: 2-d array, shape=(ny, nx)
        The lon/lat coordinates of `values`.
    values: 2-d array, shape=(ny, nx)
        Data values
    clon, clat: scaler
        The center coordinates of circular mean.
    radius: scaler or 1-d array-like
        The radius of circles. Unit is km.
    theta: 1-d array
        The angles (radians) of each sampled points on the circle.
        See `interp_circle`
        Default is np.arange(*np.deg2rad([0, 360, 1])), the whole circle.
    dxdy: 2-elements tuple, (dx, dy). Optional
        Spatial resolution. 
        Default is None, and it would automatically derive dx and dy besed on `lon`
        and `lat`.
            
    Returns:
    -------
    The circular average result on each radius, shape = (len(radius),)
        
    NOTE:
    ----
    If this function is used repeatly, and all parameters remain the same except `values`, it is 
    worth to use `circular_avg_closure` instead. `circular_avg_closure` returns a closure function
    which only use `values` as its parameter.
    """
    res = interp_circle(lon, lat, values, clon, clat, radius, theta, dxdy, 'lonlat')
    return res.mean(axis=1)


def circular_avg_closure(lon, lat, clon, clat, radius, theta=None, dxdy=None):
    """
    Return a closure function to calculate circular mean.
    
    This function is very similar to `circular_avg`, while this function returns
    a closure function which use `values` as its parameters.
    This is suitable for the situations which needed to calculate circular mean
    repeatly, and only `vaules` are different, all other parameters remain the same.
    
    Parameters:
    ----------
    See `circular_avg`
    
    Returs:
    ------
    A closure function, which its parameter is `values` and return the calculation
    result (see `circular_avg` for `values`).
    
    Example:
    -------
    >>> # using `circular_avg`
    >>> res1 = circular_avg(lon, lat, val1, clon, clat, radius)
    >>> res2 = circular_avg(lon, lat, val2, clon, clat, radius)
    >>> 
    >>> # using `circular_avg_closure`
    >>> cavg_func = circular_avg_closure(lon, lat, clon, clat, radius)
    >>> res1_closure = cavg_func(val1)
    >>> res2_closure = cavg_func(val2)
    >>> 
    >>> np.allclose(res1, res1_closure)
    True
    >>> np.allclose(res2, res2_closure)
    True
    """
    nums_r = radius.size
    nums_t = 360 if theta is None else theta.size    # 360 is the default setting in `interp_circle_closure`
    interp_func = interp_circle_closure(lon, lat, clon, clat, radius, theta, dxdy, 'lonlat')
    
    def inner(values):
        return interp_func(values).reshape(nums_r, nums_t).mean(axis=1)
    
    return inner


def rmw(lon, lat, ws, clon, clat, maxdist=None, dr=None, dxdy=None):
    """
    Find TC RMW
    
    Paramters
    ---------
    lon, lat : 2d array, shape = (ny, nx)
        Longtitude / latitude
    ws : 2d array, shape = (ny, nx)
        Wind speed
    clon, clat : scalar
        TC center longtitude / latitude
    maxdist : scalar. Optional
        The maximum search distance (km)
    dr : scalar. Optional
        The radius (km) interval
    dxdy : Tuple(dy_scalar, dx_scalar). Optional
        Spatial resolution.
        
    Return
    ------
    rmw : scalar
        Radius of maximum wind speed
    """
    # find appropriate `maxdist`
    n = 5
    slc = (slice(n, -n), slice(n, -n))
    dist_x = latlon2distance(clon, lat[slc], lon[slc], lat[slc])
    dist_y = latlon2distance(lon[slc], clat, lon[slc], lat[slc])
    _maxdist = min(dist_x.max(), dist_y.max())
    
    if maxdist is None:
        maxdist = _maxdist
    elif maxdist > _maxdist:
        warnings.warn(f"`maxdist` is too large. Replace with {_maxdist:.2f}.")
        maxdist = _maxdist
    
    # find appropriate `dr`
    if dxdy is None:
        dx = latlon2distance(lon[:,1:], lat[:,1:], lon[:,:-1], lat[:,:-1]).mean()
        dy = latlon2distance(lon[1:,:], lat[1:,:], lon[:-1,:], lat[:-1,:]).mean()
    else:
        dx, dy = dxdy
                        
    if dr is None: 
        dr = max(dx, dy)
        
    # interpolate
    radius = np.arange(0, maxdist, dr)
    axisym_ws = circular_avg(lon, lat, ws, clon, clat, radius, dxdy=(dx, dy))
    return radius[axisym_ws.argmax()]


def axisymmetricity(lon, lat, var, radius, clon, clat, dxdy=None, integ='trapz'):
    """
    Calculate axisymmetricity based on Miyamoto and Takemi (2013).
    
    Parameter:
    ---------
    lon, lat : 2d array, shape = (ny, nx)
        Longtitude / latitude
    var : 2d array, shape = (ny, nx)
        The variable used in the calculation of axissymmetricity, e.g: wind speed.
    radius : 1d array, shape = (nr,)
        The radius of circles. Unit is km.
    clon, clat: scaler
        The center longtitude / latitude of TC.
    dxdy : 2 element tuple, (dx, dy).
        Spatial resolution. Default is None, and it would find the dx and dy automatically
        based on `lon` and `lat`.
    integ : str, {'trapz', 'simps'}.
        Numerical integration method. 'trapz' is trapezoidal method, and `simps` is Simpson’s
        method. 
        See scipy document: https://reurl.cc/X6KpYD
        
    Return:
    ------
    1d array with shape = (nr,). The axisymmetricity at the given radius.
    
    Reference
    ---------
    [1] Yoshiaki Miyamoto and Tetsuya Takemi: "A Transition Mechanism for the Spontaneous 
        Axisymmetric Intensification of Tropical Cyclones"
        J. Atmos. Sci, 70, 112-129
        https://doi.org/10.1175/JAS-D-11-0285.1
    """
    axis_func = axisymmetricity_closure(lon, lat, radius, clon, clat, dxdy, integ)
    return axis_func(var)


def axisymmetricity_closure(lon, lat, radius, clon, clat, dxdy=None, integ='trapz'):
    """
    Return a closure function to calculate axisymmetricity (Miyamoto and Takemi 2013).
    
    This function is very similar to `axisymmetricity`, while this function returns
    a closure function which use `var` as its parameters.
    This is suitable for the situations which needed to calculate axisymmetricity
    repeatly, and only `var` are different, all other parameters remain the same.
    
    Parameters:
    ----------
    See `axisymmetricity`
    
    Returs:
    ------
    A closure function, which its parameter is `var` and return the calculation
    result (see `axisymmetricity` for `var`).
    """
    if integ == 'trapz':
        int_func = trapz
    elif integ == 'simps':
        int_func = simps
    else:
        raise ValueError(f'Unavailable `integ`: {integ}. It should be "trapz" or "simps".')
    
    if dxdy is None:
        dx = latlon2distance(lon[0,0], lat[0,0], lon[0,1], lat[0,0])
        dy = latlon2distance(lon[0,0], lat[0,0], lon[0,0], lat[1,0])
        dxdy = (dx, dy)
        
    theta = np.arange(*np.deg2rad([0, 360, 1]))
    dtheta = theta[1] - theta[0]
    
    interp_func = interp_circle_closure(lon, lat, clon, clat, radius, theta, dxdy, coord='lonlat')
    
    def inner(var):
        interp = interp_func(var)
        ciravg = interp.mean(axis=1)    # (n_radius,)
        cirdev = interp - ciravg[:,np.newaxis]    # (n_radius, n_theta)
        res = ciravg**2 / (ciravg**2 + int_func(cirdev**2, dx=dtheta, axis=1) / (2*np.pi))    # (n_radius,)
        return res
    
    return inner