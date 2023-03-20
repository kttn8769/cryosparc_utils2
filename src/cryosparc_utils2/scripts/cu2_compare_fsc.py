import argparse
import json
import os
import pathlib
import sys
from typing import List

import numpy as np
import matplotlib.pyplot as plt

from cryosparc_utils2.connection import communicate_cryosparc


def parse_args():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter, description=__doc__)
    parser.add_argument("--project-uid", type=str, required=True, help="Project UID.")
    parser.add_argument("--job-uid-list", nargs="+", type=str, required=True, help="Space separated list of job UIDs.")
    parser.add_argument(
        "--outfile", type=str, required=True, help="Output filename of plot figure. (e.g. fsccompare.png)"
    )
    parser.add_argument(
        "--conf", type=str, default=os.path.join(pathlib.Path.home(), ".cryosparc_conf.json"), help="Config file path."
    )
    parser.add_argument(
        "--target",
        type=str,
        default="noisesub",
        help="Which type of FSC to plot. Supported targets are: nomask, loosemask, tightmask, noisesub. noisesub corresponds to the corrected FSC value.",
    )
    args = parser.parse_args()

    print("##### Command #####\n\t" + " ".join(sys.argv))
    args_print_str = "##### Input parameters #####\n"
    for opt, val in vars(args).items():
        args_print_str += "\t{} : {}\n".format(opt, val)
    print(args_print_str)
    return args


def ticklabel_freq_to_resol(tick_val, tick_pos):
    tick_val = float(tick_val)
    if np.isclose(tick_val, 0):
        new_tick_val = "DC"
    else:
        new_tick_val = f"{1/tick_val:.1f}Å"
    return new_tick_val


def compare_fsc(project_uid: str, job_uid_list: List[str], outfile: str, conf: str, target: str) -> None:
    cs = communicate_cryosparc(conf_file=conf)
    pj = cs.find_project(project_uid)

    fsc_infos = {}
    for job_uid in job_uid_list:
        job = pj.find_job(job_uid)

        with job.download("job.json") as res:
            job_data = json.loads(res.read())
        summary_stats = None
        for result_group in job_data["output_result_groups"]:
            if "summary_stats" in result_group.keys():
                summary_stats = result_group["summary_stats"]
                break
        if summary_stats is None:
            sys.exit(f"summary_stats was not found in job.json of {project_uid}-{job_uid}")

        summary_stat_final = summary_stats[-1]
        if "fsc_info_autotight" not in summary_stat_final.keys():
            sys.exit(f"fsc_info_autotight was not found for {project_uid}-{job_uid}")
        fsc_info = summary_stat_final["fsc_info_autotight"]
        box_size = fsc_info["N"]
        pixel_size = fsc_info["psize"]
        wave_numbers = np.array(fsc_info["radwns"])
        fsc_info["resols"] = pixel_size * box_size / wave_numbers
        fsc_info["freqs"] = 1 / fsc_info["resols"]

        fsc_infos[job_uid] = fsc_info

    fig, ax = plt.subplots(layout="constrained")
    max_freq = 0
    for job_uid in job_uid_list:
        fsc_info = fsc_infos[job_uid]
        fsc_val = fsc_info[f"radwn_{target}_A"]
        if fsc_info["freqs"][-1] > max_freq:
            max_freq = fsc_info["freqs"][-1]
        ax.plot(fsc_info["freqs"], fsc_info[f"fsc_{target}"], label=f"{job_uid} ({fsc_val:.3f}Å)")
    ax.axhline(y=0.143, color="red", lw=0.4)
    ax.set_xlim(xmin=0, xmax=max_freq)
    ax.set_ylim(ymin=0, ymax=1)
    ax.xaxis.set_major_formatter(ticklabel_freq_to_resol)
    if target == "noisesub":
        title = "Corrected"
    else:
        title = target.title()
    ax.set_title(f'GSFSC Resolution ({title})')
    plt.grid()
    plt.legend(loc="center left")
    plt.savefig(outfile)
    print(f"Plot was saved as {outfile}")


def main():
    args = parse_args()
    compare_fsc(args.project_uid, args.job_uid_list, args.outfile, args.conf, args.target)


if __name__ == "__main__":
    main()
