# Load the data
import os
import pickle

import numpy as np

xu_masses = [500, 750, 1000, 1500, 2000, 2500]  # GeV
phi_masses = [1, 5, 10, 50, 100, 325]  # GeV
mc_names = ["signal", "ttbarmumu", "ttbarmumumunu"]

data_path = os.path.join(os.getcwd(), "data")
print("Loading data from", data_path)

data = {
    "xu_{}_phi_{}".format(xu_mass, phi_mass): {
        f"{mc}": np.load(
            os.path.join(
                data_path,
                f"xu_{xu_mass}_GeV",
                f"phi_{phi_mass}_GeV",
                f"{mc}.npy",
            )
        )
        for mc in mc_names
    }
    for xu_mass in xu_masses
    for phi_mass in phi_masses
}

with open(os.path.join(data_path, "histograms.pkl"), "rb") as f:
    histograms = pickle.load(f)

with open(os.path.join(data_path, "cross_sections.pkl"), "rb") as f:
    cross_sections = pickle.load(f)
print("Done!")
