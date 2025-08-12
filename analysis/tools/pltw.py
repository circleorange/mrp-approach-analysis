import numpy as np
import matplotlib.pyplot as plt

def plot_on_ax(ax, x, y, z, ttl, xlbl, ylbl, zlbl, kwargs, zones, fticks, vlines):

    if x is None: # >>>>> Evaluate x axis >>>>>
        if isinstance(y, list): x = np.arange(y[0].shape[0])
        else: x = np.arange(y.shape[0]) if y is not None else np.arange(z.shape[0])

    if y is None: # >>>>> Evaluate y axis >>>>>
        if z is not None: y = np.arange(z.shape[1]) if z.ndim > 1 else np.arange(z.shape[0])
        else: y = x

    # >>>>> Set plot metadata and options >>>>>

    if 'xscale' in kwargs:
        xscaling = kwargs.pop('xscale')
        ax.set_xscale(xscaling)

    if 'yscale' in kwargs:
        yscaling = kwargs.pop('yscale')
        ax.set_yscale(yscaling)

    vlines_defaults = {'color': 'red', 'linestyle': '--', 'linewidth': 1, 'alpha': 0.8}
    if 'vlines' in kwargs:
        vlines_opts = kwargs.pop('vlines')
        vlines_defaults.update(vlines_opts)

    if fticks is not None:
        step_size = fticks # Smaller shrinks, i.e. 1 = 1 tick at start, np.ceil(arr).astype(int)
        yticks = np.arange(min(y), 
                           max(y), 
                           step=(np.ceil((max(y)-min(y))).astype(int) // step_size)) 
        xticks = np.arange(min(x), 
                           len(x), 
                           step=(len(x) // step_size))
        if step_size > 20: ax.tick_params(axis='x', rotation=45)
        ax.set_xticks(xticks)
        ax.set_yticks(yticks)

    if ttl: ax.set_title(ttl)
    if xlbl: ax.set_xlabel(xlbl)
    if ylbl: ax.set_ylabel(ylbl)
    ax.margins(0)
    ax.grid(zorder=0)

    if zones: # >>>>> Plot zones (Optional) >>>>>

        default_zone_opts = {'color': 'grey', 'alpha': 0.3, 'zorder': 0}
        for x_start, x_end in zones:
            ax.axvspan(x_start, x_end, **default_zone_opts)

    if z is None: # >>>>> Handle Use Case - 1D array >>>>>

        fill_between = kwargs.pop('fill', False) if kwargs else False
        if fill_between: ax.fill_between(x, y, color='skyblue', alpha=0.5)

        ptype = kwargs.pop('ptype', 'line') if kwargs else 'line'

        plot_defaults = {}
        if kwargs is not None: plot_defaults.update(kwargs)

        if ptype == 'scatter': ax.scatter(x, y, **plot_defaults)
        elif ptype == 'hist': ax.hist(y, bins=x, **plot_defaults)
        else: ax.plot(x, y, **plot_defaults)
        if 'label' in plot_defaults: ax.legend(loc='upper right')

    else: # >>>>> Handle Use Case - 2D array as B-scan image >>>>>

        print(f"plot_on_ax - Processed zdata_df: {z.shape}, xdata: {x.shape}, ydata: {y.shape}")
        default_opts = {'aspect': 'auto', 'origin': 'lower'}
        if kwargs is not None: default_opts.update(kwargs)
        im = ax.imshow(z.T, **default_opts)
        if zlbl: plt.colorbar(im, ax=ax, label=zlbl)

    if vlines: # >>>>> Draw vertical lines >>>>>
        for vline in vlines:
            ax.axvline(vline, **vlines_defaults)

def fig(plots, plt_height=4, ttl=None, glob_zones=None):
    """
    Create a figure of subplots and call plot_on_ax for each one.

    Example:
        > pltw.fig(
        >   title="traces RMS", 
        >   plots=[
        >       pltw.subplot(ylabel="traces", y=traces),
        >       pltw.subplot(ylabel="traces RMS", y=traces_rms),
        >   ],
        >   kwargs=[
        >       {"color": 'brown'},
        >       {"color": 'green', "linestyle": '--', "label": f'Mean RMS: {traces_rms_mean[0]:.4f}'},
        >   ]),
    """
    nrows = len(plots)
    ncols = 1
    figsize = (14, plt_height * nrows)
    fig, axes = plt.subplots(nrows=nrows, ncols=ncols, figsize=figsize, squeeze=False)
    axes_flat = axes.flatten() # flatten axes to iterate

    for ax, subpargs in zip(axes_flat, plots): # Each args dict should include keys for plot_on_ax, except 'ax'
        add_zones_globally = False
        if glob_zones is not None: 
            subpargs = {**subpargs, 'zones': glob_zones} # inject zones globally
            add_zones_globally = True
    
        y = subpargs.get('y') # Retrieve data for single plot in the list
        kwargs = subpargs.get('kwargs')

        # >>>>> Handle multiple ydata series >>>>>
        if isinstance(y, (list, tuple)):
            
            if not isinstance(kwargs, (list, tuple)): plot_kwargs_list = [kwargs] * len(y)
            else: plot_kwargs_list = list(kwargs) + [None] * (len(y) - len(kwargs))

            print(f"multiplot - Using {len(y)} ydata series with plot_kwargs_list: {plot_kwargs_list}")

            for y_series, kw in zip(y, plot_kwargs_list):
                if not add_zones_globally: subpargs.update({'zones': None})
                add_zones_globally = False # Only inject zones once

                calls_args = {**subpargs, 'y': y_series, 'kwargs': kw}
                plot_on_ax(ax=ax, **calls_args)

        # >>>>> Single ydata series, plot directly >>>>>
        else: plot_on_ax(ax=ax, **subpargs)

    for ax in axes_flat[nrows:]: ax.set_visible(False) # turn off any unused subplots
    if ttl is not None: fig.suptitle(ttl, fontsize=14)
    # add margin between subplots
    plt.tight_layout(rect=[0, 0, 1, 0.95]) # leave space for suptitle

def plot(x=None,y=None,z=None,ttl=None,xlbl=None,ylbl=None,zlbl=None,kwargs=None,zones=None,fticks=None,vlines=None):
    return {
        "x": x, "y": y, "z": z,
        "ttl": ttl, "xlbl": xlbl, "ylbl": ylbl, "zlbl": zlbl,
        "kwargs": kwargs, "zones": zones, "fticks": fticks, "vlines": vlines
        }
