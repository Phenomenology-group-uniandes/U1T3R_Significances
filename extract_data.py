import os

xu_masses = [500, 750, 1000, 1500, 2000]
phi_masses = [1, 5, 10, 50, 100, 325]
mc_names = ["signal", "ttbarmumu", "ttbarmumumunu"]
data_path = os.path.join(os.getcwd(), "data")
os.makedirs(data_path, exist_ok=True)

# Create a folder for each xu mass
for xu_mass in xu_masses:
    xu_path = os.path.join(data_path, "xu_{}_GeV".format(xu_mass))
    os.makedirs(xu_path, exist_ok=True)

    # Create a folder for each phi mass
    for phi_mass in phi_masses:
        phi_path = os.path.join(xu_path, "phi_{}_GeV".format(phi_mass))
        os.makedirs(phi_path, exist_ok=True)

        # move files to the data folder
        for mc_name in mc_names:
            xgb_path = os.path.join(
                os.getcwd(),
                "XGBoostOutputs",
                "xu{}GeV_phi{}GeV".format(xu_mass, phi_mass),
                "{}_{}_{}.npy".format(phi_mass, xu_mass, mc_name),
            )
            os.rename(
                xgb_path, os.path.join(phi_path, "{}.npy".format(mc_name))
            )
