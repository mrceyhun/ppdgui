#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Author      : Ceyhun Uzunoglu <ceyhunuzngl AT gmail [DOT] com>
Description : PyROOT functionalities
"""
import functools
import logging
from typing import List, Dict, Union

from ROOT import TFile, TBufferJSON, TCanvas, THStack, TLegend

from . import utils
from backend.api_v1.models import ResponsePlot, ResponsePlotsDict, ResponseGroup, ResponseMain
from backend.config import get_config, ConfigPlotsGroup
from backend.dqm_meta.client import get_dqm_store
from backend.dqm_meta.models import DqmMeta

# Allowed histogram classes
stack_allowed_classes = ["TH1F"]
DRAW_OPTIONS = get_config().plots.draw_options
logging.basicConfig(level=get_config().loglevel.upper())


# TODO: limit era numbers (get min era run count, or average, etc.)

# Your Bible: https://root.cern.ch/doc/master/classTDirectoryFile.html


@functools.lru_cache(maxsize=1000, typed=False)  # Caches responses, params are hashabel so it works
def util_read_group_plots_of_one_run_from_root_file(
    group_config: ConfigPlotsGroup, dqm_meta: DqmMeta
) -> Union[ResponsePlotsDict, None]:
    """Returns a group histogram JSONs of one run

    Reading all plots of a group for one run is the most efficient way because all plots are in one ROOT file.
    They are read from ROOT file, added proper metadata and added to ResponsePlotsDict which is plot name:data dict.

    Notes:
    - ROOT file path is fetched from DQM Metadata client which provides DqmMeta object for a group_directory and run.
    - Histograms' object paths are defined in the config and are formatted using run number coming from DQM metadata.
    - A plot required dqm_link which needs to be formatted with dataset and run number.

    Args:
        group_config: Config of the group to iterate the plots of it
        dqm_meta: DQM metadata to get root file, dataset, era, run
    Returns:
        ResponsePlotsDict: dict of {key: plot name(name in the config), value: its ResponsePlot object}
    """
    try:
        group_plots_dicts = {}  # ResponsePlotsDict()  # {plot name: its data}
        with TFile(dqm_meta.root_file, "read") as tf:
            logging.debug(f"TFile={dqm_meta.root_file}")

            # Iterate all histograms defined in the plots config for the group
            for plot_conf in group_config.plots:
                obj_path = utils.get_formatted_hist_path(
                    tdirectory=group_config.tdirectory, name=plot_conf.name, run=dqm_meta.run
                )
                logging.debug(f"Hist obj path: {obj_path}")

                # Get hist object
                assumed_hist = tf.Get(obj_path)

                if not assumed_hist.IsZombie():
                    # Class Name is important to define histogram as 1D, 2D
                    assumed_hist_class = str(assumed_hist.ClassName()).strip()

                    # Create hist url from dataset and run number
                    hist_dqm_url = utils.get_formatted_hist_dqm_url(
                        conf_url=plot_conf.dqm_link, dataset=dqm_meta.dataset, run=dqm_meta.run
                    )
                    name = str(assumed_hist.GetName())

                    # keep in mind that hash can be negative too which includes dash in str
                    _id = "id" + str(hash(name))

                    data = ""
                    try:
                        data = str(TBufferJSON.ToJSON(assumed_hist))  # create json from the obj
                    except Exception as e:
                        logging.warning(f"Histogram json convert failed. obj path:{obj_path}, error: {str(e)}")

                    # Add ResponsePlot to ResponsePlotsDict with the key of plot's name in the plots.yaml config file
                    group_plots_dicts[plot_conf.name] = ResponsePlot(
                        id=_id,
                        data=data,
                        dqm_url=hist_dqm_url,
                        draw_option=DRAW_OPTIONS[assumed_hist_class],  # draw option depends on histogram class
                        hist_name=name,
                        conf_name=plot_conf.name,
                        run=dqm_meta.run,
                        type=assumed_hist_class,
                    )
                else:
                    logging.warning(f"Zombie friend => file: {dqm_meta.root_file}, obj path: {obj_path}")

        if group_plots_dicts:
            return ResponsePlotsDict(group_plots_dicts)
    except Exception as e:
        logging.warning(f"Cannot read root => file: {dqm_meta.root_file}, obj path: {obj_path}. error: {str(e)}")


def util_overlay_runs_data_of_one_hist_to_single_thstack(
    runs_data_of_one_hist: List[ResponsePlot], run_era_map: Dict[int, str]
) -> ResponsePlot:
    """Overlay/stack same histogram's different runs/eras data using THStack TCanvas

    In ROOT, overlay is possible using THStack. Histograms with different color and line style are added to the THStack
    and appropriate TLegend is created for each of them. Final result is TCanvas JSON to be drawn by JSROOT.

    Args:
        runs_data_of_one_hist: As its name emphasizes, list of histograms data that of same histogram but from different runs.
        run_era_map: Dictionary of run:era, includes only the runs of the given histograms.
    Notes:
        - If there are multiple ERAs, LineStyle will be defined by era. If there is one era, LineStyle will be defined by the Run number.
        - Color will be different for all runs which means all eras too.
    """
    # Used to set Line Style, their index defines their styles
    unique_eras = list(set(run_era_map.values()))

    # Create THStack
    ths = THStack()
    # Create legend, ref https://gist.github.com/skaplanhex/55982ed5ddcc966dfc2d
    leg = TLegend(0.7, 0.7, 0.9, 0.9)  # x0, y0, x1, y1
    leg.SetBorderSize(1)
    leg.SetFillColor(0)
    leg.SetTextFont(42)
    # leg.SetFillStyle(0)
    # leg.SetTextSize(0.35)

    c = TCanvas()
    line_style_and_width_num = 1  # will control both line style and line width(boldness) depending on ERA count
    line_color_num = 2  # will control line color of RUNS if there is only 1 ERA. 1 is black, so starts from 2
    title = ""
    for hist in runs_data_of_one_hist:
        # Get ROOT object from its JSON
        if not hist.data:
            continue
        hist_root_obj = TBufferJSON.ConvertFromJSON(hist.data)

        # Get meta
        run = hist.run
        title = str(hist_root_obj.GetTitle()).strip()

        # Differentiate to look better in Stack. Check refs: https://root.cern.ch/doc/master/classTAttLine.html
        if len(unique_eras) <= 1:
            # If ERA count is 1, set different line style, line width and line color for each RUN
            hist_root_obj.SetLineStyle(line_style_and_width_num)
            hist_root_obj.SetLineWidth(line_style_and_width_num)
            hist_root_obj.SetLineColor(line_color_num)
        else:
            # Set different LineStyle for each RUN of ERA. ERA RUNS will have same colors but different shapes.
            hist_root_obj.SetLineStyle(line_style_and_width_num)
            # If ERA count is greater than 1, set same color for same era. ROOT style numbers start from 1 and colors start from 1.
            # Find the ERA of run and find its index in unique_eras list and assign LineColor according to its index in ERAs list.
            era_index_of_run = unique_eras.index(run_era_map[run]) + 1
            hist_root_obj.SetLineColor(era_index_of_run + 1)  # Start colors from 2, because 1 is black
            # Set the LineWidth(Boldness) depends on ERA name
            hist_root_obj.SetLineWidth(era_index_of_run)

        leg.AddEntry(hist_root_obj, run_era_map[run] + "-" + str(run), "l")
        ths.Add(hist_root_obj)

        line_style_and_width_num += 1
        line_color_num += 1

    ths.SetName(runs_data_of_one_hist[0].conf_name)  # Set THStack histogram name same as histograms
    ths.SetTitle(title)  # Set THStack histogram title same as histograms
    ths.Draw("nostack,hist")
    leg.Draw()
    c.Draw()  # Required to get all objects in "c" JSON

    # Data will be empty string in case of error while getting THStack json
    data = ""
    try:
        data = str(TBufferJSON.ToJSON(c))
    except Exception as e:
        logging.warning(f"THSack convert to json failed error: {str(e)}")

    return ResponsePlot(
        id=runs_data_of_one_hist[0].id,
        data=data,
        dqm_url=runs_data_of_one_hist[0].dqm_url,
        draw_opt=DRAW_OPTIONS["THStack"],
        hist_name=runs_data_of_one_hist[0].hist_name,
        conf_name=runs_data_of_one_hist[0].conf_name,
        run=0,  # it is overlaid with runs
        type="THStack",
    )


def util_overlay_group_hists(
    group_config: ConfigPlotsGroup, runs_plots: List[ResponsePlotsDict], run_era_map: Dict[int, str]
) -> List[ResponsePlot]:
    """Overlay all histograms of a group

    Args:
        group_config: plots config of a group
        runs_plots: All runs data of a group. Each item is dict {hist name: ResponsePlot(its data)} of one run.
        run_era_map:
    """
    resp_overlaid_group_hists = []
    for single_plot_config in group_config.plots:
        # Get same histogram's json data in each run
        list_of_runs_data_of_same_histogram = [plots_of_run[single_plot_config.name] for plots_of_run in runs_plots]
        if list_of_runs_data_of_same_histogram:
            resp_overlaid_group_hists.append(
                util_overlay_runs_data_of_one_hist_to_single_thstack(
                    runs_data_of_one_hist=list_of_runs_data_of_same_histogram, run_era_map=run_era_map
                )
            )
    return resp_overlaid_group_hists


def get_group_histograms(group_conf: ConfigPlotsGroup, run_era_map: Dict[int, str]) -> ResponseGroup:
    """Returns a group's histograms either overlaid or raw

    Notes:
        - If there is one run in the runs list, response will be raw histogram JSONs including TH2F(2D)
        - If there are more than one run, response is overlaid histograms from these runs and their ERAs
    Args:
        group_conf: plots config of a group
        run_era_map: dict of run:era
    """
    conf = get_config()
    dqm_store_client = get_dqm_store(config=conf)
    runs = run_era_map.keys()
    # Dict of run: List[ResponsePlot] to easily overlay them
    raw_runs_plots = []

    # Iterate runs and get their jsons
    for run in sorted(runs, reverse=True):
        group_dqm_meta = dqm_store_client.get_meta_by_group_and_run(
            group_directory=group_conf.eos_directory, run_num=run
        )
        if not group_dqm_meta:
            continue  # Skip if this group and run is not in DQM metadata

        group_runs_hists = util_read_group_plots_of_one_run_from_root_file(group_conf, group_dqm_meta)
        if group_runs_hists:
            raw_runs_plots.append(group_runs_hists)

    if len(runs) == 1:
        # RAW: Return raw histogram jsons including 2D
        plots = raw_runs_plots[0].get_plots_only()
    else:
        # OVERLAID: If there are more than 1 run, it means return overlaid
        plots = util_overlay_group_hists(group_config=group_conf, runs_plots=raw_runs_plots, run_era_map=run_era_map)

    return ResponseGroup(group_name=group_conf.group_name, plots=plots)


def get_histograms(runs: List[int] | None = None, groups: List[str] = None, eras: List[str] = None) -> ResponseMain:
    """Main function to get all histograms with provided filters

    Args:
        runs: Requested runs data
        groups: Requested groups data, None means all groups
        eras: Requested ERAs data, None means all ERAs
    """
    logging.debug(f"Params: eras: {eras}, runs:{runs}, groups: {groups}")

    conf = get_config()
    dqm_store_client = get_dqm_store(config=conf)

    # get groups' eos directories from their names in given "groups" argument
    groups_eos_directories = None
    if groups:
        groups_eos_directories = [d for gname, d in conf.get_plots_group_eos_dir_map().items() if gname in groups]

    # Get dict of {group: {run: era}} and find runs/eras
    if eras or runs:
        # If eras or runs given. If both of them are given, both are applied in the filters
        # ... which means their "AND" condition will be applied.
        groups_runs_of_eras_dict = dqm_store_client.get_groups_runs_of_eras(
            groups_eos_dirs=groups_eos_directories, eras=eras, runs=runs, run_limit=conf.plots.max_era_run_size
        )
    else:
        # No runs or ERAs given, so return recent run's results
        # TODO: find recent run from DQM folks instead of intuitive recent run finding!
        recent_run = dqm_store_client.get_max_run()
        logging.debug(f"recent_run: {recent_run}")
        groups_runs_of_eras_dict = dqm_store_client.get_groups_runs_of_eras(
            groups_eos_dirs=groups, runs=[recent_run], run_limit=conf.plots.max_era_run_size
        )

    logging.debug(f"groups_runs_of_eras_dict: {groups_runs_of_eras_dict}")

    list_of_groups_results = []
    # Iterate items of "ConfigDetectorGroup"
    for group_conf in conf.plots.groups:
        if groups and (group_conf.group_name in groups):
            continue  # skip the group
        group_result = get_group_histograms(
            group_conf=group_conf, run_era_map=groups_runs_of_eras_dict[group_conf.eos_directory]
        )
        if group_result:
            list_of_groups_results.append(group_result)

    resp = ResponseMain(runs=runs, eras=eras, groups=groups, groups_data=list_of_groups_results)
    # logging.debug(resp.model_dump_json())
    return resp
